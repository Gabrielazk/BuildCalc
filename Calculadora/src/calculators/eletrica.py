import math

# Perda padrão (sobras de fio e conduíte)
PERDA_PADRAO_ELETRICA = 10.0

# Bitolas de fio (mm²)
BITOLAS_FIO = [1.5, 2.5, 4.0, 6.0]

# Embalagens fixas
ROLO_CONDUITE_M = 50.0   # conduíte corrugado 3/4"
ROLO_FIO_M = 100.0

# Estimativa por ponto, para quem não tem o projeto (PROVISÓRIO, confirmar com o engenheiro)
CONDUITE_POR_PONTO_M = 5.0          # metros de conduíte por tomada, interruptor ou ponto de luz
FIO_POR_TOMADA_M = {2.5: 15.0}       # fase, neutro e terra (3 fios x 5 m)
FIO_POR_INTERRUPTOR_M = {1.5: 10.0}  # fase e retorno (2 fios x 5 m)
FIO_POR_LUZ_M = {1.5: 10.0}          # neutro e retorno (2 fios x 5 m)

# Preços PROVISÓRIOS (R$) até a tabela de preços ser refeita
PRECO_ROLO_CONDUITE = 75.00
PRECO_ROLO_FIO = {1.5: 150.00, 2.5: 230.00, 4.0: 360.00, 6.0: 530.00}
PRECO_CAIXA_4X2 = 2.50        # caixinha de tomada e interruptor
PRECO_CAIXA_OCTOGONAL = 5.00  # caixa do ponto de luz no teto
PRECO_TOMADA = 15.00
PRECO_INTERRUPTOR = 12.00


def calcular_eletrica(
    tomadas: int,
    interruptores: int,
    pontos_luz: int,
    conduite_m: float = None,
    fios_m: dict = None,
    perda_percentual: float = PERDA_PADRAO_ELETRICA,
) -> dict:
    """conduite_m e fios_m são opcionais (quem tem o projeto).
    Em fios_m, só as bitolas informadas substituem a estimativa; as outras continuam estimadas."""
    if tomadas < 0 or interruptores < 0 or pontos_luz < 0:
        return {"erro": "As quantidades não podem ser negativas."}
    if tomadas + interruptores + pontos_luz <= 0:
        return {"erro": "Informe pelo menos uma tomada, interruptor ou ponto de luz."}
    if perda_percentual < 0 or (conduite_m is not None and conduite_m < 0):
        return {"erro": "Os valores não podem ser negativos."}
    fios_m = fios_m or {}
    if any(v < 0 for v in fios_m.values()):
        return {"erro": "Os valores não podem ser negativos."}

    fator = 1 + perda_percentual / 100.0
    pontos = tomadas + interruptores + pontos_luz

    # Conduíte: do projeto ou estimado por ponto
    conduite_estimado = conduite_m is None
    conduite_base = pontos * CONDUITE_POR_PONTO_M if conduite_estimado else conduite_m
    conduite_total = conduite_base * fator
    rolos_conduite = math.ceil(conduite_total / ROLO_CONDUITE_M - 1e-9) if conduite_total > 0 else 0

    # Fios: cada bitola do projeto, ou estimada por ponto
    fios = {}
    for bitola in BITOLAS_FIO:
        if bitola in fios_m:
            base = fios_m[bitola]
        else:
            base = (tomadas * FIO_POR_TOMADA_M.get(bitola, 0.0)
                    + interruptores * FIO_POR_INTERRUPTOR_M.get(bitola, 0.0)
                    + pontos_luz * FIO_POR_LUZ_M.get(bitola, 0.0))
        total = base * fator
        if total > 0:
            fios[bitola] = {
                "metros": round(total, 1),
                "rolos": math.ceil(total / ROLO_FIO_M - 1e-9),
                "do_projeto": bitola in fios_m,
            }

    return {
        "tomadas": tomadas,
        "interruptores": interruptores,
        "pontos_luz": pontos_luz,
        "perda_percentual": perda_percentual,
        "conduite_estimado": conduite_estimado,
        "conduite_m": round(conduite_total, 1),
        "rolos_conduite": rolos_conduite,
        "fios": fios,
        "caixas_4x2": tomadas + interruptores,
        "caixas_octogonais": pontos_luz,
    }