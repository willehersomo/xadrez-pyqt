import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QMessageBox
from PySide6.QtGui import QIcon, QPixmap, QPainter
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import QSize, Qt, QTimer
from UI.ui_tabuleiro import Ui_MainWindow
import pecas as pc

from banco.logica import JogoDeXadrez


class Tabuleiro(QMainWindow, Ui_MainWindow):
    def __init__(self, id_partida, cor_jogador, nome_jogador):
        super().__init__()
        self.setupUi(self)

        self.id_partida = id_partida
        self.cor_jogador = cor_jogador
        self.nome_jogador = nome_jogador

        self.jogo = JogoDeXadrez(self.id_partida)
        self.setWindowTitle(
            f"Xadrez - Partida {self.id_partida} | Você é: {self.cor_jogador.capitalize()} ({self.nome_jogador})")

        self.casa_origem = None

        self.cena_capturadas = QGraphicsScene()
        self.graphicsView.setScene(self.cena_capturadas)

        self.conectar_botoes()
        self.carregar_pecas()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.verificar_atualizacoes)
        self.timer.start(2000)

        self.btn_Confirmar.clicked.connect(self.ao_desistir)

    def svg_para_icone(self, caminho: str, tamanho: int) -> QIcon:
        renderer = QSvgRenderer(caminho)
        pixmap = QPixmap(tamanho, tamanho)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        return QIcon(pixmap)

    def carregar_pecas(self):
        TAMANHO = 65

        for linha in ["1", "2", "3", "4", "5", "6", "7", "8"]:
            for col in ["A", "B", "C", "D", "E", "F", "G", "H"]:
                btn = getattr(self, f"btn_{col}{linha}")
                btn.setIcon(QIcon())

        mapa_fen_svg = {
            'r': 'bR', 'n': 'bN', 'b': 'bB', 'q': 'bQ', 'k': 'bK', 'p': 'bP',
            'R': 'wR', 'N': 'wN', 'B': 'wB', 'Q': 'wQ', 'K': 'wK', 'P': 'wP'
        }

        matriz = self.jogo.tabuleiro

        for r in range(8):
            for c in range(8):
                peca_fen = matriz[r][c]

                if peca_fen != '--':
                    coluna_str = chr(65 + c)
                    linha_str = str(8 - r)
                    casa = f"{coluna_str}{linha_str}"

                    nome_svg = mapa_fen_svg[peca_fen]
                    btn = getattr(self, f"btn_{casa}")
                    icone = self.svg_para_icone(pc.Pecas.caminho_svg(nome_svg), TAMANHO)
                    btn.setIcon(icone)
                    btn.setIconSize(QSize(TAMANHO, TAMANHO))

        self.atualizar_pecas_capturadas()

    def conectar_botoes(self):
        for linha in ["1", "2", "3", "4", "5", "6", "7", "8"]:
            for col in ["A", "B", "C", "D", "E", "F", "G", "H"]:
                casa = f"{col}{linha}"
                btn = getattr(self, f"btn_{casa}")
                btn.clicked.connect(lambda checked=False, c=casa: self.processar_clique(c))

    def converter_casa_para_matriz(self, casa: str):
        coluna_idx = ord(casa[0]) - 65
        linha_idx = 8 - int(casa[1])
        return linha_idx, coluna_idx

    def processar_clique(self, casa):
        linha_idx, col_idx = self.converter_casa_para_matriz(casa)

        if self.casa_origem is None:
            peca = self.jogo.tabuleiro[linha_idx][col_idx]
            if peca == '--':
                return
            cor_peca = "brancas" if peca.isupper() else "pretas"

            if self.jogo.turno_atual != self.cor_jogador:
                print("Aguarde, é o turno do adversário.")
                return
            if cor_peca != self.cor_jogador:
                print("Você não pode mover as peças do adversário!")
                return

            self.casa_origem = casa
            btn = getattr(self, f"btn_{casa}")
            btn.setStyleSheet("border: 3px solid #ffaa00; background-color: #ffd166;")

        else:
            if self.casa_origem == casa:
                self.limpar_selecao()
                return

            linha_origem, col_origem = self.converter_casa_para_matriz(self.casa_origem)
            sucesso = self.jogo.fazer_movimento((linha_origem, col_origem), (linha_idx, col_idx))

            if sucesso:
                print(f"Movimento: {self.casa_origem} -> {casa}")
            else:
                print("Movimento inválido pela lógica.")

            self.limpar_selecao()
            self.carregar_pecas()

            if self.jogo.status_jogo != "ativo":
                self.anunciar_fim_de_jogo()
                self.timer.stop()

    def limpar_selecao(self):
        if self.casa_origem:
            btn = getattr(self, f"btn_{self.casa_origem}")
            btn.setStyleSheet("")
            self.casa_origem = None

    def atualizar_pecas_capturadas(self):
        self.cena_capturadas.clear()

        pecas_iniciais = {'p': 8, 'r': 2, 'n': 2, 'b': 2, 'q': 1,
                          'P': 8, 'R': 2, 'N': 2, 'B': 2, 'Q': 1}

        contagem_atual = {k: 0 for k in pecas_iniciais}
        for linha in self.jogo.tabuleiro:
            for peca in linha:
                if peca in contagem_atual:
                    contagem_atual[peca] += 1

        alvos = ['q', 'r', 'b', 'n', 'p'] if self.cor_jogador == "brancas" else ['Q', 'R', 'B', 'N', 'P']

        mapa_fen_svg = {
            'r': 'bR', 'n': 'bN', 'b': 'bB', 'q': 'bQ', 'k': 'bK', 'p': 'bP',
            'R': 'wR', 'N': 'wN', 'B': 'wB', 'Q': 'wQ', 'K': 'wK', 'P': 'wP'
        }

        y_offset = 10
        for peca in alvos:
            qtd_capturada = pecas_iniciais[peca] - contagem_atual[peca]
            for _ in range(qtd_capturada):
                nome_svg = mapa_fen_svg[peca]
                caminho = pc.Pecas.caminho_svg(nome_svg)

                pixmap = QPixmap(40, 40)
                pixmap.fill(Qt.transparent)
                painter = QPainter(pixmap)
                renderer = QSvgRenderer(caminho)
                renderer.render(painter)
                painter.end()

                item = self.cena_capturadas.addPixmap(pixmap)
                item.setPos(25, y_offset)
                y_offset += 45

    def ao_desistir(self):
        resposta = QMessageBox.question(
            self, "Desistir", "Tem certeza que deseja abandonar a partida?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if resposta == QMessageBox.StandardButton.Yes:
            print(f"O jogador {self.nome_jogador} ({self.cor_jogador}) desistiu da partida!")
            self.close()

    def verificar_atualizacoes(self):
        if self.jogo.status_jogo != "ativo":
            self.anunciar_fim_de_jogo()
            self.timer.stop()
            return

        if self.jogo.turno_atual == self.cor_jogador:
            return

        self.jogo.carregar_estado_da_base_dados()

        if self.jogo.turno_atual == self.cor_jogador:
            print("O adversário jogou! Agora é a sua vez.")
            self.carregar_pecas()

            if self.jogo.status_jogo != "ativo":
                self.anunciar_fim_de_jogo()
                self.timer.stop()

    def anunciar_fim_de_jogo(self):
        vencedor = "Brancas" if self.jogo.status_jogo == "xeque_mate_brancas" else "Pretas"

        mensagem = QMessageBox(self)
        mensagem.setWindowTitle("Fim de Jogo!")

        if (self.cor_jogador == "brancas" and vencedor == "Brancas") or \
                (self.cor_jogador == "pretas" and vencedor == "Pretas"):
            texto = "Parabéns! Você VENCEU por Xeque-Mate!"
        else:
            texto = f"Xeque-Mate! As {vencedor} venceram a partida."

        mensagem.setText(texto)
        mensagem.exec()

