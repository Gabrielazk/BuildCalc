import math

# Perda padrão do rejunte (sobras e limpeza da junta)
PERDA_PADRAO_REJUNTE = 10.0

# Espessura padrão da peça (mm), usada quando o cliente não informa (opcional)
ESPESSURA_PADRAO_MM = 8.0

# Densidade do rejunte cimentício em kg/dm³ (PROVISÓRIO, confirmar com o engenheiro)
DENSIDADE_REJUNTE = 1.58

# Embalagens fixas (latinhas de 1 kg e 2 kg)
LATA_PEQUENA_KG = 1
LATA_GRANDE_KG = 2

# Preços PROVISÓRIOS (R$) até a tabela de preços ser refeita
PRECO_LATA_1KG = 10.00
PRECO_LATA_2KG = 18.00


def calcular_rejunte(
    area_m2: float,
    largura_cm: float,
    altura_cm: float,
    junta_mm: float,
    espessura_mm: float = ESPESSURA_PADRAO_MM,
    perda_percentual: float = PERDA_PADRAO_REJUNTE,
) -> dict:
    if area_m2 <= 0 or largura_cm <= 0 or altura_cm <= 0 or junta_mm <= 0:
        return {"erro": "Área, tamanho da peça e junta devem ser maiores que zero."}
    if espessura_mm <= 0:
        return {"erro": "A espessura da peça deve ser maior que zero."}
    if perda_percentual < 0:
        return {"erro": "A perda não pode ser negativa."}

    # Fórmula usada pelos fabricantes de rejunte:
    # kg/m² = ((C + L) / (C x L)) x junta x espessura x densidade   (C e L da peça em mm)
    c_mm = largura_cm * 10.0
    l_mm = altura_cm * 10.0
    consumo_kg_m2 = ((c_mm + l_mm) / (c_mm * l_mm)) * junta_mm * espessura_mm * DENSIDADE_REJUNTE

    fator = 1 + perda_percentual / 100.0
    kg_total = area_m2 * consumo_kg_m2 * fator

    # Latinhas: o máximo possível de 2 kg e, se sobrar 1 kg, uma de 1 kg
    kg_compra = max(1, math.ceil(kg_total - 1e-9))
    latas_2kg = kg_compra // LATA_GRANDE_KG
    latas_1kg = kg_compra % LATA_GRANDE_KG

    return {
        "area_m2": round(area_m2, 2),
        "largura_cm": largura_cm,
        "altura_cm": altura_cm,
        "junta_mm": junta_mm,
        "espessura_mm": espessura_mm,
        "perda_percentual": perda_percentual,
        "consumo_kg_m2": round(consumo_kg_m2, 3),
        "kg_total": round(kg_total, 2),
        "kg_compra": kg_compra,
        "latas_1kg": latas_1kg,
        "latas_2kg": latas_2kg,
    }