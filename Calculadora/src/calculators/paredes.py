import math
from src.calculators.tracos import (
    TRACOS_MASSA,
    TRACO_MASSA_PADRAO,
    DENSIDADE_CIMENTO,
    DENSIDADE_CAL,
    SACO_CIMENTO_KG,
    SACO_CAL_KG,
)

# Tijolos e blocos: medidas em cm, na ordem do nome (largura x altura x comprimento).
# ATENÇÃO (conferir com engenheiro): medidas e preços são premissas de trabalho.
# O preço aqui é PROVISÓRIO: vai para a tabela de preços (por país e estado) na etapa de preços.
TIJOLOS = {
    "baiano":      {"largura": 9.0,  "altura": 19.0, "comprimento": 19.0, "preco": 1.20},
    "baiano_9f":   {"largura": 9.0,  "altura": 14.0, "comprimento": 19.0, "preco": 1.00},
    "bloco_9":     {"largura": 9.0,  "altura": 19.0, "comprimento": 39.0, "preco": 3.00},
    "bloco_14":    {"largura": 14.0, "altura": 19.0, "comprimento": 39.0, "preco": 4.50},
    "bloco_19":    {"largura": 19.0, "altura": 19.0, "comprimento": 39.0, "preco": 6.00},
}
TIJOLO_PADRAO = "baiano"

# Assentamento: qual lado do tijolo fica como espessura da parede.
#   em pé:   aparece o comprimento x a altura; a espessura da parede é a largura
#   deitado: aparece o comprimento x a largura; a espessura da parede é a altura
ASSENTAMENTOS = ["em_pe", "deitado"]
ASSENTAMENTO_PADRAO = "em_pe"

JUNTA_PADRAO_CM = 1.0
QUEBRA_PADRAO_PERCENTUAL = 5.0


def calcular_paredes(
    area_bruta_m2: float,
    tijolo: str = TIJOLO_PADRAO,
    assentamento: str = ASSENTAMENTO_PADRAO,
    desconto_vaos_m2: float = 0.0,
    junta_cm: float = JUNTA_PADRAO_CM,
    quebra_percentual: float = QUEBRA_PADRAO_PERCENTUAL,
    traco: str = TRACO_MASSA_PADRAO,
) -> dict:
    if area_bruta_m2 <= 0:
        return {"erro": "A área da parede deve ser maior que zero."}
    if desconto_vaos_m2 < 0 or junta_cm < 0 or quebra_percentual < 0:
        return {"erro": "Desconto, junta e quebra não podem ser negativos."}
    if tijolo not in TIJOLOS:
        return {"erro": "Tipo de tijolo ou bloco inválido."}
    if assentamento not in ASSENTAMENTOS:
        return {"erro": "Assentamento inválido."}
    partes = TRACOS_MASSA.get(traco)
    if partes is None:
        return {"erro": "Traço da massa inválido."}

    area_liquida_m2 = area_bruta_m2 - desconto_vaos_m2
    if area_liquida_m2 <= 0:
        return {"erro": "O desconto de portas e janelas não pode ser maior que a área da parede."}

    dados = TIJOLOS[tijolo]
    if assentamento == "em_pe":
        face_comprimento_cm = dados["comprimento"]
        face_altura_cm = dados["altura"]
        espessura_cm = dados["largura"]
    else:
        face_comprimento_cm = dados["comprimento"]
        face_altura_cm = dados["largura"]
        espessura_cm = dados["altura"]

    # Quantas peças cabem em 1 m2 (a junta entra na medida de cada peça)
    peca_com_junta_m2 = ((face_comprimento_cm + junta_cm) / 100.0) * ((face_altura_cm + junta_cm) / 100.0)
    pecas_por_m2 = 1.0 / peca_com_junta_m2
    unidades = math.ceil(area_liquida_m2 * pecas_por_m2 * (1 + quebra_percentual / 100.0))
    milheiros = unidades / 1000.0

    # Volume de massa = o que sobra na parede depois de tirar o volume dos tijolos
    area_face_peca_m2 = (face_comprimento_cm / 100.0) * (face_altura_cm / 100.0)
    massa_por_m2_m3 = (espessura_cm / 100.0) * (1.0 - pecas_por_m2 * area_face_peca_m2)
    volume_massa_m3 = massa_por_m2_m3 * area_liquida_m2

    total_partes = partes["cimento"] + partes["cal"] + partes["areia"]
    vol_cimento = volume_massa_m3 * partes["cimento"] / total_partes
    vol_cal = volume_massa_m3 * partes["cal"] / total_partes
    vol_areia = volume_massa_m3 * partes["areia"] / total_partes

    sacos_cimento = math.ceil(vol_cimento * DENSIDADE_CIMENTO / SACO_CIMENTO_KG)
    sacos_cal = math.ceil(vol_cal * DENSIDADE_CAL / SACO_CAL_KG)
    areia_m3 = round(vol_areia, 2)

    return {
        "area_bruta_m2": round(area_bruta_m2, 2),
        "desconto_vaos_m2": round(desconto_vaos_m2, 2),
        "area_liquida_m2": round(area_liquida_m2, 2),
        "tijolo": tijolo,
        "assentamento": assentamento,
        "junta_cm": junta_cm,
        "quebra_percentual": quebra_percentual,
        "pecas_por_m2": round(pecas_por_m2, 2),
        "unidades": unidades,
        "milheiros": round(milheiros, 2),
        "preco_unitario": dados["preco"],
        "traco": traco,
        "volume_massa_m3": round(volume_massa_m3, 3),
        "sacos_cimento": sacos_cimento,
        "sacos_cal": sacos_cal,
        "areia_m3": areia_m3,
    }