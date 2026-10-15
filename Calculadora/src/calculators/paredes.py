import math

def calcular_paredes(comprimento_m: float, altura_m: float, rendimento_tijolo: float = 25.0) -> dict:
    if comprimento_m <= 0 or altura_m <= 0:
        return {"erro": "Comprimento e altura devem ser maiores que zero."}

    area_m2 = comprimento_m * altura_m
    total_tijolos = math.ceil(area_m2 * rendimento_tijolo * 1.05)  # 5% de perda

    sacos_cimento = area_m2 * 0.12
    sacos_cal = area_m2 * 0.15
    areia_m3 = area_m2 * 0.02

    return {
        "area_m2": round(area_m2, 2),
        "total_tijolos": total_tijolos,
        "sacos_cimento": round(sacos_cimento, 1),
        "sacos_cal": round(sacos_cal, 1),
        "areia_m3": round(areia_m3, 2)
    }