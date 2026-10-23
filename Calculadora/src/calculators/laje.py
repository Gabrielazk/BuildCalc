import math
from src.calculators.tracos import consumo_concreto_por_m3, TRACO_CONCRETO_PADRAO

# Tipos de laje
TIPOS_LAJE = ["premoldada", "macica"]
TIPO_LAJE_PADRAO = "premoldada"

# Enchimento da laje pré-moldada treliçada
ENCHIMENTOS = ["eps", "lajota"]
ENCHIMENTO_PADRAO = "eps"

# Valores padrão
PERDA_PADRAO_LAJE = 5.0
CAPA_PADRAO_CM = 4.0

# Pré-moldada: concreto que entra entre as vigotas, além da capa (m³ por m² de laje)
# PROVISÓRIO, confirmar com o engenheiro (laje H12 = enchimento 8 cm + capa 4 cm)
CONCRETO_NERVURAS_M3_M2 = 0.012

# Lajotas cerâmicas por m² de laje (PROVISÓRIO, confirmar com o engenheiro)
LAJOTAS_POR_M2 = 12

# Preços PROVISÓRIOS (R$) até a tabela de preços ser refeita
# Laje pré-moldada vendida por m² (vigotas + enchimento)
PRECO_LAJE_PREMOLDADA_M2 = {"eps": 75.00, "lajota": 65.00}


def calcular_laje(
    area_m2: float,
    tipo: str = TIPO_LAJE_PADRAO,
    enchimento: str = ENCHIMENTO_PADRAO,
    capa_cm: float = CAPA_PADRAO_CM,
    espessura_cm: float = 0.0,
    perda_percentual: float = PERDA_PADRAO_LAJE,
    traco: str = TRACO_CONCRETO_PADRAO,
) -> dict:
    if area_m2 <= 0:
        return {"erro": "A área deve ser maior que zero."}
    if tipo not in TIPOS_LAJE:
        return {"erro": "Tipo de laje inválido."}
    if perda_percentual < 0:
        return {"erro": "A perda não pode ser negativa."}

    if tipo == "premoldada":
        if enchimento not in ENCHIMENTOS:
            return {"erro": "Tipo de enchimento inválido."}
        if capa_cm <= 0:
            return {"erro": "A espessura da capa deve ser maior que zero."}
        volume = area_m2 * (capa_cm / 100.0 + CONCRETO_NERVURAS_M3_M2)
    else:
        if espessura_cm <= 0:
            return {"erro": "Informe a espessura total da laje maciça."}
        volume = area_m2 * (espessura_cm / 100.0)

    consumo = consumo_concreto_por_m3(traco)
    if consumo is None:
        return {"erro": "Traço de concreto inválido."}

    fator = 1 + perda_percentual / 100.0
    volume_com_perda = volume * fator

    premoldada = (tipo == "premoldada")
    lajotas = math.ceil(area_m2 * LAJOTAS_POR_M2 * fator - 1e-9) if premoldada and enchimento == "lajota" else 0

    return {
        "area_m2": round(area_m2, 2),
        "tipo": tipo,
        "enchimento": enchimento if premoldada else "",
        "capa_cm": capa_cm if premoldada else 0.0,
        "espessura_cm": espessura_cm if not premoldada else 0.0,
        "perda_percentual": perda_percentual,
        "traco": traco,
        "volume_m3": round(volume, 3),
        "volume_com_perda_m3": round(volume_com_perda, 3),
        "laje_premoldada_m2": round(area_m2, 2) if premoldada else 0.0,
        "lajotas": lajotas,
        "sacos_cimento": math.ceil(volume_com_perda * consumo["sacos_cimento"] - 1e-9),
        "areia_m3": round(volume_com_perda * consumo["areia_m3"], 2),
        "pedra_m3": round(volume_com_perda * consumo["pedra_m3"], 2),
    }