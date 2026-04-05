class Pecas:
    TAMANHO_CASA = 80

    estado = {
        "A8": "bR", "B8": "bN", "C8": "bB", "D8": "bQ",
        "E8": "bK", "F8": "bB", "G8": "bN", "H8": "bR",
        "A7": "bP", "B7": "bP", "C7": "bP", "D7": "bP",
        "E7": "bP", "F7": "bP", "G7": "bP", "H7": "bP",
        "A2": "wP", "B2": "wP", "C2": "wP", "D2": "wP",
        "E2": "wP", "F2": "wP", "G2": "wP", "H2": "wP",
        "A1": "wR", "B1": "wN", "C1": "wB", "D1": "wQ",
        "E1": "wK", "F1": "wB", "G1": "wN", "H1": "wR",
    }

    @staticmethod
    def caminho_svg(peca: str) -> str:
        return f"PECAS_SVG/{peca}.svg"