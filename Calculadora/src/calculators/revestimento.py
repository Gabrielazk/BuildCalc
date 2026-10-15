import math

def calcular_revestimento(area_m2: float, consumo_argamassa_kg_m2: float = 5.0, consumo_rejunte_kg_m2: float = 0.5) -> dict:
    if area_m2 <= 0:
        return {"erro": "Área deve ser maior que zero."}

    total_argamassa_kg = area_m2 * consumo_argamassa_kg_m2
    sacos_argamassa_20kg = math.ceil(total_argamassa_kg / 20.0)
    total_rejunte_kg = round(area_m2 * consumo_rejunte_kg_m2, 2)

    return {
        "area_m2": round(area_m2, 2),
        "sacos_argamassa_20kg": sacos_argamassa_20kg,
        "rejunte_kg": total_rejunte_kg
    }