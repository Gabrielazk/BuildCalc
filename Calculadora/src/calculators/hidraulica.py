import math

# Perda padrão (sobras e cortes de tubo)
PERDA_PADRAO_HIDRAULICA = 10.0

# Tubos (ordem em que aparecem na tela e no resultado)
#   fria:   PVC soldável marrom 25 mm (água fria)
#   quente: CPVC 22 mm (água quente)
#   esg40:  PVC branco 40 mm (esgoto de pia, chuveiro, ralo)
#   esg100: PVC branco 100 mm (esgoto do vaso e ramal principal)
TUBOS = ["fria", "quente", "esg40", "esg100"]

# Comprimento da barra vendida, em metros (embalagens fixas)
BARRA_TUBO_M = {"fria": 6.0, "quente": 3.0, "esg40": 6.0, "esg100": 6.0}

# Estimativa por ponto, para quem não tem o projeto (PROVISÓRIO, confirmar com o engenheiro)
TUBO_POR_PONTO_M = {
    "fria": {"fria": 4.0},                    # cada ponto de água fria: 4 m de tubo 25 mm
    "quente": {"quente": 5.0},                # cada ponto de água quente: 5 m de tubo 22 mm
    "esgoto": {"esg40": 3.0, "esg100": 2.0},  # cada ponto de esgoto: 3 m de 40 mm + 2 m de 100 mm
}
CONEXOES_POR_PONTO = {"fria": 4, "quente": 4, "esgoto": 3}  # joelhos, tês, luvas...
PONTOS_POR_REGISTRO = 4  # um registro de gaveta a cada 4 pontos de água (mais ou menos um por ambiente)

# Preços PROVISÓRIOS (R$) até a tabela de preços ser refeita
PRECO_BARRA_TUBO = {"fria": 30.00, "quente": 45.00, "esg40": 35.00, "esg100": 90.00}
PRECO_CONEXAO = {"fria": 3.00, "quente": 9.00, "esgoto": 6.00}
PRECO_REGISTRO = 45.00


def calcular_hidraulica(
    pontos_fria: int,
    pontos_quente: int,
    pontos_esgoto: int,
    tubos_m: dict = None,
    perda_percentual: float = PERDA_PADRAO_HIDRAULICA,
) -> dict:
    """tubos_m é opcional (quem tem o projeto): só os tubos informados substituem a estimativa."""
    if pontos_fria < 0 or pontos_quente < 0 or pontos_esgoto < 0:
        return {"erro": "As quantidades não podem ser negativas."}
    if pontos_fria + pontos_quente + pontos_esgoto <= 0:
        return {"erro": "Informe pelo menos um ponto de água fria, água quente ou esgoto."}
    tubos_m = tubos_m or {}
    if perda_percentual < 0 or any(v < 0 for v in tubos_m.values()):
        return {"erro": "Os valores não podem ser negativos."}

    fator = 1 + perda_percentual / 100.0
    pontos = {"fria": pontos_fria, "quente": pontos_quente, "esgoto": pontos_esgoto}

    tubos = {}
    for tubo in TUBOS:
        if tubo in tubos_m:
            base = tubos_m[tubo]
        else:
            base = sum(qtd * TUBO_POR_PONTO_M[tipo].get(tubo, 0.0) for tipo, qtd in pontos.items())
        total = base * fator
        if total > 0:
            tubos[tubo] = {
                "metros": round(total, 1),
                "barras": math.ceil(total / BARRA_TUBO_M[tubo] - 1e-9),
                "do_projeto": tubo in tubos_m,
            }

    conexoes = {tipo: qtd * CONEXOES_POR_PONTO[tipo] for tipo, qtd in pontos.items() if qtd > 0}
    pontos_agua = pontos_fria + pontos_quente
    registros = math.ceil(pontos_agua / PONTOS_POR_REGISTRO) if pontos_agua > 0 else 0

    return {
        "pontos_fria": pontos_fria,
        "pontos_quente": pontos_quente,
        "pontos_esgoto": pontos_esgoto,
        "perda_percentual": perda_percentual,
        "tubos": tubos,
        "conexoes": conexoes,
        "registros": registros,
    }