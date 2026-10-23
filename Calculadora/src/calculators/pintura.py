import math

# Valores padrão
DEMAOS_PADRAO = 2
PERDA_PADRAO_PINTURA = 10.0

# Rendimento da tinta: m² pintados com 1 litro, em UMA demão (PROVISÓRIO, confirmar com o engenheiro)
RENDIMENTO_PADRAO_M2_L = 12.0

# Embalagens fixas de tinta, selador e fundo preparador
LATA_L = 18.0
GALAO_L = 3.6
GALOES_POR_LATA = 5  # 5 galões = 1 lata; a partir daí compensa comprar a lata

# Complementos (uma demão cada), sobre a área total (parede + teto). PROVISÓRIO, confirmar com o engenheiro
RENDIMENTO_SELADOR_M2_L = 8.0
RENDIMENTO_FUNDO_M2_L = 10.0
TIPOS_MASSA = ["nenhuma", "corrida", "acrilica"]   # corrida: área interna seca; acrílica: externa ou úmida
CONSUMO_MASSA_KG_M2 = 0.5                         # 2 demãos finas
BALDE_MASSA_KG = 25.0

# Preços PROVISÓRIOS (R$) até a tabela de preços ser refeita
PRECO_TINTA = {
    "parede": {"lata": 300.00, "galao": 90.00},
    "teto": {"lata": 250.00, "galao": 75.00},
    "selador": {"lata": 150.00, "galao": 45.00},
    "fundo": {"lata": 170.00, "galao": 50.00},
}
PRECO_BALDE_MASSA = {"corrida": 80.00, "acrilica": 130.00}


def latas_e_galoes(litros: float):
    """Quantas latas de 18 L e galões de 3,6 L comprar para os litros pedidos."""
    if litros <= 0:
        return 0, 0
    latas = int(litros // LATA_L)
    resto = litros - latas * LATA_L
    galoes = math.ceil(resto / GALAO_L - 1e-9) if resto > 1e-9 else 0
    if galoes >= GALOES_POR_LATA:  # 5 galões ou mais: melhor levar mais uma lata
        latas += 1
        galoes = 0
    return latas, galoes


def calcular_pintura(
    area_parede_m2: float,
    area_teto_m2: float,
    demaos: int = DEMAOS_PADRAO,
    rendimento_m2_l: float = RENDIMENTO_PADRAO_M2_L,
    perda_percentual: float = PERDA_PADRAO_PINTURA,
    selador: bool = False,
    massa: str = "nenhuma",
    fundo: bool = False,
) -> dict:
    if area_parede_m2 < 0 or area_teto_m2 < 0:
        return {"erro": "As áreas não podem ser negativas."}
    if area_parede_m2 + area_teto_m2 <= 0:
        return {"erro": "Informe a área de parede ou a área de teto."}
    if demaos <= 0 or rendimento_m2_l <= 0:
        return {"erro": "Demãos e rendimento devem ser maiores que zero."}
    if perda_percentual < 0:
        return {"erro": "A perda não pode ser negativa."}
    if massa not in TIPOS_MASSA:
        return {"erro": "Tipo de massa inválido."}

    fator = 1 + perda_percentual / 100.0
    area_total = area_parede_m2 + area_teto_m2

    def produto(litros):
        latas, galoes = latas_e_galoes(litros)
        return {"litros": round(litros, 1), "latas": latas, "galoes": galoes}

    itens = {}
    if area_parede_m2 > 0:
        itens["parede"] = produto(area_parede_m2 * demaos / rendimento_m2_l * fator)
    if area_teto_m2 > 0:
        itens["teto"] = produto(area_teto_m2 * demaos / rendimento_m2_l * fator)
    if selador:
        itens["selador"] = produto(area_total / RENDIMENTO_SELADOR_M2_L * fator)
    if fundo:
        itens["fundo"] = produto(area_total / RENDIMENTO_FUNDO_M2_L * fator)

    massa_kg = area_total * CONSUMO_MASSA_KG_M2 * fator if massa != "nenhuma" else 0.0
    baldes_massa = math.ceil(massa_kg / BALDE_MASSA_KG - 1e-9) if massa_kg > 0 else 0

    return {
        "area_parede_m2": round(area_parede_m2, 2),
        "area_teto_m2": round(area_teto_m2, 2),
        "demaos": demaos,
        "rendimento_m2_l": rendimento_m2_l,
        "perda_percentual": perda_percentual,
        "itens": itens,
        "massa": massa,
        "massa_kg": round(massa_kg, 1),
        "baldes_massa": baldes_massa,
    }