"""
Traços (proporções em VOLUME) de concreto e de massa (argamassa).

Este é o único lugar onde os traços e as constantes de conversão ficam.
Para incluir/remover um traço, edite as tabelas abaixo; as telas e os
cálculos leem daqui.

ATENÇÃO (conferir na revisão dos cálculos): FATOR_VOLUME_APARENTE_CONCRETO e as
densidades são premissas de trabalho, não valores validados.
"""

# --- CONCRETO: cimento : areia : pedra ------------------------------------
TRACOS_CONCRETO = {
    "1:2:3":   {"cimento": 1.0, "areia": 2.0, "pedra": 3.0},
    "1:3:3":   {"cimento": 1.0, "areia": 3.0, "pedra": 3.0},
    "1:4:3":   {"cimento": 1.0, "areia": 4.0, "pedra": 3.0},
    "1.5:5:5": {"cimento": 1.5, "areia": 5.0, "pedra": 5.0},
}
TRACO_CONCRETO_PADRAO = "1:2:3"

# --- MASSA (assentamento / reboco): cimento : cal : areia -----------------
# Usada nas abas de Paredes, Reboco e Contrapiso (valores do app antigo).
TRACOS_MASSA = {
    "1:0.5:6": {"cimento": 1.0, "cal": 0.5, "areia": 6.0},
    "1.5:1:8": {"cimento": 1.5, "cal": 1.0, "areia": 8.0},
    "1:0:3":   {"cimento": 1.0, "cal": 0.0, "areia": 3.0},
    "1.5:0:4": {"cimento": 1.5, "cal": 0.0, "areia": 4.0},
}
TRACO_MASSA_PADRAO = "1:0.5:6"

# --- Constantes de conversão (premissas) ----------------------------------
DENSIDADE_CIMENTO = 1500.0   # kg/m3 (aparente)
DENSIDADE_CAL = 1100.0       # kg/m3 (aparente)
SACO_CIMENTO_KG = 50.0
SACO_CAL_KG = 20.0

# m3 de material solto (cimento + areia + pedra) necessários para 1 m3 de concreto
FATOR_VOLUME_APARENTE_CONCRETO = 1.5


def consumo_concreto_por_m3(traco: str):
    """Materiais para 1 m3 de concreto no traço informado.

    Retorna None se o traço não existir.
    """
    partes = TRACOS_CONCRETO.get(traco)
    if partes is None:
        return None

    total_partes = partes["cimento"] + partes["areia"] + partes["pedra"]
    vol_cimento = FATOR_VOLUME_APARENTE_CONCRETO * partes["cimento"] / total_partes
    vol_areia = FATOR_VOLUME_APARENTE_CONCRETO * partes["areia"] / total_partes
    vol_pedra = FATOR_VOLUME_APARENTE_CONCRETO * partes["pedra"] / total_partes

    return {
        "sacos_cimento": vol_cimento * DENSIDADE_CIMENTO / SACO_CIMENTO_KG,
        "areia_m3": vol_areia,
        "pedra_m3": vol_pedra,
    }