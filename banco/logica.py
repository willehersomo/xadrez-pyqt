from banco.modelos_bd import sessao, Partida


class JogoDeXadrez:
    def __init__(self, id_partida):
        self.id_partida = id_partida
        self.tabuleiro = []
        self.turno_atual = "brancas"
        self.en_passant_alvo = None
        self.status_jogo = "ativo"

        self.carregar_estado_da_base_dados()

    def carregar_estado_da_base_dados(self):
        sessao.commit()
        partida = sessao.query(Partida).filter_by(id=self.id_partida).first()
        if partida:
            self.turno_atual = partida.turno_atual
            self.fen_para_matriz(partida.estado_fen)

    def guardar_estado_na_base_dados(self):
        partida = sessao.query(Partida).filter_by(id=self.id_partida).first()
        if partida:
            partida.estado_fen = self.matriz_para_fen()
            partida.turno_atual = self.turno_atual
            sessao.commit()

    def fen_para_matriz(self, fen):
        self.tabuleiro = []
        parte_tabuleiro = fen.split(' ')[0]
        linhas_fen = parte_tabuleiro.split('/')
        for linha in linhas_fen:
            linha_matriz = []
            for char in linha:
                if char.isdigit():
                    for _ in range(int(char)): linha_matriz.append('--')
                else:
                    linha_matriz.append(char)
            self.tabuleiro.append(linha_matriz)

    def matriz_para_fen(self):
        fen = ""
        for linha in self.tabuleiro:
            vazias = 0
            for peca in linha:
                if peca == '--':
                    vazias += 1
                else:
                    if vazias > 0: fen += str(vazias); vazias = 0
                    fen += peca
            if vazias > 0: fen += str(vazias)
            fen += "/"
        return fen[:-1]

    def caminho_livre(self, l_origem, c_origem, l_destino, c_destino):
        passo_l = 0 if l_origem == l_destino else (1 if l_destino > l_origem else -1)
        passo_c = 0 if c_origem == c_destino else (1 if c_destino > c_origem else -1)
        l_atual, c_atual = l_origem + passo_l, c_origem + passo_c
        while l_atual != l_destino or c_atual != c_destino:
            if self.tabuleiro[l_atual][c_atual] != '--': return False
            l_atual += passo_l;
            c_atual += passo_c
        return True

    def validar_movimento_matematico(self, origem, destino):
        l_orig, c_orig = origem
        l_dest, c_dest = destino
        peca = self.tabuleiro[l_orig][c_orig]
        peca_dest = self.tabuleiro[l_dest][c_dest]
        tipo = peca.lower()

        if peca_dest != '--' and (peca.isupper() == peca_dest.isupper()):
            return False

        abs_l, abs_c = abs(l_dest - l_orig), abs(c_dest - c_orig)

        if tipo == 'n': return (abs_l == 2 and abs_c == 1) or (abs_l == 1 and abs_c == 2)
        if tipo == 'r': return (abs_l == 0 or abs_c == 0) and self.caminho_livre(l_orig, c_orig, l_dest, c_dest)
        if tipo == 'b': return (abs_l == abs_c) and self.caminho_livre(l_orig, c_orig, l_dest, c_dest)
        if tipo == 'q': return (abs_l == abs_c or abs_l == 0 or abs_c == 0) and self.caminho_livre(l_orig, c_orig,
                                                                                                   l_dest, c_dest)
        if tipo == 'k':
            # Roque
            if abs_l == 0 and abs_c == 2:
                col_torre = 7 if c_dest > c_orig else 0
                if self.tabuleiro[l_orig][col_torre].lower() == 'r':
                    return self.caminho_livre(l_orig, c_orig, l_orig, col_torre)
            return abs_l <= 1 and abs_c <= 1

        if tipo == 'p':
            dir = -1 if peca.isupper() else 1
            if c_orig == c_dest and peca_dest == '--':
                if l_dest == l_orig + dir: return True
                if l_orig == (6 if peca.isupper() else 1) and l_dest == l_orig + 2 * dir:
                    return self.tabuleiro[l_orig + dir][c_orig] == '--'
            if abs_c == 1 and l_dest == l_orig + dir:
                if peca_dest != '--': return True
                if (l_dest, c_dest) == self.en_passant_alvo: return True
        return False

    def aplicar_movimento_bruto(self, origem, destino):
        l_orig, c_orig = origem
        l_dest, c_dest = destino
        peca = self.tabuleiro[l_orig][c_orig]

        # En Passant
        if peca.lower() == 'p' and (l_dest, c_dest) == self.en_passant_alvo:
            self.tabuleiro[l_orig][c_dest] = '--'

        # Roque
        if peca.lower() == 'k' and abs(c_dest - c_orig) == 2:
            col_torre_orig = 7 if c_dest > c_orig else 0
            col_torre_dest = c_dest - 1 if c_dest > c_orig else c_dest + 1
            self.tabuleiro[l_orig][col_torre_dest] = self.tabuleiro[l_orig][col_torre_orig]
            self.tabuleiro[l_orig][col_torre_orig] = '--'

        # Move a peça
        self.tabuleiro[l_dest][c_dest] = peca
        self.tabuleiro[l_orig][c_orig] = '--'

        # Promoção
        if peca.lower() == 'p' and (l_dest == 0 or l_dest == 7):
            self.tabuleiro[l_dest][c_dest] = 'Q' if peca.isupper() else 'q'

    def esta_em_xeque(self, cor):
        rei = 'K' if cor == 'brancas' else 'k'
        pos_rei = None

        # achar o rei
        for l in range(8):
            for c in range(8):
                if self.tabuleiro[l][c] == rei:
                    pos_rei = (l, c)
                    break
        if not pos_rei: return False

        # xeque???
        for l in range(8):
            for c in range(8):
                peca = self.tabuleiro[l][c]
                if peca != '--':
                    cor_peca = 'brancas' if peca.isupper() else 'pretas'
                    if cor_peca != cor:
                        if self.validar_movimento_matematico((l, c), pos_rei):
                            return True
        return False

    def verificar_xeque_mate(self, cor):
        if not self.esta_em_xeque(cor):
            return False

        for l_orig in range(8):
            for c_orig in range(8):
                peca = self.tabuleiro[l_orig][c_orig]
                if peca != '--':
                    cor_peca = 'brancas' if peca.isupper() else 'pretas'
                    if cor_peca == cor:
                        for l_dest in range(8):
                            for c_dest in range(8):
                                if self.validar_movimento_matematico((l_orig, c_orig), (l_dest, c_dest)):
                                    fen_backup = self.matriz_para_fen()
                                    ep_backup = self.en_passant_alvo

                                    self.aplicar_movimento_bruto((l_orig, c_orig), (l_dest, c_dest))
                                    xeque_ainda = self.esta_em_xeque(cor)

                                    self.fen_para_matriz(fen_backup)
                                    self.en_passant_alvo = ep_backup

                                    if not xeque_ainda:
                                        return False
        return True

    def fazer_movimento(self, origem, destino):
        if self.status_jogo != "ativo":
            return False

        l_orig, c_orig = origem
        l_dest, c_dest = destino
        peca = self.tabuleiro[l_orig][c_orig]

        if not self.validar_movimento_matematico(origem, destino):
            return False

        fen_backup = self.matriz_para_fen()
        ep_backup = self.en_passant_alvo

        self.aplicar_movimento_bruto(origem, destino)

        if self.esta_em_xeque(self.turno_atual):
            self.fen_para_matriz(fen_backup)
            self.en_passant_alvo = ep_backup
            return False


        if peca.lower() == 'p' and abs(l_dest - l_orig) == 2:
            self.en_passant_alvo = (l_orig + (1 if l_dest > l_orig else -1), c_orig)
        else:
            self.en_passant_alvo = None

        self.turno_atual = "pretas" if self.turno_atual == "brancas" else "brancas"

        if self.verificar_xeque_mate(self.turno_atual):
            print(f"!!! XEQUE-MATE !!! Vitória das {'Brancas' if self.turno_atual == 'pretas' else 'Pretas'}!")
            self.status_jogo = "xeque_mate_" + ("brancas" if self.turno_atual == "pretas" else "pretas")

        self.guardar_estado_na_base_dados()
        return True
