import math

def calcular_brocas(
    quantidade: int,
    profundidade_m: float,
    diametro_cm: float,
    perda_percentual: float = 10.0,
    incluir_ferragem: bool = False,
    num_barras_longitudinais: int = 0,
    bitola_mm: float = 8.0,
    preco_mao_obra_metro: float = 0.0
) -> dict:
    if quantidade <= 0 or profundidade_m <= 0 or diametro_cm <= 0:
        return {"erro": "Quantidade, profundidade e diâmetro devem ser maiores que zero."}
    
    raio_m = (diametro_cm / 100.0) / 2.0
    area_base_m2 = math.pi * (raio_m ** 2)
    volume_nominal_m3 = area_base_m2 * profundidade_m * quantidade
    
    # Perda ajustável
    fator_perda = 1.0 + (perda_percentual / 100.0)
    volume_total_m3 = volume_nominal_m3 * fator_perda
    
    sacos_cimento = math.ceil(volume_total_m3 * 7.0)
    areia_m3 = round(volume_total_m3 * 0.55, 2)
    pedra_m3 = round(volume_total_m3 * 0.85, 2)
    
    # Ferragem Opcional
    total_metros_barras = 0.0
    quilos_aco = 0.0
    barras_12m = 0
    
    if incluir_ferragem and num_barras_longitudinais > 0:
        total_metros_barras = quantidade * profundidade_m * num_barras_longitudinais
        peso_por_metro = 0.395 if bitola_mm <= 8.0 else 0.617
        quilos_aco = round(total_metros_barras * peso_por_metro, 2)
        barras_12m = math.ceil(total_metros_barras / 12.0)
        
    # Mão de Obra Opcional
    total_metros_escavados = quantidade * profundidade_m
    custo_mao_obra = round(total_metros_escavados * preco_mao_obra_metro, 2)
    
    return {
        "volume_nominal_m3": round(volume_nominal_m3, 3),
        "volume_com_perda_m3": round(volume_total_m3, 3),
        "perda_percentual": perda_percentual,
        "sacos_cimento": sacos_cimento,
        "areia_m3": areia_m3,
        "pedra_m3": pedra_m3,
        "incluiu_ferragem": incluir_ferragem,
        "total_metros_barras": total_metros_barras,
        "quilos_aco": quilos_aco,
        "barras_12m": barras_12m,
        "total_metros_escavados": round(total_metros_escavados, 2),
        "custo_mao_obra": custo_mao_obra
    }