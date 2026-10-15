def calcular_contrapiso(area_m2: float, espessura_cm: float = 3.0) -> dict:
    if area_m2 <= 0 or espessura_cm <= 0:
        return {"erro": "Valores devem ser maiores que zero."}

    volume_m3 = area_m2 * (espessura_cm / 100)
    sacos_cimento = volume_m3 * 7.0
    areia_m3 = volume_m3 * 0.6
    pedra_m3 = volume_m3 * 0.6

    return {
        "area_m2": round(area_m2, 2),
        "sacos_cimento": round(sacos_cimento, 1),
        "areia_m3": round(areia_m3, 2),
        "pedra_m3": round(pedra_m3, 2)
    }