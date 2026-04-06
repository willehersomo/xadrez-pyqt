from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class Partida(Base):
    __tablename__ = 'partidas_xadrez'

    id = Column(Integer, primary_key=True)
    jogador_brancas = Column(String(50))
    jogador_pretas = Column(String(50))

    estado_fen = Column(String(100), default="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")

    turno_atual = Column(String(10), default="brancas")


URL_BASE_DADOS = 'mysql+pymysql://avnadmin:AVNS_E3bxwaNSVrU_t8UwOQU@xadrez-pyqt-xadrez-pyqt.g.aivencloud.com:22586/defaultdb'
#se for testar, avisa pra eu ligar o servidor

engine = create_engine(URL_BASE_DADOS, connect_args={'ssl': {}})

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
sessao = Session()

if __name__ == "__main__":
    nova_partida = Partida(jogador_brancas=None, jogador_pretas=None)
    sessao.add(nova_partida)
    sessao.commit()

    print(f"Nova partida criada com sucesso! O ID dela é: {nova_partida.id}")