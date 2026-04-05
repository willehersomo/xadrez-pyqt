import sys
from PySide6.QtWidgets import QApplication, QWidget, QMessageBox

from UI.ui_menu import Ui_Form

from banco.modelos_bd import sessao, Partida
from main.tabuleiro import Tabuleiro


class MenuInicial(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.btn_entrar.clicked.connect(self.verificar_e_entrar)

    def verificar_e_entrar(self):
        id_partida = self.input_id.text()
        nome_jogador = self.input_nome.text()
        cor_escolhida = self.combo_cor.currentText().lower()

        if not id_partida.isdigit() or not nome_jogador:
            QMessageBox.warning(self, "Erro", "Preencha um ID válido (apenas números) e o seu nome!")
            return

        id_partida = int(id_partida)

        partida = sessao.query(Partida).filter_by(id=id_partida).first()

        if not partida:
            print(f"Partida {id_partida} não encontrada. Criando uma nova...")
            partida = Partida(id=id_partida)
            if cor_escolhida == "brancas":
                partida.jogador_brancas = nome_jogador
            else:
                partida.jogador_pretas = nome_jogador
            sessao.add(partida)
            sessao.commit()
        else:
            if cor_escolhida == "brancas":
                if partida.jogador_brancas is not None and partida.jogador_brancas != nome_jogador:
                    QMessageBox.warning(self, "Erro", "Alguém já está jogando com as Brancas nesta partida!")
                    return
                else:
                    partida.jogador_brancas = nome_jogador
            elif cor_escolhida == "pretas":
                if partida.jogador_pretas is not None and partida.jogador_pretas != nome_jogador:
                    QMessageBox.warning(self, "Erro", "Alguém já está jogando com as Pretas nesta partida!")
                    return
                else:
                    partida.jogador_pretas = nome_jogador
            sessao.commit()

        self.abrir_tabuleiro(id_partida, cor_escolhida, nome_jogador)

    def abrir_tabuleiro(self, id_partida, cor, nome):
        self.janela_jogo = Tabuleiro(id_partida, cor, nome)
        self.janela_jogo.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    menu = MenuInicial()
    menu.show()
    sys.exit(app.exec())