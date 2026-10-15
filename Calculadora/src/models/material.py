from dataclasses import dataclass, asdict

PRECOS_POR_ESTADO = {
    "SP": {"cimento": 36.00, "cal": 18.00, "areia": 110.00, "pedra": 120.00, "aco": 9.50},
    "RJ": {"cimento": 38.00, "cal": 19.50, "areia": 125.00, "pedra": 130.00, "aco": 10.00},
    "MG": {"cimento": 34.00, "cal": 17.00, "areia": 95.00, "pedra": 105.00, "aco": 9.20},
    "BA": {"cimento": 39.00, "cal": 21.00, "areia": 130.00, "pedra": 135.00, "aco": 10.20},
    "PR": {"cimento": 33.00, "cal": 16.50, "areia": 90.00, "pedra": 100.00, "aco": 9.00},
    "CE": {"cimento": 40.00, "cal": 22.00, "areia": 135.00, "pedra": 140.00, "aco": 10.50},
    "US-CA": {"cimento": 12.00, "cal": 8.00, "areia": 45.00, "pedra": 50.00, "aco": 2.50},
    "US-TX": {"cimento": 10.00, "cal": 7.00, "areia": 38.00, "pedra": 42.00, "aco": 2.20},
}

@dataclass
class TabelaPrecos:
    estado: str = "SP"
    moeda: str = "R$"
    cimento_50kg: float = 36.00
    cal_20kg: float = 18.00
    areia_m3: float = 110.00
    pedra_m3: float = 120.00
    aco_kg: float = 9.50
    tijolo_unitario: float = 1.20
    argamassa_20kg: float = 22.00
    rejunte_kg: float = 8.50

    def carregar_estado(self, uf: str, moeda: str = "R$"):
        self.estado = uf
        self.moeda = moeda
        if uf in PRECOS_POR_ESTADO:
            dados = PRECOS_POR_ESTADO[uf]
            self.cimento_50kg = dados["cimento"]
            self.cal_20kg = dados["cal"]
            self.areia_m3 = dados["areia"]
            self.pedra_m3 = dados["pedra"]
            self.aco_kg = dados.get("aco", 9.50)

    def para_dicionario(self) -> dict:
        return asdict(self)