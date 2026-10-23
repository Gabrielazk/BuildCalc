import math

# Tipos de telha
TIPOS_TELHA = ["ceramica", "concreto", "fibrocimento"]
TIPO_TELHA_PADRAO = "ceramica"

# Perda padrão (quebras e recortes)
PERDA_PADRAO_TELHADO = 5.0

# Inclinação padrão (%) de cada tipo de telha (PROVISÓRIO, confirmar com o engenheiro)
INCLINACAO_PADRAO = {"ceramica": 30.0, "concreto": 30.0, "fibrocimento": 15.0}

# Telhas por m² de telhado (PROVISÓRIO, confirmar com o engenheiro)
# Cerâmica: tipo romana. Fibrocimento: telha de 2,44 x 1,10 m (cerca de 2,4 m² úteis cada)
TELHAS_POR_M2 = {"ceramica": 16.0, "concreto": 10.5, "fibrocimento": 1 / 2.4}

# Peças de cumeeira por metro (PROVISÓRIO, confirmar com o engenheiro)
CUMEEIRAS_POR_M = {"ceramica": 3.0, "concreto": 3.0, "fibrocimento": 1.0}

# Madeiramento: metros de madeira por m² de telhado (PROVISÓRIO, confirmar com o engenheiro)
# Telha fibrocimento vai direto nas terças (sem ripas e caibros)
MADEIRA_POR_M2 = {
    "ceramica": {"ripas": 3.0, "caibros": 2.0, "tercas": 0.6},
    "concreto": {"ripas": 3.0, "caibros": 2.0, "tercas": 0.6},
    "fibrocimento": {"ripas": 0.0, "caibros": 0.0, "tercas": 0.8},
}

# Preços PROVISÓRIOS (R$) até a tabela de preços ser refeita
PRECO_TELHA = {"ceramica": 2.50, "concreto": 4.50, "fibrocimento": 75.00}      # por telha
PRECO_CUMEEIRA = {"ceramica": 4.00, "concreto": 8.00, "fibrocimento": 45.00}   # por peça
PRECO_MADEIRA_M = {"ripas": 3.00, "caibros": 9.00, "tercas": 25.00}            # por metro


def calcular_telhado(
    area_m2: float,
    tipo_telha: str = TIPO_TELHA_PADRAO,
    inclinacao_percentual: float = None,
    cumeeira_m: float = 0.0,
    incluir_madeiramento: bool = False,
    perda_percentual: float = PERDA_PADRAO_TELHADO,
) -> dict:
    if tipo_telha not in TIPOS_TELHA:
        return {"erro": "Tipo de telha inválido."}
    if inclinacao_percentual is None:
        inclinacao_percentual = INCLINACAO_PADRAO[tipo_telha]
    if area_m2 <= 0:
        return {"erro": "A área deve ser maior que zero."}
    if inclinacao_percentual < 0 or cumeeira_m < 0 or perda_percentual < 0:
        return {"erro": "Os valores não podem ser negativos."}

    # A área informada é a da planta (vista de cima); a inclinação aumenta a área real do telhado
    area_real = area_m2 * math.sqrt(1 + (inclinacao_percentual / 100.0) ** 2)
    fator = 1 + perda_percentual / 100.0

    telhas = math.ceil(area_real * TELHAS_POR_M2[tipo_telha] * fator - 1e-9)
    cumeeiras = math.ceil(cumeeira_m * CUMEEIRAS_POR_M[tipo_telha] * fator - 1e-9) if cumeeira_m > 0 else 0

    madeira = {"ripas": 0.0, "caibros": 0.0, "tercas": 0.0}
    if incluir_madeiramento:
        for peca, metros_m2 in MADEIRA_POR_M2[tipo_telha].items():
            madeira[peca] = round(area_real * metros_m2 * fator, 1)

    return {
        "area_planta_m2": round(area_m2, 2),
        "inclinacao_percentual": inclinacao_percentual,
        "area_real_m2": round(area_real, 2),
        "tipo_telha": tipo_telha,
        "perda_percentual": perda_percentual,
        "telhas": telhas,
        "cumeeira_m": round(cumeeira_m, 2),
        "cumeeiras": cumeeiras,
        "incluiu_madeiramento": incluir_madeiramento,
        "ripas_m": madeira["ripas"],
        "caibros_m": madeira["caibros"],
        "tercas_m": madeira["tercas"],
    }