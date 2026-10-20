import math
from src.calculators.tracos import consumo_concreto_por_m3, TRACO_CONCRETO_PADRAO

# Peso (kg por metro) das bitolas comerciais de aço (mm -> kg/m).
# ATENÇÃO (conferir na revisão dos cálculos): valores de tabela de trabalho.
PESO_POR_METRO = {
    5.0: 0.154,
    6.3: 0.245,
    8.0: 0.395,
    10.0: 0.617,
    12.5: 0.963,
    16.0: 1.578,
    20.0: 2.466,
}

# Bitolas oferecidas na tela para o ferro longitudinal (a de 5 mm fica só para estribo)
BITOLAS_LONGITUDINAL = [6.3, 8.0, 10.0, 12.5, 16.0]
BITOLA_PADRAO = 8.0

# Estribos (premissas de trabalho, a conferir)
BITOLA_ESTRIBO_MM = 5.0
ESPACAMENTO_ESTRIBO_PADRAO_CM = 20.0
COBRIMENTO_CM = 3.0        # concreto que cobre o estribo
GANCHO_ESTRIBO_CM = 10.0   # sobra para fechar o estribo

BARRA_COMERCIAL_M = 12.0


def calcular_brocas(
    quantidade: int,
    profundidade_m: float,
    diametro_cm: float,
    perda_percentual: float = 10.0,
    incluir_ferragem: bool = False,
    num_barras_longitudinais: int = 0,
    bitola_mm: float = BITOLA_PADRAO,
    preco_mao_obra_metro: float = 0.0,
    traco: str = TRACO_CONCRETO_PADRAO,
    espacamento_estribo_cm: float = ESPACAMENTO_ESTRIBO_PADRAO_CM
) -> dict:
    if quantidade <= 0 or profundidade_m <= 0 or diametro_cm <= 0:
        return {"erro": "Quantidade, profundidade e diâmetro devem ser maiores que zero."}
    if perda_percentual < 0:
        return {"erro": "A perda não pode ser negativa."}
    if num_barras_longitudinais < 0 or espacamento_estribo_cm < 0:
        return {"erro": "Barras e espaçamento dos estribos não podem ser negativos."}
    if bitola_mm not in PESO_POR_METRO:
        return {"erro": "Bitola do ferro inválida."}

    raio_m = (diametro_cm / 100.0) / 2.0
    area_base_m2 = math.pi * (raio_m ** 2)
    volume_nominal_m3 = area_base_m2 * profundidade_m * quantidade

    # Perda ajustável
    fator_perda = 1.0 + (perda_percentual / 100.0)
    volume_total_m3 = volume_nominal_m3 * fator_perda

    consumo = consumo_concreto_por_m3(traco)
    if consumo is None:
        return {"erro": "Traço de concreto inválido."}

    sacos_cimento = math.ceil(volume_total_m3 * consumo["sacos_cimento"])
    areia_m3 = round(volume_total_m3 * consumo["areia_m3"], 2)
    pedra_m3 = round(volume_total_m3 * consumo["pedra_m3"], 2)

    # Ferragem opcional: ferro longitudinal + estribos
    total_metros_barras = 0.0
    kg_longitudinal = 0.0
    barras_longitudinal = 0
    estribos_por_broca = 0
    total_estribos = 0
    total_metros_estribos = 0.0
    kg_estribos = 0.0
    barras_estribos = 0

    if incluir_ferragem and num_barras_longitudinais > 0:
        total_metros_barras = quantidade * profundidade_m * num_barras_longitudinais
        kg_longitudinal = round(total_metros_barras * PESO_POR_METRO[bitola_mm], 2)
        barras_longitudinal = math.ceil(total_metros_barras / BARRA_COMERCIAL_M)

        if espacamento_estribo_cm > 0:
            diametro_interno_cm = diametro_cm - 2 * COBRIMENTO_CM
            if diametro_interno_cm <= 0:
                return {"erro": "Diâmetro muito pequeno para colocar estribos."}
            comprimento_estribo_m = (math.pi * diametro_interno_cm + GANCHO_ESTRIBO_CM) / 100.0
            estribos_por_broca = int(profundidade_m * 100.0 // espacamento_estribo_cm) + 1
            total_estribos = estribos_por_broca * quantidade
            total_metros_estribos = total_estribos * comprimento_estribo_m
            kg_estribos = round(total_metros_estribos * PESO_POR_METRO[BITOLA_ESTRIBO_MM], 2)
            barras_estribos = math.ceil(total_metros_estribos / BARRA_COMERCIAL_M)

    quilos_aco = round(kg_longitudinal + kg_estribos, 2)
    barras_12m = barras_longitudinal + barras_estribos

    # Mão de obra opcional
    total_metros_escavados = quantidade * profundidade_m
    custo_mao_obra = round(total_metros_escavados * preco_mao_obra_metro, 2)

    return {
        "volume_nominal_m3": round(volume_nominal_m3, 3),
        "volume_com_perda_m3": round(volume_total_m3, 3),
        "perda_percentual": perda_percentual,
        "traco": traco,
        "sacos_cimento": sacos_cimento,
        "areia_m3": areia_m3,
        "pedra_m3": pedra_m3,
        "incluiu_ferragem": incluir_ferragem and num_barras_longitudinais > 0,
        "bitola_mm": bitola_mm,
        "total_metros_barras": round(total_metros_barras, 2),
        "kg_longitudinal": kg_longitudinal,
        "barras_12m_longitudinal": barras_longitudinal,
        "incluiu_estribos": total_estribos > 0,
        "bitola_estribo_mm": BITOLA_ESTRIBO_MM,
        "espacamento_estribo_cm": espacamento_estribo_cm,
        "total_estribos": total_estribos,
        "total_metros_estribos": round(total_metros_estribos, 2),
        "kg_estribos": kg_estribos,
        "barras_12m_estribos": barras_estribos,
        "quilos_aco": quilos_aco,
        "barras_12m": barras_12m,
        "total_metros_escavados": round(total_metros_escavados, 2),
        "custo_mao_obra": custo_mao_obra
    }