def calcular_baldrame(comprimento_m: float, largura_cm: float, altura_cm: float, perda_percentual: float = 10.0) -> dict:
    if comprimento_m <= 0 or largura_cm <= 0 or altura_cm <= 0:
        return {"erro": "Valores devem ser maiores que zero."}
    if perda_percentual < 0:
        return {"erro": "A perda não pode ser negativa."}

    largura_m = largura_cm / 100
    altura_m = altura_cm / 100

    volume = comprimento_m * largura_m * altura_m
    volume_com_perda = volume * (1 + perda_percentual / 100.0)

    sacos_cimento = volume_com_perda * 7.0
    areia_m3 = volume_com_perda * 0.55
    pedra_m3 = volume_com_perda * 0.85

    return {
        "volume_m3": round(volume, 3),
        "volume_com_perda_m3": round(volume_com_perda, 3),
        "perda_percentual": perda_percentual,
        "sacos_cimento": round(sacos_cimento, 1),
        "areia_m3": round(areia_m3, 2),
        "pedra_m3": round(pedra_m3, 2)
    }