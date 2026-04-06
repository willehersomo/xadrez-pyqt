from banco.modelos_bd import sessao, Partida

try:
    quantidade = sessao.query(Partida).delete()
    sessao.commit()

    print(f"Banco limpo! {quantidade} partidas apagadas.")

except Exception as e:
    sessao.rollback()
    print(f"Erro ao limpar o banco: {e}")

