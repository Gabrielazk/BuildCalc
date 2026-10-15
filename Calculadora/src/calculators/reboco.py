def calcular_reboco(area_m2: float, espessura_cm: float = 2.0) -> dict:
    if area_m2 <= 0 or espessura_cm <= 0:
        return {"erro": "Valores devem ser maiores que zero."}

    volume_m3 = area_m2 * (espessura_cm / 100)
    sacos_cimento = volume_m3 * 6.0
    sacos_cal = volume_m3 * 6.0
    areia_m3 = volume_m3 * 1.05

    return {
        "area_m2": round(area_m2, 2),
        "sacos_cimento": round(sacos_cimento, 1),
        "sacos_cal": round(sacos_cal, 1),
        "areia_m3": round(areia_m3, 2)
    }