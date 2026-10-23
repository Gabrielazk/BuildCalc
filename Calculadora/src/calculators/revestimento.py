import math

# Perda padrão de piso e azulejo (recortes e quebras)
PERDA_PADRAO_REVESTIMENTO = 10.0

# Argamassa colante (de saco): AC-I, AC-II e AC-III
TIPOS_ARGAMASSA = ["AC-I", "AC-II", "AC-III"]
ARGAMASSA_PADRAO_PISO = "AC-I"
ARGAMASSA_PADRAO_AZULEJO = "AC-II"  # AC-III para áreas molhadas (o cliente escolhe)
SACO_ARGAMASSA_KG = 20.0

# Consumo de argamassa (mesma regra do app antigo): 5 kg/m², ou 8 kg/m² se a peça for maior que 0,9 m²
CONSUMO_ARGAMASSA_KG_M2 = 5.0
CONSUMO_ARGAMASSA_PECA_GRANDE_KG_M2 = 8.0
AREA_PECA_GRANDE_M2 = 0.9

# Rodapé: comprimento de cada peça (PROVISÓRIO, confirmar com o engenheiro)
RODAPE_PECA_M = 2.40

# Preços PROVISÓRIOS (R$) até a tabela de preços ser refeita
PRECO_PISO_M2 = 50.00
PRECO_AZULEJO_M2 = 40.00
PRECO_RODAPE_M = 15.00
PRECO_ARGAMASSA_SACO = {"AC-I": 22.00, "AC-II": 30.00, "AC-III": 42.00}


def _calcular_ceramica(
    area_m2: float,
    largura_cm: float,
    altura_cm: float,
    desconto_vaos_m2: float,
    m2_por_caixa: float,
    tipo_argamassa: str,
    perda_percentual: float,
    rodape_m: float,
) -> dict:
    if area_m2 <= 0 or largura_cm <= 0 or altura_cm <= 0:
        return {"erro": "Área e tamanho da peça devem ser maiores que zero."}
    if desconto_vaos_m2 < 0 or m2_por_caixa < 0 or rodape_m < 0 or perda_percentual < 0:
        return {"erro": "Os valores não podem ser negativos."}
    if desconto_vaos_m2 >= area_m2:
        return {"erro": "O desconto de vãos deve ser menor que a área."}
    if tipo_argamassa not in TIPOS_ARGAMASSA:
        return {"erro": "Tipo de argamassa inválido."}

    area_liquida = area_m2 - desconto_vaos_m2
    fator = 1 + perda_percentual / 100.0
    area_com_perda = area_liquida * fator
    area_peca = (largura_cm / 100.0) * (altura_cm / 100.0)
    pecas = math.ceil(area_com_perda / area_peca - 1e-9)
    caixas = math.ceil(area_com_perda / m2_por_caixa - 1e-9) if m2_por_caixa > 0 else 0

    consumo = CONSUMO_ARGAMASSA_PECA_GRANDE_KG_M2 if area_peca > AREA_PECA_GRANDE_M2 else CONSUMO_ARGAMASSA_KG_M2
    argamassa_kg = area_com_perda * consumo
    sacos = math.ceil(argamassa_kg / SACO_ARGAMASSA_KG - 1e-9)

    rodape_com_perda = rodape_m * fator
    rodape_pecas = math.ceil(rodape_com_perda / RODAPE_PECA_M - 1e-9) if rodape_m > 0 else 0

    return {
        "area_bruta_m2": round(area_m2, 2),
        "desconto_vaos_m2": round(desconto_vaos_m2, 2),
        "area_liquida_m2": round(area_liquida, 2),
        "area_com_perda_m2": round(area_com_perda, 2),
        "perda_percentual": perda_percentual,
        "largura_cm": largura_cm,
        "altura_cm": altura_cm,
        "pecas": pecas,
        "m2_por_caixa": m2_por_caixa,
        "caixas": caixas,
        "tipo_argamassa": tipo_argamassa,
        "argamassa_kg": round(argamassa_kg, 1),
        "sacos_argamassa": sacos,
        "rodape_m": round(rodape_com_perda, 2),
        "rodape_pecas": rodape_pecas,
    }


def calcular_piso(
    area_m2: float,
    largura_cm: float,
    altura_cm: float,
    m2_por_caixa: float = 0.0,
    tipo_argamassa: str = ARGAMASSA_PADRAO_PISO,
    perda_percentual: float = PERDA_PADRAO_REVESTIMENTO,
    rodape_m: float = 0.0,
) -> dict:
    return _calcular_ceramica(area_m2, largura_cm, altura_cm, 0.0, m2_por_caixa,
                              tipo_argamassa, perda_percentual, rodape_m)


def calcular_azulejo(
    area_parede_m2: float,
    largura_cm: float,
    altura_cm: float,
    desconto_vaos_m2: float = 0.0,
    m2_por_caixa: float = 0.0,
    tipo_argamassa: str = ARGAMASSA_PADRAO_AZULEJO,
    perda_percentual: float = PERDA_PADRAO_REVESTIMENTO,
) -> dict:
    return _calcular_ceramica(area_parede_m2, largura_cm, altura_cm, desconto_vaos_m2, m2_por_caixa,
                              tipo_argamassa, perda_percentual, 0.0)