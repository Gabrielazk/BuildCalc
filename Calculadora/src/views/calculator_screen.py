"""Tela de cálculo com as abas (Brocas, Baldrame, Paredes...)."""
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from kivy.clock import Clock
from kivymd.uix.button import (
    MDButton,
    MDButtonText,
    MDButtonIcon,
    MDIconButton,
)
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogHeadlineText,
    MDDialogSupportingText,
    MDDialogButtonContainer,
)
from src.calculators.brocas import (
    calcular_brocas,
    BITOLAS_LONGITUDINAL,
    BITOLA_PADRAO,
    ESPACAMENTO_ESTRIBO_PADRAO_CM,
)
from src.calculators.baldrame import calcular_baldrame, PERDA_PADRAO_BALDRAME, PRECO_LATA_IMPERM
from src.calculators.reboco import (
    calcular_reboco,
    ESPESSURA_PADRAO_CM as ESPESSURA_REBOCO_PADRAO_CM,
    PERDA_PADRAO_REBOCO,
    CHAPISCO_TRACO_RODAPE,
    CHAPISCO_ESPESSURA_CM,
)
from src.calculators.contrapiso import calcular_contrapiso, PERDA_PADRAO_CONTRAPISO
from src.calculators.revestimento import (
    calcular_piso,
    calcular_azulejo,
    PERDA_PADRAO_REVESTIMENTO,
    TIPOS_ARGAMASSA,
    ARGAMASSA_PADRAO_PISO,
    ARGAMASSA_PADRAO_AZULEJO,
    RODAPE_PECA_M,
    PRECO_PISO_M2,
    PRECO_AZULEJO_M2,
    PRECO_RODAPE_M,
    PRECO_ARGAMASSA_SACO,
)
from src.calculators.laje import (
    calcular_laje,
    TIPOS_LAJE,
    TIPO_LAJE_PADRAO,
    ENCHIMENTOS,
    ENCHIMENTO_PADRAO,
    PERDA_PADRAO_LAJE,
    CAPA_PADRAO_CM,
    PRECO_LAJE_PREMOLDADA_M2,
)
from src.calculators.telhado import (
    calcular_telhado,
    TIPOS_TELHA,
    TIPO_TELHA_PADRAO,
    PERDA_PADRAO_TELHADO,
    INCLINACAO_PADRAO,
    PRECO_TELHA,
    PRECO_CUMEEIRA,
    PRECO_MADEIRA_M,
)
from src.calculators.eletrica import (
    calcular_eletrica,
    BITOLAS_FIO,
    PERDA_PADRAO_ELETRICA,
    PRECO_ROLO_CONDUITE,
    PRECO_ROLO_FIO,
    PRECO_CAIXA_4X2,
    PRECO_CAIXA_OCTOGONAL,
    PRECO_TOMADA,
    PRECO_INTERRUPTOR,
)
from src.calculators.hidraulica import (
    calcular_hidraulica,
    TUBOS,
    BARRA_TUBO_M,
    PERDA_PADRAO_HIDRAULICA,
    PRECO_BARRA_TUBO,
    PRECO_CONEXAO,
    PRECO_REGISTRO,
)
from src.calculators.pintura import (
    calcular_pintura,
    DEMAOS_PADRAO,
    PERDA_PADRAO_PINTURA,
    RENDIMENTO_PADRAO_M2_L,
    TIPOS_MASSA,
    PRECO_TINTA,
    PRECO_BALDE_MASSA,
)
from src.calculators.esquadrias import (
    calcular_esquadrias,
    TIPOS_ESQUADRIA,
    TIPO_ESQUADRIA_PADRAO,
    MATERIAIS,
    MATERIAL_PADRAO,
    PRECO_TUBO_ESPUMA,
    PRECO_PARAFUSO,
    PRECO_SACO_ARGAMASSA_FIXACAO,
)
from src.calculators.rejunte import (
    calcular_rejunte,
    PERDA_PADRAO_REJUNTE,
    ESPESSURA_PADRAO_MM,
    PRECO_LATA_1KG,
    PRECO_LATA_2KG,
)
from src.calculators.paredes import (
    calcular_paredes,
    TIJOLOS,
    TIJOLO_PADRAO,
    ASSENTAMENTOS,
    ASSENTAMENTO_PADRAO,
    JUNTA_PADRAO_CM,
    QUEBRA_PADRAO_PERCENTUAL,
)
from src.calculators.tracos import (
    TRACOS_CONCRETO,
    TRACO_CONCRETO_PADRAO,
    TRACOS_MASSA,
    TRACO_MASSA_PADRAO,
)
from kivymd.uix.widget import MDWidget
from src.views.comum import CONFIG_APP, TABELA_PRECOS_GLOBAL, ORCAMENTO_FINAL, txt, fmt_moeda, fmt_num


# --- TELA DE CÁLCULO COM ABAS (Navegação Interna) ---
# Ordem das abas no fluxo (botão Próximo). Aba nova entra aqui.
# Etapas do fluxo, na ordem da obra, com as abas de cada uma. Aba nova entra na etapa dela.
ETAPAS = [
    ("estrutura", ["brocas", "baldrame", "paredes", "laje", "telhado"]),
    ("instalacoes", ["eletrica", "hidraulica"]),
    ("acabamento", ["contrapiso", "reboco", "piso", "azulejo", "rejunte", "pintura", "esquadrias"]),
]
# Todas as abas em sequência (é a ordem dos botões Anterior / Próximo)
ABAS_ORDEM = [aba for _, abas in ETAPAS for aba in abas]


def etapa_da_aba(aba):
    """Posição (0, 1, 2) e nome da etapa de uma aba."""
    for indice, (etapa, abas) in enumerate(ETAPAS):
        if aba in abas:
            return indice, etapa
    return 0, ETAPAS[0][0]

# Campos de texto que cada aba guarda (chave usada no estado e no Histórico)
CAMPOS_ABA = {
    "brocas": ["qtd", "prof", "diam", "perda", "barras", "esp_estribo", "mo"],
    "baldrame": ["comp", "larg", "alt", "perda", "mo", "barras", "esp_estribo"],
    "paredes": ["area", "vaos", "junta", "quebra"],
    "contrapiso": ["area", "esp", "perda"],
    "reboco": ["area", "vaos", "esp", "perda"],
    "piso": ["area", "larg", "alt", "caixa", "perda", "rodape"],
    "azulejo": ["area", "larg", "alt", "vaos", "caixa", "perda"],
    "rejunte": ["area", "larg", "alt", "junta", "esp", "perda"],
    "laje": ["area", "capa", "esp", "perda"],
    "telhado": ["area", "incl", "cumeeira", "perda"],
    "eletrica": ["tomadas", "interruptores", "luzes", "conduite", "fio1.5", "fio2.5", "fio4", "fio6", "perda"],
    "hidraulica": ["fria", "quente", "esgoto", "tubo_fria", "tubo_quente", "tubo_esg40", "tubo_esg100", "perda"],
    "pintura": ["parede", "teto", "demaos", "rend", "perda"],
    "esquadrias": ["qtd", "larg", "alt"],  # campos do formulário "Nova porta ou janela"; a lista fica em self.esquadrias_itens
}
# Se algum destes tiver texto, a aba conta como preenchida (aba em branco é ignorada)
CAMPOS_INICIAIS = {
    "brocas": ["qtd", "prof", "diam", "barras", "mo"],
    "baldrame": ["comp", "larg", "alt", "barras", "mo"],
    "paredes": ["area", "vaos"],
    "contrapiso": ["area", "esp"],
    "reboco": ["area", "vaos"],
    "piso": ["area", "larg", "alt"],
    "azulejo": ["area", "larg", "alt"],
    "rejunte": ["area", "larg", "alt", "junta"],
    "laje": ["area", "esp"],
    "telhado": ["area", "cumeeira"],
    "eletrica": ["tomadas", "interruptores", "luzes", "conduite", "fio1.5", "fio2.5", "fio4", "fio6"],
    "hidraulica": ["fria", "quente", "esgoto", "tubo_fria", "tubo_quente", "tubo_esg40", "tubo_esg100"],
    "pintura": ["parede", "teto"],
    "esquadrias": ["qtd", "larg", "alt"],
}


class CalculatorScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "calculator"
        self.md_bg_color = self.theme_cls.backgroundColor
        self.reiniciar(montar=False)

        self.layout_principal = MDBoxLayout(orientation="vertical", padding="16dp", spacing="12dp")
        self.add_widget(self.layout_principal)
        self.montar_tela()

    def reiniciar(self, montar=True):
        """Nova obra: apaga os dados de todas as abas e volta aos valores padrão."""
        self.aba_atual = ABAS_ORDEM[0]
        self.origem = "home"
        self.modo_somente_leitura = False
        self.estado_abas = {}        # texto digitado em cada aba
        self.textos_resultado = {}   # último resultado mostrado em cada aba
        self.traco = {"brocas": TRACO_CONCRETO_PADRAO, "baldrame": TRACO_CONCRETO_PADRAO, "paredes": TRACO_MASSA_PADRAO, "contrapiso": TRACO_CONCRETO_PADRAO, "reboco": TRACO_MASSA_PADRAO, "laje": TRACO_CONCRETO_PADRAO}
        self.tijolo = {"paredes": TIJOLO_PADRAO}
        self.assent = {"paredes": ASSENTAMENTO_PADRAO}
        self.bitola = {"brocas": BITOLA_PADRAO, "baldrame": BITOLA_PADRAO}
        self.imperm = {"baldrame": False}
        self.dois_lados = {"reboco": False}
        self.chapisco = {"reboco": False}
        self.argamassa = {"piso": ARGAMASSA_PADRAO_PISO, "azulejo": ARGAMASSA_PADRAO_AZULEJO}
        self.laje_tipo = TIPO_LAJE_PADRAO
        self.laje_enchimento = ENCHIMENTO_PADRAO
        self.telha_tipo = TIPO_TELHA_PADRAO
        self.madeiramento = {"telhado": False}
        self.selador = {"pintura": False}
        self.fundo = {"pintura": False}
        self.massa_tipo = "nenhuma"
        self.esquadrias_itens = []   # lista de portas e janelas da aba Esquadrias
        self.esq_tipo = TIPO_ESQUADRIA_PADRAO
        self.esq_material = MATERIAL_PADRAO
        self.esq_fixacao = {"espuma": False, "parafusos": False, "argamassa": False}
        self._campos = {}            # campos da aba aberta no momento
        self._botoes_traco = {}
        self._botoes_bitola = {}
        self._botoes_imperm = {}
        self._botoes_sn = {}
        self._botoes_arg = {}
        self._botoes_tijolo = {}
        self._botoes_assent = {}
        self._lbl_resultado = None
        self.menu_ativo = None
        self.dialog_ajuda = None
        self.dialog_limpar = None
        if montar:
            self.montar_tela()

    def montar_tela(self):
        self.layout_principal.clear_widgets()

        # --- TOPO (Botão Voltar + Título) ---
        topo = MDBoxLayout(size_hint_y=None, height="40dp", spacing="10dp")
        self.btn_voltar = MDButton(MDButtonText(text=txt("btn_voltar")), on_release=self.voltar_home)
        self.titulo_topo = MDLabel(
            text=f"{txt('titulo_calculadora')} ({CONFIG_APP['estado']})",
            font_style="Title",
            role="medium",
            bold=True,
            theme_text_color="Primary"
        )
        topo.add_widget(self.btn_voltar)
        topo.add_widget(self.titulo_topo)
        self.layout_principal.add_widget(topo)

        # --- ETAPAS (Estrutura, Instalações, Acabamento): a etapa atual fica destacada ---
        self.rolagem_etapas = MDScrollView(do_scroll_x=True, do_scroll_y=False, bar_width=0, size_hint_y=None, height="48dp")
        self.faixa_etapas = MDBoxLayout(size_hint_x=None, spacing="8dp")
        self.faixa_etapas.bind(minimum_width=self.faixa_etapas.setter("width"))
        self.rolagem_etapas.add_widget(self.faixa_etapas)
        self.layout_principal.add_widget(self.rolagem_etapas)

        # --- ABAS DA ETAPA ATUAL + AJUDA "?": a aba aberta fica destacada ---
        box_tabs = MDBoxLayout(size_hint_y=None, height="48dp", spacing="8dp")

        # As abas ficam numa faixa que rola para o lado (cabem muitas abas em telas pequenas)
        self.faixa_abas = MDBoxLayout(size_hint_x=None, spacing="8dp")
        self.faixa_abas.bind(minimum_width=self.faixa_abas.setter("width"))
        self.rolagem_abas = MDScrollView(do_scroll_x=True, do_scroll_y=False, bar_width=0)
        self.rolagem_abas.add_widget(self.faixa_abas)
        box_tabs.add_widget(self.rolagem_abas)
        self.btn_ajuda = MDIconButton(
            icon="help-circle-outline",
            pos_hint={"center_y": 0.5},
            on_release=self.abrir_ajuda
        )
        box_tabs.add_widget(self.btn_ajuda)
        self.layout_principal.add_widget(box_tabs)

        # --- ÁREA DINÂMICA (Conteúdo das Abas) ---
        self.container_conteudo = MDBoxLayout(orientation="vertical")
        self.layout_principal.add_widget(self.container_conteudo)

        # Reabre a aba que estava ativa (brocas por padrão)
        self.trocar_aba(self.aba_atual)

    def atualizar_interface(self):
        self.montar_tela()

    # ==========================================
    # BARRAS DE ETAPAS E ABAS (destaque: botão preenchido = onde a pessoa está)
    # ==========================================
    def _atualizar_barras(self):
        indice_etapa, _ = etapa_da_aba(self.aba_atual)

        self.faixa_etapas.clear_widgets()
        for indice, (etapa, abas) in enumerate(ETAPAS):
            self.faixa_etapas.add_widget(MDButton(
                MDButtonText(text=f"{indice + 1}. {txt('etapa_' + etapa)}"),
                style="filled" if indice == indice_etapa else "outlined",
                on_release=lambda x, a=abas[0]: self.trocar_aba(a)  # pula para a 1ª aba da etapa
            ))

        self.faixa_abas.clear_widgets()
        botao_atual = None
        for aba in ETAPAS[indice_etapa][1]:
            botao = MDButton(
                MDButtonText(text=txt(f"aba_{aba}")),
                style="filled" if aba == self.aba_atual else "outlined",
                on_release=lambda x, a=aba: self.trocar_aba(a)
            )
            if aba == self.aba_atual:
                botao_atual = botao
            self.faixa_abas.add_widget(botao)

        # Rola a faixa até a aba aberta (para ela não ficar escondida no canto)
        if botao_atual is not None:
            Clock.schedule_once(lambda dt: self.rolagem_abas.scroll_to(botao_atual, padding=dp(8), animate=False), 0)

    # ==========================================
    # ESTADO DE CADA ABA (não perde o que foi digitado ao trocar de aba)
    # ==========================================
    def _capturar_estado(self):
        if not self._campos:
            return
        self.estado_abas[self.aba_atual] = {chave: campo.text for chave, campo in self._campos.items()}

    def _restaurar_estado(self):
        estado = self.estado_abas.get(self.aba_atual, {})
        for chave, campo in self._campos.items():
            if chave in estado:
                campo.text = estado[chave]
        texto = self.textos_resultado.get(self.aba_atual)
        if texto and self._lbl_resultado is not None:
            self._lbl_resultado.text = texto

    def trocar_aba(self, aba_nome):
        self._capturar_estado()
        self.aba_atual = aba_nome
        self._campos = {}
        self.container_conteudo.clear_widgets()
        self._atualizar_barras()

        if aba_nome == "brocas":
            self.container_conteudo.add_widget(self.montar_conteudo_brocas())
        elif aba_nome == "baldrame":
            self.container_conteudo.add_widget(self.montar_conteudo_baldrame())
        elif aba_nome == "paredes":
            self.container_conteudo.add_widget(self.montar_conteudo_paredes())
        elif aba_nome == "contrapiso":
            self.container_conteudo.add_widget(self.montar_conteudo_contrapiso())
        elif aba_nome == "reboco":
            self.container_conteudo.add_widget(self.montar_conteudo_reboco())
        elif aba_nome in ("piso", "azulejo"):
            self.container_conteudo.add_widget(self.montar_conteudo_ceramica(aba_nome))
        elif aba_nome == "rejunte":
            self.container_conteudo.add_widget(self.montar_conteudo_rejunte())
        elif aba_nome == "laje":
            self.container_conteudo.add_widget(self.montar_conteudo_laje())
        elif aba_nome == "telhado":
            self.container_conteudo.add_widget(self.montar_conteudo_telhado())
        elif aba_nome == "eletrica":
            self.container_conteudo.add_widget(self.montar_conteudo_eletrica())
        elif aba_nome == "hidraulica":
            self.container_conteudo.add_widget(self.montar_conteudo_hidraulica())
        elif aba_nome == "pintura":
            self.container_conteudo.add_widget(self.montar_conteudo_pintura())
        elif aba_nome == "esquadrias":
            self.container_conteudo.add_widget(self.montar_conteudo_esquadrias())

        self._restaurar_estado()

    # ==========================================
    # CONTEÚDO DA ABA 1: BROCAS
    # ==========================================
    def montar_conteudo_brocas(self):
        scroll = MDScrollView()
        box_form = MDBoxLayout(orientation="vertical", spacing="16dp", padding="8dp", size_hint_y=None)
        box_form.bind(minimum_height=box_form.setter('height'))
        ro = self.modo_somente_leitura

        # --- Obrigatórios ---
        self.lbl_obrigatorio = MDLabel(text=txt("secao_dimensoes"), font_style="Title", role="small", bold=True, theme_text_color="Primary")
        self.in_qtd = MDTextField(MDTextFieldHintText(text=txt("hint_qtd")), mode="outlined", write_tab=False, readonly=ro)
        self.in_prof = MDTextField(MDTextFieldHintText(text=txt("hint_prof")), mode="outlined", write_tab=False, readonly=ro)
        self.in_diam = MDTextField(MDTextFieldHintText(text=txt("hint_diam")), mode="outlined", write_tab=False, readonly=ro)
        box_form.add_widget(self.lbl_obrigatorio)
        box_form.add_widget(self.in_qtd)
        box_form.add_widget(self.in_diam)
        box_form.add_widget(self.in_prof)

        # --- Opcionais (já vêm preenchidos com valores padrão; os rótulos dizem "opcional") ---
        self._montar_seletor_traco(box_form, "brocas")

        self.in_perda = MDTextField(MDTextFieldHintText(text=txt("hint_perda")), text="10", mode="outlined", write_tab=False, readonly=ro)
        self.in_mo = MDTextField(MDTextFieldHintText(text=txt("hint_mo")), mode="outlined", write_tab=False, readonly=ro)
        box_form.add_widget(self.in_perda)
        box_form.add_widget(self.in_mo)

        # --- Armadura ---
        self.lbl_armadura = MDLabel(text=txt("secao_armadura"), font_style="Title", role="small", bold=True, theme_text_color="Primary")
        self.in_barras = MDTextField(MDTextFieldHintText(text=txt("hint_barras")), mode="outlined", write_tab=False, readonly=ro)
        self.in_esp_estribo = MDTextField(
            MDTextFieldHintText(text=txt("hint_esp_estribo")),
            text=self._texto_campo(ESPACAMENTO_ESTRIBO_PADRAO_CM),
            mode="outlined", write_tab=False, readonly=ro
        )
        box_form.add_widget(self.lbl_armadura)
        box_form.add_widget(self.in_barras)
        self._montar_seletor_bitola(box_form, "brocas")
        box_form.add_widget(self.in_esp_estribo)

        self._campos = {
            "qtd": self.in_qtd, "prof": self.in_prof, "diam": self.in_diam,
            "perda": self.in_perda, "mo": self.in_mo,
            "barras": self.in_barras, "esp_estribo": self.in_esp_estribo,
        }

        if not ro:
            self.btn_calcular = MDButton(MDButtonText(text=txt("btn_calcular")), pos_hint={"center_x": 0.5}, on_release=self.executar_calculo)
            box_form.add_widget(self.btn_calcular)

        box_resultado = MDBoxLayout(orientation="vertical", spacing="12dp", padding=("0dp", "16dp", "0dp", "0dp"), size_hint_y=None)
        box_resultado.bind(minimum_height=box_resultado.setter('height'))

        self.lbl_resultado = MDLabel(text=txt("msg_inicial"), theme_text_color="Secondary", size_hint_y=None)
        self.lbl_resultado.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        self._lbl_resultado = self.lbl_resultado
        box_resultado.add_widget(self.lbl_resultado)

        self._montar_botoes_fluxo(box_resultado)

        box_form.add_widget(box_resultado)
        scroll.add_widget(box_form)
        return scroll

    # ==========================================
    # CONTEÚDO DA ABA 2: BALDRAME
    # ==========================================
    def montar_conteudo_baldrame(self):
        scroll = MDScrollView()
        box_form = MDBoxLayout(orientation="vertical", spacing="16dp", padding="8dp", size_hint_y=None)
        box_form.bind(minimum_height=box_form.setter('height'))
        ro = self.modo_somente_leitura

        # --- Obrigatórios ---
        self.lbl_obrigatorio_bal = MDLabel(text=txt("secao_dimensoes"), font_style="Title", role="small", bold=True, theme_text_color="Primary")
        self.in_bal_comp = MDTextField(MDTextFieldHintText(text=txt("hint_comprimento")), mode="outlined", write_tab=False, readonly=ro)
        self.in_bal_larg = MDTextField(MDTextFieldHintText(text=txt("hint_largura")), mode="outlined", write_tab=False, readonly=ro)
        self.in_bal_alt = MDTextField(MDTextFieldHintText(text=txt("hint_altura")), mode="outlined", write_tab=False, readonly=ro)
        box_form.add_widget(self.lbl_obrigatorio_bal)
        box_form.add_widget(self.in_bal_comp)
        box_form.add_widget(self.in_bal_larg)
        box_form.add_widget(self.in_bal_alt)

        # --- Opcionais (já vêm preenchidos com valores padrão; os rótulos dizem "opcional") ---
        self._montar_seletor_traco(box_form, "baldrame")

        self.in_bal_perda = MDTextField(
            MDTextFieldHintText(text=txt("hint_perda_bal")),
            text=self._texto_campo(PERDA_PADRAO_BALDRAME),
            mode="outlined", write_tab=False, readonly=ro
        )
        self.in_bal_mo = MDTextField(MDTextFieldHintText(text=txt("hint_mo")), mode="outlined", write_tab=False, readonly=ro)
        box_form.add_widget(self.in_bal_perda)
        box_form.add_widget(self.in_bal_mo)

        # --- Armadura ---
        self.lbl_armadura_bal = MDLabel(text=txt("secao_armadura"), font_style="Title", role="small", bold=True, theme_text_color="Primary")
        self.in_bal_barras = MDTextField(MDTextFieldHintText(text=txt("hint_barras_bal")), mode="outlined", write_tab=False, readonly=ro)
        self.in_bal_esp_estribo = MDTextField(
            MDTextFieldHintText(text=txt("hint_esp_estribo")),
            text=self._texto_campo(ESPACAMENTO_ESTRIBO_PADRAO_CM),
            mode="outlined", write_tab=False, readonly=ro
        )
        box_form.add_widget(self.lbl_armadura_bal)
        box_form.add_widget(self.in_bal_barras)
        self._montar_seletor_bitola(box_form, "baldrame")
        box_form.add_widget(self.in_bal_esp_estribo)

        # --- Impermeabilização (Sim / Não) ---
        self._montar_seletor_imperm(box_form, "baldrame")

        self._campos = {
            "comp": self.in_bal_comp, "larg": self.in_bal_larg, "alt": self.in_bal_alt,
            "perda": self.in_bal_perda, "mo": self.in_bal_mo,
            "barras": self.in_bal_barras, "esp_estribo": self.in_bal_esp_estribo,
        }

        if not ro:
            self.btn_calc_bal = MDButton(MDButtonText(text=txt("btn_calcular")), pos_hint={"center_x": 0.5}, on_release=self.executar_calculo)
            box_form.add_widget(self.btn_calc_bal)

        box_res = MDBoxLayout(orientation="vertical", spacing="12dp", padding=("0dp", "16dp", "0dp", "0dp"), size_hint_y=None)
        box_res.bind(minimum_height=box_res.setter('height'))

        self.lbl_res_baldrame = MDLabel(text=txt("msg_inicial"), theme_text_color="Secondary", size_hint_y=None)
        self.lbl_res_baldrame.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        self._lbl_resultado = self.lbl_res_baldrame
        box_res.add_widget(self.lbl_res_baldrame)

        self._montar_botoes_fluxo(box_res)

        box_form.add_widget(box_res)
        scroll.add_widget(box_form)
        return scroll

    # ==========================================
    # CONTEÚDO DA ABA 3: PAREDES
    # ==========================================
    def montar_conteudo_paredes(self):
        scroll = MDScrollView()
        box_form = MDBoxLayout(orientation="vertical", spacing="16dp", padding="8dp", size_hint_y=None)
        box_form.bind(minimum_height=box_form.setter('height'))
        ro = self.modo_somente_leitura

        # --- Obrigatórios ---
        self.lbl_obrigatorio_par = MDLabel(text=txt("secao_dimensoes"), font_style="Title", role="small", bold=True, theme_text_color="Primary")
        self.in_par_area = MDTextField(MDTextFieldHintText(text=txt("hint_area_parede")), mode="outlined", write_tab=False, readonly=ro)
        box_form.add_widget(self.lbl_obrigatorio_par)
        box_form.add_widget(self.in_par_area)
        self._montar_seletor_tijolo(box_form, "paredes")
        self._montar_seletor_assent(box_form, "paredes")

        # --- Opcionais (já vêm preenchidos com valores padrão; os rótulos dizem "opcional") ---
        self.in_par_vaos = MDTextField(MDTextFieldHintText(text=txt("hint_vaos")), mode="outlined", write_tab=False, readonly=ro)
        self.in_par_junta = MDTextField(
            MDTextFieldHintText(text=txt("hint_junta")),
            text=self._texto_campo(JUNTA_PADRAO_CM), mode="outlined", write_tab=False, readonly=ro
        )
        self.in_par_quebra = MDTextField(
            MDTextFieldHintText(text=txt("hint_quebra")),
            text=self._texto_campo(QUEBRA_PADRAO_PERCENTUAL), mode="outlined", write_tab=False, readonly=ro
        )
        box_form.add_widget(self.in_par_vaos)
        box_form.add_widget(self.in_par_junta)
        box_form.add_widget(self.in_par_quebra)
        self._montar_seletor_traco(box_form, "paredes")

        self._campos = {
            "area": self.in_par_area, "vaos": self.in_par_vaos,
            "junta": self.in_par_junta, "quebra": self.in_par_quebra,
        }

        if not ro:
            self.btn_calc_par = MDButton(MDButtonText(text=txt("btn_calcular")), pos_hint={"center_x": 0.5}, on_release=self.executar_calculo)
            box_form.add_widget(self.btn_calc_par)

        box_res = MDBoxLayout(orientation="vertical", spacing="12dp", padding=("0dp", "16dp", "0dp", "0dp"), size_hint_y=None)
        box_res.bind(minimum_height=box_res.setter('height'))

        self.lbl_res_paredes = MDLabel(text=txt("msg_inicial"), theme_text_color="Secondary", size_hint_y=None)
        self.lbl_res_paredes.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        self._lbl_resultado = self.lbl_res_paredes
        box_res.add_widget(self.lbl_res_paredes)

        self._montar_botoes_fluxo(box_res)

        box_form.add_widget(box_res)
        scroll.add_widget(box_form)
        return scroll

    # ==========================================
    # CONTEÚDO DA ABA 4: CONTRAPISO
    # ==========================================
    def montar_conteudo_contrapiso(self):
        scroll = MDScrollView()
        box_form = MDBoxLayout(orientation="vertical", spacing="16dp", padding="8dp", size_hint_y=None)
        box_form.bind(minimum_height=box_form.setter('height'))
        ro = self.modo_somente_leitura

        # --- Obrigatórios ---
        self.lbl_obrigatorio_con = MDLabel(text=txt("secao_dimensoes"), font_style="Title", role="small", bold=True, theme_text_color="Primary")
        self.in_con_area = MDTextField(MDTextFieldHintText(text=txt("hint_area_contrapiso")), mode="outlined", write_tab=False, readonly=ro)
        self.in_con_esp = MDTextField(MDTextFieldHintText(text=txt("hint_esp_contrapiso")), mode="outlined", write_tab=False, readonly=ro)
        box_form.add_widget(self.lbl_obrigatorio_con)
        box_form.add_widget(self.in_con_area)
        box_form.add_widget(self.in_con_esp)

        # --- Opcionais (já vêm preenchidos com valores padrão; os rótulos dizem "opcional") ---
        self._montar_seletor_traco(box_form, "contrapiso")
        self.in_con_perda = MDTextField(
            MDTextFieldHintText(text=txt("hint_perda_bal")),
            text=self._texto_campo(PERDA_PADRAO_CONTRAPISO), mode="outlined", write_tab=False, readonly=ro
        )
        box_form.add_widget(self.in_con_perda)

        self._campos = {"area": self.in_con_area, "esp": self.in_con_esp, "perda": self.in_con_perda}

        if not ro:
            self.btn_calc_con = MDButton(MDButtonText(text=txt("btn_calcular")), pos_hint={"center_x": 0.5}, on_release=self.executar_calculo)
            box_form.add_widget(self.btn_calc_con)

        box_res = MDBoxLayout(orientation="vertical", spacing="12dp", padding=("0dp", "16dp", "0dp", "0dp"), size_hint_y=None)
        box_res.bind(minimum_height=box_res.setter('height'))

        self.lbl_res_contrapiso = MDLabel(text=txt("msg_inicial"), theme_text_color="Secondary", size_hint_y=None)
        self.lbl_res_contrapiso.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        self._lbl_resultado = self.lbl_res_contrapiso
        box_res.add_widget(self.lbl_res_contrapiso)

        self._montar_botoes_fluxo(box_res)

        box_form.add_widget(box_res)
        scroll.add_widget(box_form)
        return scroll

    # ==========================================
    # CONTEÚDO DA ABA 5: REBOCO
    # ==========================================
    def montar_conteudo_reboco(self):
        scroll = MDScrollView()
        box_form = MDBoxLayout(orientation="vertical", spacing="16dp", padding="8dp", size_hint_y=None)
        box_form.bind(minimum_height=box_form.setter('height'))
        ro = self.modo_somente_leitura

        # --- Obrigatórios (a espessura e o traço já vêm com valor padrão) ---
        self.lbl_obrigatorio_reb = MDLabel(text=txt("secao_dimensoes"), font_style="Title", role="small", bold=True, theme_text_color="Primary")
        self.in_reb_area = MDTextField(MDTextFieldHintText(text=txt("hint_area_reboco")), mode="outlined", write_tab=False, readonly=ro)
        self.in_reb_esp = MDTextField(
            MDTextFieldHintText(text=txt("hint_esp_reboco")),
            text=self._texto_campo(ESPESSURA_REBOCO_PADRAO_CM), mode="outlined", write_tab=False, readonly=ro
        )
        box_form.add_widget(self.lbl_obrigatorio_reb)
        box_form.add_widget(self.in_reb_area)
        box_form.add_widget(self.in_reb_esp)
        self._montar_seletor_traco(box_form, "reboco")

        # --- Opcionais ---
        self.in_reb_vaos = MDTextField(MDTextFieldHintText(text=txt("hint_vaos")), mode="outlined", write_tab=False, readonly=ro)
        self.in_reb_perda = MDTextField(
            MDTextFieldHintText(text=txt("hint_perda")),
            text=self._texto_campo(PERDA_PADRAO_REBOCO), mode="outlined", write_tab=False, readonly=ro
        )
        box_form.add_widget(self.in_reb_vaos)
        box_form.add_widget(self.in_reb_perda)
        self._montar_sim_nao(box_form, txt("label_dois_lados"), self.dois_lados, "reboco", "dois_lados")
        self._montar_sim_nao(box_form, txt("label_chapisco"), self.chapisco, "reboco", "chapisco")

        self._campos = {
            "area": self.in_reb_area, "vaos": self.in_reb_vaos,
            "esp": self.in_reb_esp, "perda": self.in_reb_perda,
        }

        if not ro:
            self.btn_calc_reb = MDButton(MDButtonText(text=txt("btn_calcular")), pos_hint={"center_x": 0.5}, on_release=self.executar_calculo)
            box_form.add_widget(self.btn_calc_reb)

        box_res = MDBoxLayout(orientation="vertical", spacing="12dp", padding=("0dp", "16dp", "0dp", "0dp"), size_hint_y=None)
        box_res.bind(minimum_height=box_res.setter('height'))

        self.lbl_res_reboco = MDLabel(text=txt("msg_inicial"), theme_text_color="Secondary", size_hint_y=None)
        self.lbl_res_reboco.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        self._lbl_resultado = self.lbl_res_reboco
        box_res.add_widget(self.lbl_res_reboco)

        self._montar_botoes_fluxo(box_res)

        box_form.add_widget(box_res)
        scroll.add_widget(box_form)
        return scroll

    # ==========================================
    # CONTEÚDO DAS ABAS PISO E AZULEJO (mesma tela, campos um pouco diferentes)
    # ==========================================
    def montar_conteudo_ceramica(self, aba):
        scroll = MDScrollView()
        box_form = MDBoxLayout(orientation="vertical", spacing="16dp", padding="8dp", size_hint_y=None)
        box_form.bind(minimum_height=box_form.setter('height'))
        ro = self.modo_somente_leitura
        piso = (aba == "piso")

        def campo(hint, texto=""):
            return MDTextField(MDTextFieldHintText(text=hint), text=texto, mode="outlined", write_tab=False, readonly=ro)

        # --- Obrigatórios ---
        box_form.add_widget(MDLabel(text=txt("secao_dimensoes"), font_style="Title", role="small", bold=True, theme_text_color="Primary"))
        self.in_cer_area = campo(txt("hint_area_piso" if piso else "hint_area_azulejo"))
        box_form.add_widget(self.in_cer_area)
        if piso and not ro:
            self._montar_dica_contrapiso(box_form)
        self.in_cer_larg = campo(txt("hint_larg_peca"))
        self.in_cer_alt = campo(txt("hint_alt_peca"))
        box_form.add_widget(self.in_cer_larg)
        box_form.add_widget(self.in_cer_alt)

        # --- Opcionais ---
        self.in_cer_vaos = campo(txt("hint_vaos"))
        self.in_cer_caixa = campo(txt("hint_m2_caixa"))
        self.in_cer_perda = campo(txt("hint_perda"), self._texto_campo(PERDA_PADRAO_REVESTIMENTO))
        if not piso:
            box_form.add_widget(self.in_cer_vaos)
        box_form.add_widget(self.in_cer_caixa)
        box_form.add_widget(self.in_cer_perda)
        self._botoes_arg[aba] = self._montar_dropdown(
            box_form, txt("label_argamassa"), TIPOS_ARGAMASSA, self.argamassa[aba],
            lambda v: self._escolher_argamassa(aba, v)
        )
        self.in_cer_rodape = campo(txt("hint_rodape"))
        if piso:
            box_form.add_widget(self.in_cer_rodape)

        self._campos = {
            "area": self.in_cer_area, "larg": self.in_cer_larg, "alt": self.in_cer_alt,
            "caixa": self.in_cer_caixa, "perda": self.in_cer_perda,
        }
        self._campos["rodape" if piso else "vaos"] = self.in_cer_rodape if piso else self.in_cer_vaos

        if not ro:
            self.btn_calc_cer = MDButton(MDButtonText(text=txt("btn_calcular")), pos_hint={"center_x": 0.5}, on_release=self.executar_calculo)
            box_form.add_widget(self.btn_calc_cer)

        box_res = MDBoxLayout(orientation="vertical", spacing="12dp", padding=("0dp", "16dp", "0dp", "0dp"), size_hint_y=None)
        box_res.bind(minimum_height=box_res.setter('height'))

        self.lbl_res_ceramica = MDLabel(text=txt("msg_inicial"), theme_text_color="Secondary", size_hint_y=None)
        self.lbl_res_ceramica.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        self._lbl_resultado = self.lbl_res_ceramica
        box_res.add_widget(self.lbl_res_ceramica)

        self._montar_botoes_fluxo(box_res)

        box_form.add_widget(box_res)
        scroll.add_widget(box_form)
        return scroll

    def _area_contrapiso_digitada(self):
        """Área já digitada na aba Contrapiso (texto), ou None."""
        texto = ((self.estado_abas.get("contrapiso") or {}).get("area") or "").strip()
        try:
            return texto if texto and self._numero(texto) > 0 else None
        except ValueError:
            return None

    def _montar_dica_contrapiso(self, box_form):
        """Dica do .md: a área do Contrapiso pode ser reaproveitada no Piso (toque para usar)."""
        area = self._area_contrapiso_digitada()
        if not area:
            return
        self.btn_dica_contrapiso = MDButton(
            MDButtonText(text=txt("dica_area_contrapiso").format(area=area)),
            style="text", on_release=lambda x: setattr(self.in_cer_area, "text", area)
        )
        box_form.add_widget(self.btn_dica_contrapiso)

    # ==========================================
    # CONTEÚDO DA ABA LAJE (pré-moldada treliçada ou maciça)
    # ==========================================
    def montar_conteudo_laje(self):
        scroll = MDScrollView()
        box_form = MDBoxLayout(orientation="vertical", spacing="16dp", padding="8dp", size_hint_y=None)
        box_form.bind(minimum_height=box_form.setter('height'))
        ro = self.modo_somente_leitura
        premoldada = (self.laje_tipo == "premoldada")

        def campo(hint, texto=""):
            return MDTextField(MDTextFieldHintText(text=hint), text=texto, mode="outlined", write_tab=False, readonly=ro)

        # Os dois campos de espessura sempre existem (o que foi digitado não se perde ao trocar o tipo),
        # mas só aparece o do tipo escolhido
        self.in_laje_area = campo(txt("hint_area_laje"))
        self.in_laje_capa = campo(txt("hint_capa_laje"), self._texto_campo(CAPA_PADRAO_CM))
        self.in_laje_esp = campo(txt("hint_esp_laje"))
        self.in_laje_perda = campo(txt("hint_perda_bal"), self._texto_campo(PERDA_PADRAO_LAJE))

        # --- Obrigatórios ---
        box_form.add_widget(MDLabel(text=txt("secao_dimensoes"), font_style="Title", role="small", bold=True, theme_text_color="Primary"))
        box_form.add_widget(self.in_laje_area)
        self._botao_laje_tipo = self._montar_dropdown(
            box_form, txt("label_tipo_laje"), TIPOS_LAJE, self.laje_tipo,
            self._escolher_laje_tipo, rotulo=self._rotulo_laje, largura=None
        )
        if not premoldada:
            box_form.add_widget(self.in_laje_esp)

        # --- Opcionais (já vêm com valor padrão) ---
        if premoldada:
            self._botao_laje_ench = self._montar_dropdown(
                box_form, txt("label_enchimento"), ENCHIMENTOS, self.laje_enchimento,
                self._escolher_laje_enchimento, rotulo=self._rotulo_laje, largura=None
            )
            box_form.add_widget(self.in_laje_capa)
        self._montar_seletor_traco(box_form, "laje")
        box_form.add_widget(self.in_laje_perda)

        self._campos = {
            "area": self.in_laje_area, "capa": self.in_laje_capa,
            "esp": self.in_laje_esp, "perda": self.in_laje_perda,
        }

        if not ro:
            self.btn_calc_laje = MDButton(MDButtonText(text=txt("btn_calcular")), pos_hint={"center_x": 0.5}, on_release=self.executar_calculo)
            box_form.add_widget(self.btn_calc_laje)

        box_res = MDBoxLayout(orientation="vertical", spacing="12dp", padding=("0dp", "16dp", "0dp", "0dp"), size_hint_y=None)
        box_res.bind(minimum_height=box_res.setter('height'))

        self.lbl_res_laje = MDLabel(text=txt("msg_inicial"), theme_text_color="Secondary", size_hint_y=None)
        self.lbl_res_laje.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        self._lbl_resultado = self.lbl_res_laje
        box_res.add_widget(self.lbl_res_laje)

        self._montar_botoes_fluxo(box_res)

        box_form.add_widget(box_res)
        scroll.add_widget(box_form)
        return scroll

    @staticmethod
    def _rotulo_laje(chave):
        """Texto na tela para o tipo de laje e o enchimento."""
        return txt(f"opcao_{chave}")

    def _escolher_laje_tipo(self, valor):
        if valor == self.laje_tipo:
            return
        self.laje_tipo = valor
        self.textos_resultado.pop("laje", None)  # o resultado antigo era do outro tipo
        self.trocar_aba("laje")  # remonta a aba mostrando os campos do tipo escolhido

    def _escolher_laje_enchimento(self, valor):
        self.laje_enchimento = valor
        self._botao_laje_ench.text = self._rotulo_laje(valor)

    # ==========================================
    # CONTEÚDO DA ABA TELHADO (telhas, cumeeira e madeiramento)
    # ==========================================
    def montar_conteudo_telhado(self):
        scroll = MDScrollView()
        box_form = MDBoxLayout(orientation="vertical", spacing="16dp", padding="8dp", size_hint_y=None)
        box_form.bind(minimum_height=box_form.setter('height'))
        ro = self.modo_somente_leitura

        def campo(hint, texto=""):
            return MDTextField(MDTextFieldHintText(text=hint), text=texto, mode="outlined", write_tab=False, readonly=ro)

        # --- Obrigatórios ---
        box_form.add_widget(MDLabel(text=txt("secao_dimensoes"), font_style="Title", role="small", bold=True, theme_text_color="Primary"))
        self.in_tel_area = campo(txt("hint_area_telhado"))
        box_form.add_widget(self.in_tel_area)
        self._botao_telha_tipo = self._montar_dropdown(
            box_form, txt("label_tipo_telha"), TIPOS_TELHA, self.telha_tipo,
            self._escolher_telha_tipo, rotulo=self._rotulo_telha, largura=None
        )

        # --- Opcionais (já vêm com valor padrão) ---
        self.in_tel_incl = campo(txt("hint_inclinacao"), self._texto_campo(INCLINACAO_PADRAO[self.telha_tipo]))
        self.in_tel_cumeeira = campo(txt("hint_cumeeira"))
        self.in_tel_perda = campo(txt("hint_perda_bal"), self._texto_campo(PERDA_PADRAO_TELHADO))
        box_form.add_widget(self.in_tel_incl)
        box_form.add_widget(self.in_tel_cumeeira)
        self._montar_sim_nao(box_form, txt("label_madeiramento"), self.madeiramento, "telhado", "madeiramento")
        box_form.add_widget(self.in_tel_perda)

        self._campos = {
            "area": self.in_tel_area, "incl": self.in_tel_incl,
            "cumeeira": self.in_tel_cumeeira, "perda": self.in_tel_perda,
        }

        if not ro:
            self.btn_calc_tel = MDButton(MDButtonText(text=txt("btn_calcular")), pos_hint={"center_x": 0.5}, on_release=self.executar_calculo)
            box_form.add_widget(self.btn_calc_tel)

        box_res = MDBoxLayout(orientation="vertical", spacing="12dp", padding=("0dp", "16dp", "0dp", "0dp"), size_hint_y=None)
        box_res.bind(minimum_height=box_res.setter('height'))

        self.lbl_res_telhado = MDLabel(text=txt("msg_inicial"), theme_text_color="Secondary", size_hint_y=None)
        self.lbl_res_telhado.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        self._lbl_resultado = self.lbl_res_telhado
        box_res.add_widget(self.lbl_res_telhado)

        self._montar_botoes_fluxo(box_res)

        box_form.add_widget(box_res)
        scroll.add_widget(box_form)
        return scroll

    @staticmethod
    def _rotulo_telha(chave):
        return txt(f"opcao_{chave}")

    def _escolher_telha_tipo(self, valor):
        antigo = self.telha_tipo
        self.telha_tipo = valor
        self._botao_telha_tipo.text = self._rotulo_telha(valor)
        # Se a inclinação ainda é a padrão do tipo antigo (ou está vazia), troca pela padrão do tipo novo
        incl_atual = self.in_tel_incl.text.strip()
        if not incl_atual or incl_atual == self._texto_campo(INCLINACAO_PADRAO[antigo]):
            self.in_tel_incl.text = self._texto_campo(INCLINACAO_PADRAO[valor])

    # ==========================================
    # CONTEÚDO DA ABA ELÉTRICA (estimativa por ponto, ou metragens do projeto)
    # ==========================================
    @staticmethod
    def _chave_fio(bitola):
        """1.5 -> 'fio1.5', 4.0 -> 'fio4' (chave do campo no estado e no Histórico)."""
        return f"fio{fmt_num(bitola, 0 if float(bitola).is_integer() else 1).replace(',', '.')}"

    @staticmethod
    def _rotulo_bitola_fio(bitola):
        return fmt_num(bitola, 0 if float(bitola).is_integer() else 1)

    def montar_conteudo_eletrica(self):
        scroll = MDScrollView()
        box_form = MDBoxLayout(orientation="vertical", spacing="16dp", padding="8dp", size_hint_y=None)
        box_form.bind(minimum_height=box_form.setter('height'))
        ro = self.modo_somente_leitura

        def campo(hint, texto=""):
            return MDTextField(MDTextFieldHintText(text=hint), text=texto, mode="outlined", write_tab=False, readonly=ro)

        # --- Obrigatórios ---
        box_form.add_widget(MDLabel(text=txt("secao_quantidades"), font_style="Title", role="small", bold=True, theme_text_color="Primary"))
        self.in_ele_tomadas = campo(txt("hint_tomadas"))
        self.in_ele_interruptores = campo(txt("hint_interruptores"))
        self.in_ele_luzes = campo(txt("hint_luzes"))
        box_form.add_widget(self.in_ele_tomadas)
        box_form.add_widget(self.in_ele_interruptores)
        box_form.add_widget(self.in_ele_luzes)

        # --- Opcionais: metragens de quem já tem o projeto (vazio = o app estima) ---
        box_form.add_widget(MDLabel(text=txt("secao_projeto"), font_style="Title", role="small", bold=True, theme_text_color="Primary"))
        self.in_ele_conduite = campo(txt("hint_conduite"))
        box_form.add_widget(self.in_ele_conduite)
        self._campos = {
            "tomadas": self.in_ele_tomadas, "interruptores": self.in_ele_interruptores,
            "luzes": self.in_ele_luzes, "conduite": self.in_ele_conduite,
        }
        for bitola in BITOLAS_FIO:
            campo_fio = campo(txt("hint_fio").format(b=self._rotulo_bitola_fio(bitola)))
            box_form.add_widget(campo_fio)
            self._campos[self._chave_fio(bitola)] = campo_fio
        self.in_ele_perda = campo(txt("hint_perda"), self._texto_campo(PERDA_PADRAO_ELETRICA))
        box_form.add_widget(self.in_ele_perda)
        self._campos["perda"] = self.in_ele_perda

        if not ro:
            self.btn_calc_ele = MDButton(MDButtonText(text=txt("btn_calcular")), pos_hint={"center_x": 0.5}, on_release=self.executar_calculo)
            box_form.add_widget(self.btn_calc_ele)

        box_res = MDBoxLayout(orientation="vertical", spacing="12dp", padding=("0dp", "16dp", "0dp", "0dp"), size_hint_y=None)
        box_res.bind(minimum_height=box_res.setter('height'))

        self.lbl_res_eletrica = MDLabel(text=txt("msg_inicial"), theme_text_color="Secondary", size_hint_y=None)
        self.lbl_res_eletrica.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        self._lbl_resultado = self.lbl_res_eletrica
        box_res.add_widget(self.lbl_res_eletrica)

        self._montar_botoes_fluxo(box_res)

        box_form.add_widget(box_res)
        scroll.add_widget(box_form)
        return scroll

    # ==========================================
    # CONTEÚDO DA ABA HIDRÁULICA (estimativa por ponto, ou metragens do projeto)
    # ==========================================
    def montar_conteudo_hidraulica(self):
        scroll = MDScrollView()
        box_form = MDBoxLayout(orientation="vertical", spacing="16dp", padding="8dp", size_hint_y=None)
        box_form.bind(minimum_height=box_form.setter('height'))
        ro = self.modo_somente_leitura

        def campo(hint, texto=""):
            return MDTextField(MDTextFieldHintText(text=hint), text=texto, mode="outlined", write_tab=False, readonly=ro)

        self._campos = {}

        # --- Obrigatórios ---
        box_form.add_widget(MDLabel(text=txt("secao_quantidades"), font_style="Title", role="small", bold=True, theme_text_color="Primary"))
        for chave in ("fria", "quente", "esgoto"):
            self._campos[chave] = campo(txt(f"hint_pontos_{chave}"))
            box_form.add_widget(self._campos[chave])

        # --- Opcionais: metragens de quem já tem o projeto (vazio = o app estima) ---
        box_form.add_widget(MDLabel(text=txt("secao_projeto"), font_style="Title", role="small", bold=True, theme_text_color="Primary"))
        for tubo in TUBOS:
            self._campos[f"tubo_{tubo}"] = campo(txt(f"hint_tubo_{tubo}"))
            box_form.add_widget(self._campos[f"tubo_{tubo}"])
        self._campos["perda"] = campo(txt("hint_perda"), self._texto_campo(PERDA_PADRAO_HIDRAULICA))
        box_form.add_widget(self._campos["perda"])

        if not ro:
            self.btn_calc_hid = MDButton(MDButtonText(text=txt("btn_calcular")), pos_hint={"center_x": 0.5}, on_release=self.executar_calculo)
            box_form.add_widget(self.btn_calc_hid)

        box_res = MDBoxLayout(orientation="vertical", spacing="12dp", padding=("0dp", "16dp", "0dp", "0dp"), size_hint_y=None)
        box_res.bind(minimum_height=box_res.setter('height'))

        self.lbl_res_hidraulica = MDLabel(text=txt("msg_inicial"), theme_text_color="Secondary", size_hint_y=None)
        self.lbl_res_hidraulica.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        self._lbl_resultado = self.lbl_res_hidraulica
        box_res.add_widget(self.lbl_res_hidraulica)

        self._montar_botoes_fluxo(box_res)

        box_form.add_widget(box_res)
        scroll.add_widget(box_form)
        return scroll

    @staticmethod
    def _texto_barras(qtd, metros_barra):
        """Ex.: '5 barras de 6 m'."""
        m = fmt_num(metros_barra, 0 if float(metros_barra).is_integer() else 1)
        return f"{qtd} {(txt('un_barra_m') if qtd == 1 else txt('un_barras_m')).format(m=m)}"

    # ==========================================
    # CONTEÚDO DA ABA PINTURA (tinta de parede e de teto + complementos)
    # ==========================================
    def montar_conteudo_pintura(self):
        scroll = MDScrollView()
        box_form = MDBoxLayout(orientation="vertical", spacing="16dp", padding="8dp", size_hint_y=None)
        box_form.bind(minimum_height=box_form.setter('height'))
        ro = self.modo_somente_leitura

        def campo(hint, texto=""):
            return MDTextField(MDTextFieldHintText(text=hint), text=texto, mode="outlined", write_tab=False, readonly=ro)

        # --- Obrigatórios (basta uma das duas áreas) ---
        box_form.add_widget(MDLabel(text=txt("secao_areas"), font_style="Title", role="small", bold=True, theme_text_color="Primary"))
        self.in_pint_parede = campo(txt("hint_area_parede_pint"))
        self.in_pint_teto = campo(txt("hint_area_teto_pint"))
        self.in_pint_demaos = campo(txt("hint_demaos"), self._texto_campo(DEMAOS_PADRAO))
        box_form.add_widget(self.in_pint_parede)
        box_form.add_widget(self.in_pint_teto)
        box_form.add_widget(self.in_pint_demaos)

        # --- Opcionais (já vêm com valor padrão) ---
        self.in_pint_rend = campo(txt("hint_rendimento"), self._texto_campo(RENDIMENTO_PADRAO_M2_L))
        self.in_pint_perda = campo(txt("hint_perda"), self._texto_campo(PERDA_PADRAO_PINTURA))
        box_form.add_widget(self.in_pint_rend)
        self._montar_sim_nao(box_form, txt("label_selador"), self.selador, "pintura", "selador")
        self._botao_massa = self._montar_dropdown(
            box_form, txt("label_massa"), TIPOS_MASSA, self.massa_tipo,
            self._escolher_massa, rotulo=self._rotulo_massa, largura=None
        )
        self._montar_sim_nao(box_form, txt("label_fundo"), self.fundo, "pintura", "fundo")
        box_form.add_widget(self.in_pint_perda)

        self._campos = {
            "parede": self.in_pint_parede, "teto": self.in_pint_teto, "demaos": self.in_pint_demaos,
            "rend": self.in_pint_rend, "perda": self.in_pint_perda,
        }

        if not ro:
            self.btn_calc_pint = MDButton(MDButtonText(text=txt("btn_calcular")), pos_hint={"center_x": 0.5}, on_release=self.executar_calculo)
            box_form.add_widget(self.btn_calc_pint)

        box_res = MDBoxLayout(orientation="vertical", spacing="12dp", padding=("0dp", "16dp", "0dp", "0dp"), size_hint_y=None)
        box_res.bind(minimum_height=box_res.setter('height'))

        self.lbl_res_pintura = MDLabel(text=txt("msg_inicial"), theme_text_color="Secondary", size_hint_y=None)
        self.lbl_res_pintura.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        self._lbl_resultado = self.lbl_res_pintura
        box_res.add_widget(self.lbl_res_pintura)

        self._montar_botoes_fluxo(box_res)

        box_form.add_widget(box_res)
        scroll.add_widget(box_form)
        return scroll

    @staticmethod
    def _rotulo_massa(chave):
        return txt(f"opcao_massa_{chave}")

    def _escolher_massa(self, valor):
        self.massa_tipo = valor
        self._botao_massa.text = self._rotulo_massa(valor)

    @staticmethod
    def _texto_latas_galoes(latas, galoes):
        """Ex.: '2 latas de 18 L e 1 galão de 3,6 L'."""
        partes = []
        if latas:
            partes.append(f"{latas} {txt('un_lata_18') if latas == 1 else txt('un_latas_18')}")
        if galoes:
            partes.append(f"{galoes} {txt('un_galao_36') if galoes == 1 else txt('un_galoes_36')}")
        return f" {txt('un_e')} ".join(partes)

    # ==========================================
    # CONTEÚDO DA ABA ESQUADRIAS (lista de portas e janelas + insumos de fixação)
    # ==========================================
    def montar_conteudo_esquadrias(self):
        scroll = MDScrollView()
        box_form = MDBoxLayout(orientation="vertical", spacing="16dp", padding="8dp", size_hint_y=None)
        box_form.bind(minimum_height=box_form.setter('height'))
        ro = self.modo_somente_leitura

        def campo(hint, texto=""):
            return MDTextField(MDTextFieldHintText(text=hint), text=texto, mode="outlined", write_tab=False, readonly=ro)

        # --- Formulário para adicionar uma porta ou janela (some no modo leitura) ---
        self.in_esq_qtd = campo(txt("hint_qtd_esquadria"))
        self.in_esq_larg = campo(txt("hint_larg_esquadria"))
        self.in_esq_alt = campo(txt("hint_alt_esquadria"))
        if not ro:
            box_form.add_widget(MDLabel(text=txt("secao_nova_esquadria"), font_style="Title", role="small", bold=True, theme_text_color="Primary"))
            self._botao_esq_tipo = self._montar_dropdown(
                box_form, txt("label_tipo_esquadria"), TIPOS_ESQUADRIA, self.esq_tipo,
                self._escolher_esq_tipo, rotulo=self._rotulo_esq_tipo, largura=None
            )
            self._botao_esq_material = self._montar_dropdown(
                box_form, txt("label_material"), MATERIAIS, self.esq_material,
                self._escolher_esq_material, rotulo=self._rotulo_material, largura=None
            )
            box_form.add_widget(self.in_esq_qtd)
            box_form.add_widget(self.in_esq_larg)
            box_form.add_widget(self.in_esq_alt)
            box_form.add_widget(MDButton(
                MDButtonIcon(icon="plus"), MDButtonText(text=txt("btn_adicionar_lista")),
                style="tonal", pos_hint={"center_x": 0.5}, on_release=self._adicionar_esquadria
            ))
        self._campos = {"qtd": self.in_esq_qtd, "larg": self.in_esq_larg, "alt": self.in_esq_alt}

        # --- Lista para cotação (cada item tem um X para remover) ---
        box_form.add_widget(MDLabel(text=txt("secao_lista_esquadrias"), font_style="Title", role="small", bold=True, theme_text_color="Primary"))
        if not self.esquadrias_itens:
            box_form.add_widget(MDLabel(text=txt("msg_lista_vazia"), theme_text_color="Secondary", adaptive_height=True))
        for indice, item in enumerate(self.esquadrias_itens):
            linha = MDBoxLayout(size_hint_y=None, height="48dp", spacing="8dp")
            linha.add_widget(MDLabel(text=self._texto_item_esquadria(item), theme_text_color="Primary"))
            if not ro:
                linha.add_widget(MDIconButton(
                    icon="close", pos_hint={"center_y": 0.5},
                    on_release=lambda x, i=indice: self._remover_esquadria(i)
                ))
            box_form.add_widget(linha)

        # --- Opcionais: insumos de fixação ---
        box_form.add_widget(MDLabel(text=txt("secao_fixacao"), font_style="Title", role="small", bold=True, theme_text_color="Primary"))
        self._montar_sim_nao(box_form, txt("label_espuma"), self.esq_fixacao, "espuma", "fixacao")
        self._montar_sim_nao(box_form, txt("label_parafusos"), self.esq_fixacao, "parafusos", "fixacao")
        self._montar_sim_nao(box_form, txt("label_argamassa_fix"), self.esq_fixacao, "argamassa", "fixacao")

        if not ro:
            self.btn_calc_esq = MDButton(MDButtonText(text=txt("btn_calcular")), pos_hint={"center_x": 0.5}, on_release=self.executar_calculo)
            box_form.add_widget(self.btn_calc_esq)

        box_res = MDBoxLayout(orientation="vertical", spacing="12dp", padding=("0dp", "16dp", "0dp", "0dp"), size_hint_y=None)
        box_res.bind(minimum_height=box_res.setter('height'))

        self.lbl_res_esquadrias = MDLabel(text=txt("msg_inicial"), theme_text_color="Secondary", size_hint_y=None)
        self.lbl_res_esquadrias.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        self._lbl_resultado = self.lbl_res_esquadrias
        box_res.add_widget(self.lbl_res_esquadrias)

        self._montar_botoes_fluxo(box_res)

        box_form.add_widget(box_res)
        scroll.add_widget(box_form)
        return scroll

    @staticmethod
    def _rotulo_esq_tipo(chave):
        return txt(f"opcao_{chave}")

    @staticmethod
    def _rotulo_material(chave):
        return txt(f"opcao_mat_{chave}")

    def _escolher_esq_tipo(self, valor):
        self.esq_tipo = valor
        self._botao_esq_tipo.text = self._rotulo_esq_tipo(valor)

    def _escolher_esq_material(self, valor):
        self.esq_material = valor
        self._botao_esq_material.text = self._rotulo_material(valor)

    @staticmethod
    def _texto_item_esquadria(item):
        """Ex.: '3x Porta 80 x 210 cm (Madeira)'."""
        def n(v):
            return fmt_num(v, 0 if float(v).is_integer() else 1)
        texto = f"{item['qtd']}x {CalculatorScreen._rotulo_esq_tipo(item['tipo'])} {n(item['larg'])} x {n(item['alt'])} cm"
        if item["material"] != MATERIAL_PADRAO:
            texto += f" ({CalculatorScreen._rotulo_material(item['material'])})"
        return texto

    def _adicionar_esquadria(self, instance=None):
        try:
            qtd = int(self.in_esq_qtd.text.strip())
            larg = self._numero(self.in_esq_larg.text)
            alt = self._numero(self.in_esq_alt.text)
        except ValueError:
            self._lbl_resultado.text = txt("msg_erro_num")
            return
        if qtd <= 0 or larg <= 0 or alt <= 0:
            self._lbl_resultado.text = txt("msg_erro_num")
            return

        # Mesmo tipo, material e tamanho: soma na quantidade em vez de repetir a linha
        for item in self.esquadrias_itens:
            if (item["tipo"], item["material"], item["larg"], item["alt"]) == (self.esq_tipo, self.esq_material, larg, alt):
                item["qtd"] += qtd
                break
        else:
            self.esquadrias_itens.append({"tipo": self.esq_tipo, "material": self.esq_material, "qtd": qtd, "larg": larg, "alt": alt})

        for campo in self._campos.values():  # limpa o formulário para a próxima
            campo.text = ""
        self.textos_resultado.pop("esquadrias", None)
        self.trocar_aba("esquadrias")

    def _remover_esquadria(self, indice):
        if 0 <= indice < len(self.esquadrias_itens):
            self.esquadrias_itens.pop(indice)
        self.textos_resultado.pop("esquadrias", None)
        self.trocar_aba("esquadrias")

    # ==========================================
    # CONTEÚDO DA ABA REJUNTE (pode reaproveitar os dados do Piso ou do Azulejo)
    # ==========================================
    def montar_conteudo_rejunte(self):
        scroll = MDScrollView()
        box_form = MDBoxLayout(orientation="vertical", spacing="16dp", padding="8dp", size_hint_y=None)
        box_form.bind(minimum_height=box_form.setter('height'))
        ro = self.modo_somente_leitura

        def campo(hint, texto=""):
            return MDTextField(MDTextFieldHintText(text=hint), text=texto, mode="outlined", write_tab=False, readonly=ro)

        # --- Obrigatórios ---
        box_form.add_widget(MDLabel(text=txt("secao_dimensoes"), font_style="Title", role="small", bold=True, theme_text_color="Primary"))
        self.in_rej_area = campo(txt("hint_area_rejunte"))
        self.in_rej_larg = campo(txt("hint_larg_peca"))
        self.in_rej_alt = campo(txt("hint_alt_peca"))
        self.in_rej_junta = campo(txt("hint_junta_mm"))
        if not ro:
            self._montar_dicas_rejunte(box_form)
        box_form.add_widget(self.in_rej_area)
        box_form.add_widget(self.in_rej_larg)
        box_form.add_widget(self.in_rej_alt)
        box_form.add_widget(self.in_rej_junta)

        # --- Opcionais (já vêm com valor padrão) ---
        self.in_rej_esp = campo(txt("hint_esp_peca"), self._texto_campo(ESPESSURA_PADRAO_MM))
        self.in_rej_perda = campo(txt("hint_perda"), self._texto_campo(PERDA_PADRAO_REJUNTE))
        box_form.add_widget(self.in_rej_esp)
        box_form.add_widget(self.in_rej_perda)

        self._campos = {
            "area": self.in_rej_area, "larg": self.in_rej_larg, "alt": self.in_rej_alt,
            "junta": self.in_rej_junta, "esp": self.in_rej_esp, "perda": self.in_rej_perda,
        }

        if not ro:
            self.btn_calc_rej = MDButton(MDButtonText(text=txt("btn_calcular")), pos_hint={"center_x": 0.5}, on_release=self.executar_calculo)
            box_form.add_widget(self.btn_calc_rej)

        box_res = MDBoxLayout(orientation="vertical", spacing="12dp", padding=("0dp", "16dp", "0dp", "0dp"), size_hint_y=None)
        box_res.bind(minimum_height=box_res.setter('height'))

        self.lbl_res_rejunte = MDLabel(text=txt("msg_inicial"), theme_text_color="Secondary", size_hint_y=None)
        self.lbl_res_rejunte.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        self._lbl_resultado = self.lbl_res_rejunte
        box_res.add_widget(self.lbl_res_rejunte)

        self._montar_botoes_fluxo(box_res)

        box_form.add_widget(box_res)
        scroll.add_widget(box_form)
        return scroll

    def _dados_ceramica_digitados(self, aba):
        """Área (já sem os vãos, no Azulejo), largura e altura digitadas no Piso/Azulejo, ou None."""
        e = self.estado_abas.get(aba) or {}
        try:
            area = self._numero(e.get("area"))
            larg = self._numero(e.get("larg"))
            alt = self._numero(e.get("alt"))
            vaos = self._numero(e.get("vaos"), 0.0) if aba == "azulejo" else 0.0
        except ValueError:
            return None
        area -= vaos
        if area <= 0 or larg <= 0 or alt <= 0:
            return None
        return self._texto_campo(round(area, 2)), self._texto_campo(larg), self._texto_campo(alt)

    def _montar_dicas_rejunte(self, box_form):
        """Dica (só texto): mostra a área e o tamanho da peça já digitados no Piso e no Azulejo."""
        for aba in ("piso", "azulejo"):
            dados = self._dados_ceramica_digitados(aba)
            if not dados:
                continue
            area, larg, alt = dados
            box_form.add_widget(MDLabel(
                text=txt(f"dica_rejunte_{aba}").format(area=area, peca=f"{larg}x{alt}"),
                theme_text_color="Secondary", adaptive_height=True
            ))

    def _escolher_argamassa(self, aba, valor):
        self.argamassa[aba] = valor
        if aba in self._botoes_arg:
            self._botoes_arg[aba].text = valor

    # ==========================================
    # BOTÕES DO FLUXO: Limpar, Anterior (menos na 1ª aba), Próximo (menos na última) e Finalizar
    # (somem no modo leitura)
    # ==========================================
    def _montar_botoes_fluxo(self, box):
        """Limpar e Anterior (menos na 1ª aba); Próximo dentro da etapa; na última aba de cada etapa,
        "Avançar para a próxima etapa" no lugar do Próximo; Finalizar em todas."""
        if self.modo_somente_leitura:
            return
        posicao = ABAS_ORDEM.index(self.aba_atual)
        indice_etapa, _ = etapa_da_aba(self.aba_atual)
        abas_etapa = ETAPAS[indice_etapa][1]
        ultima_da_etapa = (self.aba_atual == abas_etapa[-1])
        ultima_etapa = (indice_etapa == len(ETAPAS) - 1)

        linha = MDBoxLayout(size_hint_y=None, height="48dp", spacing="8dp")
        linha.add_widget(MDWidget())
        self.btn_limpar = MDButton(MDButtonText(text=txt("btn_limpar")), style="outlined", on_release=self.pedir_limpar)
        linha.add_widget(self.btn_limpar)
        if posicao > 0:
            anterior = ABAS_ORDEM[posicao - 1]
            self.btn_anterior = MDButton(MDButtonText(text=txt("btn_anterior")), style="outlined", on_release=lambda x: self.trocar_aba(anterior))
            linha.add_widget(self.btn_anterior)
        if not ultima_da_etapa:
            proxima = ABAS_ORDEM[posicao + 1]
            self.btn_proximo = MDButton(MDButtonText(text=txt("btn_proximo")), style="outlined", on_release=lambda x: self.trocar_aba(proxima))
            linha.add_widget(self.btn_proximo)
        linha.add_widget(MDWidget())
        box.add_widget(linha)

        # Fim da etapa: o botão é maior, então fica numa linha só dele (não cabe ao lado dos outros no celular)
        if ultima_da_etapa and not ultima_etapa:
            primeira_da_proxima = ETAPAS[indice_etapa + 1][1][0]
            self.btn_avancar_etapa = MDButton(
                MDButtonIcon(icon="arrow-right"), MDButtonText(text=txt("btn_avancar_etapa")),
                style="tonal", pos_hint={"center_x": 0.5},
                on_release=lambda x: self.trocar_aba(primeira_da_proxima)
            )
            box.add_widget(self.btn_avancar_etapa)

        self.btn_finalizar = MDButton(MDButtonText(text=txt("btn_finalizar")), style="filled", pos_hint={"center_x": 0.5}, on_release=self.finalizar_e_ir_resumo)
        box.add_widget(self.btn_finalizar)

    def pedir_limpar(self, instance=None):
        if self.dialog_limpar:
            self.dialog_limpar.dismiss()
        self.dialog_limpar = MDDialog(
            MDDialogHeadlineText(text=txt("btn_limpar")),
            MDDialogSupportingText(text=txt("dialog_limpar")),
            MDDialogButtonContainer(
                MDButton(MDButtonText(text=txt("btn_cancelar")), on_release=lambda x: self.dialog_limpar.dismiss()),
                MDButton(MDButtonText(text=txt("btn_confirmar")), on_release=self.limpar_aba_atual)
            )
        )
        self.dialog_limpar.open()

    def limpar_aba_atual(self, instance=None):
        """Apaga só a aba aberta (as outras não são afetadas)."""
        aba = self.aba_atual
        self.estado_abas.pop(aba, None)
        self.textos_resultado.pop(aba, None)
        self.traco[aba] = self._tabela_traco(aba)[1]
        if aba in self.tijolo:
            self.tijolo[aba] = TIJOLO_PADRAO
        if aba in self.assent:
            self.assent[aba] = ASSENTAMENTO_PADRAO
        if aba in self.bitola:
            self.bitola[aba] = BITOLA_PADRAO
        if aba in self.imperm:
            self.imperm[aba] = False
        if aba in self.dois_lados:
            self.dois_lados[aba] = False
        if aba in self.chapisco:
            self.chapisco[aba] = False
        if aba in self.argamassa:
            self.argamassa[aba] = ARGAMASSA_PADRAO_PISO if aba == "piso" else ARGAMASSA_PADRAO_AZULEJO
        if aba == "laje":
            self.laje_tipo = TIPO_LAJE_PADRAO
            self.laje_enchimento = ENCHIMENTO_PADRAO
        if aba == "telhado":
            self.telha_tipo = TIPO_TELHA_PADRAO
            self.madeiramento[aba] = False
        if aba == "pintura":
            self.selador[aba] = False
            self.fundo[aba] = False
            self.massa_tipo = "nenhuma"
        if aba == "esquadrias":
            self.esquadrias_itens = []
            self.esq_tipo = TIPO_ESQUADRIA_PADRAO
            self.esq_material = MATERIAL_PADRAO
            self.esq_fixacao = {"espuma": False, "parafusos": False, "argamassa": False}
        self._campos = {}
        self.trocar_aba(aba)
        if self.dialog_limpar:
            self.dialog_limpar.dismiss()

    # ==========================================
    # DROPDOWNS (traço do concreto e bitola do ferro)
    # ==========================================
    @staticmethod
    def _rotulo_bitola(bitola):
        if float(bitola).is_integer():
            return f"{int(bitola)} mm"
        return f"{fmt_num(bitola, 1)} mm"

    def _montar_dropdown(self, box_form, titulo, opcoes, atual, ao_escolher, rotulo=str, largura=200):
        """Título + botão que abre a lista de opções. Retorna o texto do botão (mostra a opção atual)."""
        box_form.add_widget(MDLabel(text=titulo, font_style="Title", role="small", bold=True, theme_text_color="Primary"))
        texto = MDButtonText(text=rotulo(atual))
        botao = MDButton(
            MDButtonIcon(icon="menu-down"),
            texto,
            style="outlined",
            size_hint_x=1,
            disabled=self.modo_somente_leitura,
            on_release=lambda x: self._abrir_menu(x, opcoes, ao_escolher, rotulo, largura)
        )
        box_form.add_widget(botao)
        return texto

    def _abrir_menu(self, caller, opcoes, ao_escolher, rotulo, largura=200):
        if self.menu_ativo:
            self.menu_ativo.dismiss()
        # largura=None: o menu fica da largura do botão (não passa da tela)
        largura_menu = dp(largura) if largura else getattr(caller, "width", dp(300))
        itens = [
            {"text": rotulo(opcao), "on_release": lambda *args, o=opcao: self._escolher_no_menu(ao_escolher, o)}
            for opcao in opcoes
        ]
        self.menu_ativo = MDDropdownMenu(caller=caller, items=itens, width=largura_menu, position="bottom")
        self.menu_ativo.open()

    def _escolher_no_menu(self, ao_escolher, opcao):
        ao_escolher(opcao)
        if self.menu_ativo:
            self.menu_ativo.dismiss()

    # --- Traço do concreto (Brocas e Baldrame) ---
    @staticmethod
    def _tabela_traco(aba):
        """Concreto (Brocas, Baldrame) ou massa (Paredes): tabela de traços, traço padrão e título do campo."""
        if aba == "paredes":
            return TRACOS_MASSA, TRACO_MASSA_PADRAO, "label_traco_massa"
        if aba == "reboco":
            return TRACOS_MASSA, TRACO_MASSA_PADRAO, "label_traco_massa_obrig"
        return TRACOS_CONCRETO, TRACO_CONCRETO_PADRAO, "label_traco"

    def _montar_seletor_traco(self, box_form, aba):
        tabela, _, titulo = self._tabela_traco(aba)
        self._botoes_traco[aba] = self._montar_dropdown(
            box_form, txt(titulo), list(tabela.keys()), self.traco[aba],
            lambda nome: self._escolher_traco(aba, nome)
        )

    def _escolher_traco(self, aba, nome):
        self.traco[aba] = nome
        if aba in self._botoes_traco:
            self._botoes_traco[aba].text = nome

    # --- Bitola do ferro ---
    def _montar_seletor_bitola(self, box_form, aba):
        self._botoes_bitola[aba] = self._montar_dropdown(
            box_form, txt("label_bitola"), BITOLAS_LONGITUDINAL, self.bitola[aba],
            lambda b: self._escolher_bitola(aba, b), rotulo=self._rotulo_bitola
        )

    def _escolher_bitola(self, aba, bitola):
        self.bitola[aba] = bitola
        if aba in self._botoes_bitola:
            self._botoes_bitola[aba].text = self._rotulo_bitola(bitola)

    # --- Tijolo / bloco e assentamento (Paredes) ---
    @staticmethod
    def _rotulo_tijolo(chave):
        return txt(f"tj_{chave}")

    def _montar_seletor_tijolo(self, box_form, aba):
        self._botoes_tijolo[aba] = self._montar_dropdown(
            box_form, txt("label_tijolo"), list(TIJOLOS.keys()), self.tijolo[aba],
            lambda t: self._escolher_tijolo(aba, t), rotulo=self._rotulo_tijolo, largura=None
        )

    def _escolher_tijolo(self, aba, chave):
        self.tijolo[aba] = chave
        if aba in self._botoes_tijolo:
            self._botoes_tijolo[aba].text = self._rotulo_tijolo(chave)

    @staticmethod
    def _rotulo_assent(chave):
        return txt(f"opcao_{chave}")

    def _montar_seletor_assent(self, box_form, aba):
        self._botoes_assent[aba] = self._montar_dropdown(
            box_form, txt("label_assent"), ASSENTAMENTOS, self.assent[aba],
            lambda a: self._escolher_assent(aba, a), rotulo=self._rotulo_assent
        )

    def _escolher_assent(self, aba, chave):
        self.assent[aba] = chave
        if aba in self._botoes_assent:
            self._botoes_assent[aba].text = self._rotulo_assent(chave)

    # --- Sim / Não genérico (Reboco: dois lados e chapisco) ---
    def _montar_sim_nao(self, box_form, titulo, estado, aba, nome):
        self._botoes_sn[(nome, aba)] = self._montar_dropdown(
            box_form, titulo, [False, True], estado[aba],
            lambda v: self._escolher_sim_nao(estado, aba, nome, v), rotulo=self._rotulo_sim_nao
        )

    def _escolher_sim_nao(self, estado, aba, nome, valor):
        estado[aba] = valor
        if (nome, aba) in self._botoes_sn:
            self._botoes_sn[(nome, aba)].text = self._rotulo_sim_nao(valor)

    # --- Impermeabilização (Sim / Não) ---
    @staticmethod
    def _rotulo_sim_nao(valor):
        return txt("opcao_sim") if valor else txt("opcao_nao")

    def _montar_seletor_imperm(self, box_form, aba):
        self._botoes_imperm[aba] = self._montar_dropdown(
            box_form, txt("label_imperm"), [False, True], self.imperm[aba],
            lambda v: self._escolher_imperm(aba, v), rotulo=self._rotulo_sim_nao
        )

    def _escolher_imperm(self, aba, valor):
        self.imperm[aba] = valor
        if aba in self._botoes_imperm:
            self._botoes_imperm[aba].text = self._rotulo_sim_nao(valor)

    # --- Ajuda "?" da aba (inclui a nota sobre os valores padrão) ---
    def abrir_ajuda(self, instance=None):
        if self.dialog_ajuda:
            self.dialog_ajuda.dismiss()
        texto = f"{txt(f'ajuda_{self.aba_atual}')}\n\n{txt('nota_opcionais')}"
        self.dialog_ajuda = MDDialog(
            MDDialogHeadlineText(text=txt("titulo_ajuda")),
            MDDialogSupportingText(text=texto),
            MDDialogButtonContainer(
                MDButton(MDButtonText(text=txt("btn_fechar")), on_release=lambda x: self.dialog_ajuda.dismiss())
            )
        )
        self.dialog_ajuda.open()

    # ==========================================
    # CÁLCULOS (a partir do texto digitado, sem depender dos campos na tela)
    # ==========================================
    @staticmethod
    def _numero(texto, padrao=0.0):
        texto = (texto or "").strip()
        return float(texto.replace(',', '.')) if texto else padrao

    def _aba_iniciada(self, aba, estado):
        if aba == "esquadrias" and self.esquadrias_itens:
            return True  # a lista já tem itens (mesmo com o formulário vazio)
        return any((estado.get(chave) or "").strip() for chave in CAMPOS_INICIAIS[aba])

    def _calcular_aba(self, aba, e):
        """Retorna {"erro": mensagem} ou {"texto": resultado na tela, "resultado": dados da etapa}."""
        try:
            if aba == "baldrame":
                return self._calcular_baldrame(e)
            if aba == "paredes":
                return self._calcular_paredes(e)
            if aba == "contrapiso":
                return self._calcular_contrapiso(e)
            if aba == "reboco":
                return self._calcular_reboco(e)
            if aba in ("piso", "azulejo"):
                return self._calcular_ceramica(aba, e)
            if aba == "rejunte":
                return self._calcular_rejunte(e)
            if aba == "laje":
                return self._calcular_laje(e)
            if aba == "telhado":
                return self._calcular_telhado(e)
            if aba == "eletrica":
                return self._calcular_eletrica(e)
            if aba == "hidraulica":
                return self._calcular_hidraulica(e)
            if aba == "pintura":
                return self._calcular_pintura(e)
            if aba == "esquadrias":
                return self._calcular_esquadrias(e)
            return self._calcular_brocas(e)
        except ValueError:
            return {"erro": txt("msg_erro_num")}

    def _calcular_brocas(self, e):
        if not (e.get("qtd") or "").strip() or not (e.get("prof") or "").strip() or not (e.get("diam") or "").strip():
            return {"erro": txt("msg_erro_num")}

        qtd = int(e["qtd"].strip())
        prof = self._numero(e["prof"])
        diam = self._numero(e["diam"])
        perda = self._numero(e.get("perda"), 10.0)
        t_barras = (e.get("barras") or "").strip()
        num_barras = int(t_barras) if t_barras else 0
        esp_estribo = self._numero(e.get("esp_estribo"), 0.0)
        preco_mo = self._numero(e.get("mo"), 0.0)
        bitola = self.bitola["brocas"]

        res = calcular_brocas(
            quantidade=qtd, profundidade_m=prof, diametro_cm=diam,
            perda_percentual=perda, incluir_ferragem=(num_barras > 0),
            num_barras_longitudinais=num_barras, bitola_mm=bitola,
            preco_mao_obra_metro=preco_mo, traco=self.traco["brocas"],
            espacamento_estribo_cm=esp_estribo
        )
        if "erro" in res:
            return {"erro": f"Erro: {res['erro']}"}

        custo_cimento = res['sacos_cimento'] * TABELA_PRECOS_GLOBAL.cimento_50kg
        custo_areia = res['areia_m3'] * TABELA_PRECOS_GLOBAL.areia_m3
        custo_pedra = res['pedra_m3'] * TABELA_PRECOS_GLOBAL.pedra_m3
        custo_aco = res['quilos_aco'] * TABELA_PRECOS_GLOBAL.aco_kg if res['incluiu_ferragem'] else 0.0
        custo_mo = res['custo_mao_obra']
        custo_mat = custo_cimento + custo_areia + custo_pedra + custo_aco
        custo_total = custo_mat + custo_mo

        texto_res = (
            f"{txt('label_traco_curto')}: {res['traco']}\n"
            f"{txt('label_volume')} ({fmt_num(res['perda_percentual'], 0)}% perda): {fmt_num(res['volume_com_perda_m3'], 3)} m³\n"
            f"• {txt('label_cimento')}: {res['sacos_cimento']} {txt('un_sacos')} ({fmt_moeda(custo_cimento)})\n"
            f"• {txt('label_areia')}: {fmt_num(res['areia_m3'], 2)} m³ ({fmt_moeda(custo_areia)})\n"
            f"• {txt('label_pedra')}: {fmt_num(res['pedra_m3'], 2)} m³ ({fmt_moeda(custo_pedra)})\n"
        )
        if res['incluiu_ferragem']:
            texto_res += (
                f"• {txt('label_ferro')} {self._rotulo_bitola(res['bitola_mm'])}: "
                f"{fmt_num(res['kg_longitudinal'], 1)} kg ({res['barras_12m_longitudinal']} {txt('un_barras12')})\n"
            )
            if res['incluiu_estribos']:
                texto_res += (
                    f"• {txt('label_estribos')} {self._rotulo_bitola(res['bitola_estribo_mm'])} "
                    f"c/ {fmt_num(res['espacamento_estribo_cm'], 0)} cm: "
                    f"{fmt_num(res['kg_estribos'], 1)} kg ({res['barras_12m_estribos']} {txt('un_barras12')})\n"
                )
            texto_res += f"• {txt('label_aco')}: {fmt_num(res['quilos_aco'], 1)} kg ({fmt_moeda(custo_aco)})\n"
        if custo_mo > 0:
            texto_res += f"• {txt('label_mo')}: {fmt_num(res['total_metros_escavados'], 1)} m ({fmt_moeda(custo_mo)})\n"
        texto_res += f"\n{txt('label_custo')}: {fmt_moeda(custo_total)}"

        resultado = {
            "etapa": txt("secao_brocas"),
            "tipo": "brocas",
            "inputs": {
                "qtd": qtd, "prof": prof, "diam": diam, "perda": perda, "barras": num_barras,
                "mo": preco_mo, "traco": res["traco"], "bitola": bitola, "esp_estribo": esp_estribo
            },
            "cimento": res['sacos_cimento'], "areia": res['areia_m3'], "pedra": res['pedra_m3'],
            "aco_kg": res['quilos_aco'], "barras_12m": res['barras_12m'],
            "custo_mat": custo_mat, "custo_mo": custo_mo, "custo_total": custo_total,
            "resumo_texto": texto_res
        }
        return {"texto": texto_res, "resultado": resultado}

    def _calcular_baldrame(self, e):
        if not (e.get("comp") or "").strip() or not (e.get("larg") or "").strip() or not (e.get("alt") or "").strip():
            return {"erro": txt("msg_erro_num")}

        comp = self._numero(e["comp"])
        larg = self._numero(e["larg"])
        alt = self._numero(e["alt"])
        perda = self._numero(e.get("perda"), PERDA_PADRAO_BALDRAME)
        t_barras = (e.get("barras") or "").strip()
        num_barras = int(t_barras) if t_barras else 0
        esp_estribo = self._numero(e.get("esp_estribo"), 0.0)
        preco_mo = self._numero(e.get("mo"), 0.0)
        bitola = self.bitola["baldrame"]
        imperm = self.imperm["baldrame"]

        res = calcular_baldrame(
            comprimento_m=comp, largura_cm=larg, altura_cm=alt,
            perda_percentual=perda, traco=self.traco["baldrame"],
            num_barras_longitudinais=num_barras, bitola_mm=bitola,
            espacamento_estribo_cm=esp_estribo, incluir_impermeabilizacao=imperm
        )
        if "erro" in res:
            return {"erro": f"Erro: {res['erro']}"}

        custo_cimento = res['sacos_cimento'] * TABELA_PRECOS_GLOBAL.cimento_50kg
        custo_areia = res['areia_m3'] * TABELA_PRECOS_GLOBAL.areia_m3
        custo_pedra = res['pedra_m3'] * TABELA_PRECOS_GLOBAL.pedra_m3
        custo_aco = res['quilos_aco'] * TABELA_PRECOS_GLOBAL.aco_kg if res['incluiu_ferragem'] else 0.0
        custo_mo = comp * preco_mo
        custo_imperm = res['latas_imperm'] * PRECO_LATA_IMPERM if res['incluiu_impermeabilizacao'] else 0.0
        custo_mat = custo_cimento + custo_areia + custo_pedra + custo_aco + custo_imperm
        custo_total = custo_mat + custo_mo

        texto_res = (
            f"{txt('label_traco_curto')}: {res['traco']}\n"
            f"{txt('label_volume')} ({fmt_num(perda, 0)}% perda): {fmt_num(res['volume_com_perda_m3'], 3)} m³\n"
            f"• {txt('label_cimento')}: {res['sacos_cimento']} {txt('un_sacos')} ({fmt_moeda(custo_cimento)})\n"
            f"• {txt('label_areia')}: {fmt_num(res['areia_m3'], 2)} m³ ({fmt_moeda(custo_areia)})\n"
            f"• {txt('label_pedra')}: {fmt_num(res['pedra_m3'], 2)} m³ ({fmt_moeda(custo_pedra)})\n"
        )
        if res['incluiu_ferragem']:
            texto_res += (
                f"• {txt('label_ferro')} {self._rotulo_bitola(res['bitola_mm'])}: "
                f"{fmt_num(res['kg_longitudinal'], 1)} kg ({res['barras_12m_longitudinal']} {txt('un_barras12')})\n"
            )
            if res['incluiu_estribos']:
                texto_res += (
                    f"• {txt('label_estribos')} {self._rotulo_bitola(res['bitola_estribo_mm'])} "
                    f"c/ {fmt_num(res['espacamento_estribo_cm'], 0)} cm: "
                    f"{fmt_num(res['kg_estribos'], 1)} kg ({res['barras_12m_estribos']} {txt('un_barras12')})\n"
                )
            texto_res += f"• {txt('label_aco')}: {fmt_num(res['quilos_aco'], 1)} kg ({fmt_moeda(custo_aco)})\n"
        if res['incluiu_impermeabilizacao']:
            un_lata = txt('un_lata') if res['latas_imperm'] == 1 else txt('un_latas')
            texto_res += (
                f"• {txt('label_imperm_item')}: {fmt_num(res['area_imperm_m2'], 1)} m² · "
                f"{fmt_num(res['litros_imperm'], 1)} L ({res['latas_imperm']} {un_lata}) ({fmt_moeda(custo_imperm)})\n"
            )
        if custo_mo > 0:
            texto_res += f"• {txt('label_mo')}: {fmt_num(comp, 1)} m ({fmt_moeda(custo_mo)})\n"
        texto_res += f"\n{txt('label_custo')}: {fmt_moeda(custo_total)}"

        resultado = {
            "etapa": txt("secao_baldrame"),
            "tipo": "baldrame",
            "cimento": res['sacos_cimento'], "areia": res['areia_m3'], "pedra": res['pedra_m3'],
            "aco_kg": res['quilos_aco'], "barras_12m": res['barras_12m'],
            "imperm_litros": res['litros_imperm'],
            "custo_mat": custo_mat, "custo_mo": custo_mo, "custo_total": custo_total,
            "resumo_texto": texto_res,
            "inputs": {
                "comp": comp, "larg": larg, "alt": alt, "perda": perda, "mo": preco_mo,
                "traco": res["traco"], "barras": num_barras, "bitola": bitola,
                "esp_estribo": esp_estribo, "imperm": imperm
            }
        }
        return {"texto": texto_res, "resultado": resultado}

    def _calcular_reboco(self, e):
        if not (e.get("area") or "").strip() or not (e.get("esp") or "").strip():
            return {"erro": txt("msg_erro_num")}

        area = self._numero(e["area"])
        esp = self._numero(e["esp"])
        vaos = self._numero(e.get("vaos"), 0.0)
        perda = self._numero(e.get("perda"), PERDA_PADRAO_REBOCO)
        dois_lados = self.dois_lados["reboco"]
        chapisco = self.chapisco["reboco"]

        res = calcular_reboco(
            area_bruta_m2=area, espessura_cm=esp, desconto_vaos_m2=vaos,
            dois_lados=dois_lados, chapisco=chapisco, perda_percentual=perda,
            traco=self.traco["reboco"]
        )
        if "erro" in res:
            return {"erro": f"Erro: {res['erro']}"}

        custo_cimento = res['sacos_cimento'] * TABELA_PRECOS_GLOBAL.cimento_50kg
        custo_cal = res['sacos_cal'] * TABELA_PRECOS_GLOBAL.cal_20kg
        custo_areia = res['areia_m3'] * TABELA_PRECOS_GLOBAL.areia_m3
        custo_mat = custo_cimento + custo_cal + custo_areia

        texto_res = f"{txt('label_area_bruta')}: {fmt_num(res['area_bruta_m2'], 2)} m²\n"
        if res['desconto_vaos_m2'] > 0:
            texto_res += f"{txt('label_vaos')}: {fmt_num(res['desconto_vaos_m2'], 2)} m²\n"
            texto_res += f"{txt('label_area_liquida')}: {fmt_num(res['area_liquida_m2'], 2)} m²\n"
        if dois_lados:
            texto_res += f"{txt('label_area_rebocar')} ({txt('txt_dois_lados')}): {fmt_num(res['area_rebocada_m2'], 2)} m²\n"
        texto_res += (
            f"{txt('label_traco_curto')}: {res['traco']}\n"
            f"{txt('label_volume_reboco')} ({fmt_num(perda, 0)}% perda): {fmt_num(res['volume_reboco_m3'], 3)} m³\n"
        )
        if chapisco:
            texto_res += f"{txt('label_chapisco_res')}: {txt('txt_chapisco_incluido')} ({CHAPISCO_TRACO_RODAPE}, {fmt_num(CHAPISCO_ESPESSURA_CM, 1)} cm)\n"
        texto_res += (
            f"• {txt('label_cimento')}: {res['sacos_cimento']} {txt('un_sacos')} ({fmt_moeda(custo_cimento)})\n"
            f"• {txt('label_cal')}: {res['sacos_cal']} {txt('un_sacos_cal')} ({fmt_moeda(custo_cal)})\n"
            f"• {txt('label_areia')}: {fmt_num(res['areia_m3'], 2)} m³ ({fmt_moeda(custo_areia)})\n"
            f"\n{txt('label_custo')}: {fmt_moeda(custo_mat)}"
        )

        resultado = {
            "etapa": txt("secao_reboco"),
            "tipo": "reboco",
            "cimento": res['sacos_cimento'], "cal": res['sacos_cal'], "areia": res['areia_m3'],
            "custo_mat": custo_mat, "custo_mo": 0.0, "custo_total": custo_mat,
            "resumo_texto": texto_res,
            "inputs": {
                "area": area, "vaos": vaos, "esp": esp, "perda": perda,
                "traco": res["traco"], "dois_lados": dois_lados, "chapisco": chapisco
            }
        }
        return {"texto": texto_res, "resultado": resultado}

    def _calcular_ceramica(self, aba, e):
        piso = (aba == "piso")
        if not all((e.get(k) or "").strip() for k in ("area", "larg", "alt")):
            return {"erro": txt("msg_erro_num")}

        area = self._numero(e["area"])
        larg = self._numero(e["larg"])
        alt = self._numero(e["alt"])
        caixa = self._numero(e.get("caixa"), 0.0)
        perda = self._numero(e.get("perda"), PERDA_PADRAO_REVESTIMENTO)
        tipo_arg = self.argamassa[aba]
        vaos = 0.0 if piso else self._numero(e.get("vaos"), 0.0)
        rodape = self._numero(e.get("rodape"), 0.0) if piso else 0.0

        if piso:
            res = calcular_piso(area, larg, alt, caixa, tipo_arg, perda, rodape)
        else:
            res = calcular_azulejo(area, larg, alt, vaos, caixa, tipo_arg, perda)
        if "erro" in res:
            return {"erro": f"Erro: {res['erro']}"}

        preco_m2 = PRECO_PISO_M2 if piso else PRECO_AZULEJO_M2
        custo_pecas = res['area_com_perda_m2'] * preco_m2
        custo_arg = res['sacos_argamassa'] * PRECO_ARGAMASSA_SACO[tipo_arg]
        custo_rodape = res['rodape_m'] * PRECO_RODAPE_M
        custo_mat = custo_pecas + custo_arg + custo_rodape

        texto_res = f"{txt('label_area')}: {fmt_num(res['area_bruta_m2'], 2)} m²\n"
        if res['desconto_vaos_m2'] > 0:
            texto_res += f"{txt('label_vaos')}: {fmt_num(res['desconto_vaos_m2'], 2)} m²\n"
            texto_res += f"{txt('label_area_liquida')}: {fmt_num(res['area_liquida_m2'], 2)} m²\n"
        texto_res += (
            f"{txt('label_area_perda')} ({fmt_num(perda, 0)}%): {fmt_num(res['area_com_perda_m2'], 2)} m²\n"
            f"{txt('label_peca')}: {fmt_num(larg, 0 if float(larg).is_integer() else 1)}x{fmt_num(alt, 0 if float(alt).is_integer() else 1)} cm\n"
        )
        custo_txt = f" ({fmt_moeda(custo_pecas)})"
        if res['caixas'] > 0:
            texto_res += f"• {txt('label_pecas')}: {res['pecas']} {txt('un_pecas')}\n"
            texto_res += f"• {txt('label_caixas')}: {res['caixas']} {txt('un_caixas')} ({fmt_num(caixa, 2)} {txt('un_caixa_m2')}){custo_txt}\n"
        else:
            texto_res += f"• {txt('label_pecas')}: {res['pecas']} {txt('un_pecas')}{custo_txt}\n"
        texto_res += (
            f"• {txt('label_argamassa_res')} {tipo_arg}: {res['sacos_argamassa']} {txt('un_sacos_cal')} "
            f"({fmt_num(res['argamassa_kg'], 1)} kg) ({fmt_moeda(custo_arg)})\n"
        )
        if res['rodape_m'] > 0:
            texto_res += (
                f"• {txt('label_rodape')}: {fmt_num(res['rodape_m'], 2)} m "
                f"({res['rodape_pecas']} {txt('un_pecas')} {txt('un_de')} {fmt_num(RODAPE_PECA_M, 2)} m) ({fmt_moeda(custo_rodape)})\n"
            )
        texto_res += f"\n{txt('label_custo')}: {fmt_moeda(custo_mat)}"

        resultado = {
            "etapa": txt("secao_" + aba),
            "tipo": aba,
            "argamassa_sacos": res['sacos_argamassa'],
            "pecas": res['pecas'], "caixas": res['caixas'], "rodape_m": res['rodape_m'],
            "custo_mat": custo_mat, "custo_mo": 0.0, "custo_total": custo_mat,
            "resumo_texto": texto_res,
            "inputs": {
                "area": area, "larg": larg, "alt": alt, "caixa": caixa, "perda": perda,
                "argamassa": tipo_arg, "vaos": vaos, "rodape": rodape
            }
        }
        return {"texto": texto_res, "resultado": resultado}

    @staticmethod
    def _texto_latas(latas_1kg, latas_2kg):
        """Ex.: '2 latas de 2 kg e 1 lata de 1 kg'."""
        partes = []
        if latas_2kg:
            partes.append(f"{latas_2kg} {txt('un_lata_2kg') if latas_2kg == 1 else txt('un_latas_2kg')}")
        if latas_1kg:
            partes.append(f"{latas_1kg} {txt('un_lata_1kg') if latas_1kg == 1 else txt('un_latas_1kg')}")
        return f" {txt('un_e')} ".join(partes)

    def _calcular_rejunte(self, e):
        if not all((e.get(k) or "").strip() for k in ("area", "larg", "alt", "junta")):
            return {"erro": txt("msg_erro_num")}

        area = self._numero(e["area"])
        larg = self._numero(e["larg"])
        alt = self._numero(e["alt"])
        junta = self._numero(e["junta"])
        esp = self._numero(e.get("esp"), ESPESSURA_PADRAO_MM)
        perda = self._numero(e.get("perda"), PERDA_PADRAO_REJUNTE)

        res = calcular_rejunte(area, larg, alt, junta, esp, perda)
        if "erro" in res:
            return {"erro": f"Erro: {res['erro']}"}

        custo_mat = res['latas_1kg'] * PRECO_LATA_1KG + res['latas_2kg'] * PRECO_LATA_2KG

        def n(v):
            return fmt_num(v, 0 if float(v).is_integer() else 1)

        texto_res = (
            f"{txt('label_area')}: {fmt_num(res['area_m2'], 2)} m²\n"
            f"{txt('label_peca')}: {n(larg)}x{n(alt)} cm\n"
            f"{txt('label_junta')}: {n(junta)} mm\n"
            f"{txt('label_espessura')}: {n(esp)} mm\n"
            f"{txt('label_consumo')}: {fmt_num(res['consumo_kg_m2'], 3)} kg/m²\n"
            f"• {txt('label_rejunte_res')} ({txt('label_com_perda').format(p=fmt_num(perda, 0))}): {fmt_num(res['kg_total'], 2)} kg\n"
            f"• {self._texto_latas(res['latas_1kg'], res['latas_2kg'])} ({fmt_moeda(custo_mat)})\n"
            f"\n{txt('label_custo')}: {fmt_moeda(custo_mat)}"
        )

        resultado = {
            "etapa": txt("secao_rejunte"),
            "tipo": "rejunte",
            "rejunte_kg": res['kg_total'],
            "rejunte_latas_1kg": res['latas_1kg'],
            "rejunte_latas_2kg": res['latas_2kg'],
            "custo_mat": custo_mat, "custo_mo": 0.0, "custo_total": custo_mat,
            "resumo_texto": texto_res,
            "inputs": {"area": area, "larg": larg, "alt": alt, "junta": junta, "esp": esp, "perda": perda}
        }
        return {"texto": texto_res, "resultado": resultado}

    def _calcular_laje(self, e):
        premoldada = (self.laje_tipo == "premoldada")
        obrigatorios = ("area",) if premoldada else ("area", "esp")
        if not all((e.get(k) or "").strip() for k in obrigatorios):
            return {"erro": txt("msg_erro_num")}

        area = self._numero(e["area"])
        capa = self._numero(e.get("capa"), CAPA_PADRAO_CM)
        esp = self._numero(e.get("esp"), 0.0)
        perda = self._numero(e.get("perda"), PERDA_PADRAO_LAJE)

        res = calcular_laje(area, self.laje_tipo, self.laje_enchimento, capa, esp, perda, self.traco["laje"])
        if "erro" in res:
            return {"erro": f"Erro: {res['erro']}"}

        custo_cimento = res['sacos_cimento'] * TABELA_PRECOS_GLOBAL.cimento_50kg
        custo_areia = res['areia_m3'] * TABELA_PRECOS_GLOBAL.areia_m3
        custo_pedra = res['pedra_m3'] * TABELA_PRECOS_GLOBAL.pedra_m3
        custo_laje_pm = res['laje_premoldada_m2'] * PRECO_LAJE_PREMOLDADA_M2.get(res['enchimento'], 0.0)
        custo_mat = custo_cimento + custo_areia + custo_pedra + custo_laje_pm

        def n(v):
            return fmt_num(v, 0 if float(v).is_integer() else 1)

        texto_res = (
            f"{txt('label_area')}: {fmt_num(res['area_m2'], 2)} m²\n"
            f"{txt('label_tipo_laje')}: {self._rotulo_laje(res['tipo'])}\n"
        )
        if premoldada:
            texto_res += (
                f"{txt('label_enchimento').replace(' (Opcional)', '').replace(' (Optional)', '')}: {self._rotulo_laje(res['enchimento'])}\n"
                f"{txt('label_capa')}: {n(res['capa_cm'])} cm\n"
            )
        else:
            texto_res += f"{txt('label_espessura_laje')}: {n(res['espessura_cm'])} cm\n"
        texto_res += (
            f"{txt('label_traco_curto')}: {res['traco']}\n"
            f"{txt('label_volume')} ({txt('label_com_perda').format(p=fmt_num(perda, 0))}): {fmt_num(res['volume_com_perda_m3'], 3)} m³\n"
        )
        if premoldada:
            texto_res += f"• {txt('label_laje_pm')}: {fmt_num(res['laje_premoldada_m2'], 2)} m² ({fmt_moeda(custo_laje_pm)})\n"
            if res['lajotas'] > 0:
                texto_res += f"  ({txt('label_lajotas')}: {res['lajotas']} {txt('un_unidades')})\n"
        texto_res += (
            f"• {txt('label_cimento')}: {res['sacos_cimento']} {txt('un_sacos')} ({fmt_moeda(custo_cimento)})\n"
            f"• {txt('label_areia')}: {fmt_num(res['areia_m3'], 2)} m³ ({fmt_moeda(custo_areia)})\n"
            f"• {txt('label_pedra')}: {fmt_num(res['pedra_m3'], 2)} m³ ({fmt_moeda(custo_pedra)})\n"
            f"\n{txt('label_custo')}: {fmt_moeda(custo_mat)}"
        )

        resultado = {
            "etapa": txt("secao_laje"),
            "tipo": "laje",
            "cimento": res['sacos_cimento'], "areia": res['areia_m3'], "pedra": res['pedra_m3'],
            "laje_premoldada_m2": res['laje_premoldada_m2'], "lajotas": res['lajotas'],
            "custo_mat": custo_mat, "custo_mo": 0.0, "custo_total": custo_mat,
            "resumo_texto": texto_res,
            "inputs": {
                "area": area, "capa": capa, "esp": esp if esp > 0 else "", "perda": perda, "traco": res["traco"],
                "tipo_laje": res["tipo"], "enchimento": self.laje_enchimento
            }
        }
        return {"texto": texto_res, "resultado": resultado}

    def _calcular_telhado(self, e):
        if not (e.get("area") or "").strip():
            return {"erro": txt("msg_erro_num")}

        tipo = self.telha_tipo
        area = self._numero(e["area"])
        incl = self._numero(e.get("incl"), INCLINACAO_PADRAO[tipo])
        cumeeira = self._numero(e.get("cumeeira"), 0.0)
        perda = self._numero(e.get("perda"), PERDA_PADRAO_TELHADO)
        madeira = self.madeiramento["telhado"]

        res = calcular_telhado(area, tipo, incl, cumeeira, madeira, perda)
        if "erro" in res:
            return {"erro": f"Erro: {res['erro']}"}

        custo_telhas = res['telhas'] * PRECO_TELHA[tipo]
        custo_cumeeira = res['cumeeiras'] * PRECO_CUMEEIRA[tipo]
        custo_ripas = res['ripas_m'] * PRECO_MADEIRA_M["ripas"]
        custo_caibros = res['caibros_m'] * PRECO_MADEIRA_M["caibros"]
        custo_tercas = res['tercas_m'] * PRECO_MADEIRA_M["tercas"]
        custo_madeira = custo_ripas + custo_caibros + custo_tercas
        custo_mat = custo_telhas + custo_cumeeira + custo_madeira

        def n(v):
            return fmt_num(v, 0 if float(v).is_integer() else 1)

        texto_res = (
            f"{txt('label_area_planta')}: {fmt_num(res['area_planta_m2'], 2)} m²\n"
            f"{txt('label_inclinacao')}: {n(res['inclinacao_percentual'])}%\n"
            f"{txt('label_area_real')}: {fmt_num(res['area_real_m2'], 2)} m²\n"
            f"{txt('label_tipo_telha')}: {self._rotulo_telha(tipo)}\n\n"
            f"• {txt('label_telhas')} ({txt('label_com_perda').format(p=fmt_num(perda, 0))}): "
            f"{res['telhas']} {txt('un_unidades')} ({fmt_moeda(custo_telhas)})\n"
        )
        if res['cumeeiras'] > 0:
            texto_res += (
                f"• {txt('label_cumeeira')}: {fmt_num(res['cumeeira_m'], 2)} m = "
                f"{res['cumeeiras']} {txt('un_pecas')} ({fmt_moeda(custo_cumeeira)})\n"
            )
        if res['incluiu_madeiramento']:
            texto_res += f"• {txt('label_madeiramento_res')}:\n"
            for chave, custo in (("ripas", custo_ripas), ("caibros", custo_caibros), ("tercas", custo_tercas)):
                if res[f"{chave}_m"] > 0:
                    texto_res += f"   - {txt('label_' + chave)}: {fmt_num(res[chave + '_m'], 1)} m ({fmt_moeda(custo)})\n"
        texto_res += f"\n{txt('label_custo')}: {fmt_moeda(custo_mat)}"

        resultado = {
            "etapa": txt("secao_telhado"),
            "tipo": "telhado",
            "telhas": res['telhas'], "tipo_telha": tipo, "cumeeiras": res['cumeeiras'],
            "ripas_m": res['ripas_m'], "caibros_m": res['caibros_m'], "tercas_m": res['tercas_m'],
            "custo_mat": custo_mat, "custo_mo": 0.0, "custo_total": custo_mat,
            "resumo_texto": texto_res,
            "inputs": {
                "area": area, "incl": incl, "cumeeira": cumeeira if cumeeira > 0 else "", "perda": perda,
                "tipo_telha": tipo, "madeiramento": madeira
            }
        }
        return {"texto": texto_res, "resultado": resultado}

    def _calcular_esquadrias(self, e):
        # Digitou no formulário mas não adicionou: avisa (se começou, tem que terminar)
        if any((e.get(chave) or "").strip() for chave in CAMPOS_ABA["esquadrias"]):
            return {"erro": txt("msg_esquadria_pendente")}
        if not self.esquadrias_itens:
            return {"erro": txt("msg_lista_vazia")}

        fix = self.esq_fixacao
        res = calcular_esquadrias(self.esquadrias_itens, fix["espuma"], fix["parafusos"], fix["argamassa"])
        if "erro" in res:
            return {"erro": f"Erro: {res['erro']}"}

        custo_espuma = res['tubos_espuma'] * PRECO_TUBO_ESPUMA
        custo_parafusos = res['parafusos'] * PRECO_PARAFUSO
        custo_argamassa = res['sacos_argamassa'] * PRECO_SACO_ARGAMASSA_FIXACAO
        custo_mat = custo_espuma + custo_parafusos + custo_argamassa

        texto_res = ""
        for tipo, rotulo in (("porta", "label_portas"), ("janela", "label_janelas")):
            itens_tipo = [i for i in self.esquadrias_itens if i["tipo"] == tipo]
            if not itens_tipo:
                continue
            texto_res += f"{txt(rotulo)}:\n"
            for item in itens_tipo:
                area = (item["larg"] / 100.0) * (item["alt"] / 100.0)
                texto_res += f"• {self._texto_item_esquadria(item)}: {fmt_num(area, 2)} m² {txt('label_cada')}\n"
            texto_res += "\n"
        texto_res += (
            f"{txt('label_portas')}: {res['portas']} | {txt('label_janelas')}: {res['janelas']}\n"
            f"{txt('label_area_vaos')}: {fmt_num(res['area_vaos_m2'], 2)} m²\n"
        )
        if res['tubos_espuma'] or res['parafusos'] or res['sacos_argamassa']:
            texto_res += f"\n{txt('secao_fixacao')}:\n"
        if res['tubos_espuma'] > 0:
            qtd = res['tubos_espuma']
            texto_res += f"• {txt('label_res_espuma')}: {qtd} {txt('un_tubo_500') if qtd == 1 else txt('un_tubos_500')} ({fmt_moeda(custo_espuma)})\n"
        if res['parafusos'] > 0:
            texto_res += f"• {txt('label_res_parafusos')}: {res['parafusos']} {txt('un_unidades')} ({fmt_moeda(custo_parafusos)})\n"
        if res['sacos_argamassa'] > 0:
            qtd = res['sacos_argamassa']
            texto_res += (
                f"• {txt('label_res_argamassa_fix')}: {fmt_num(res['argamassa_kg'], 1)} kg = "
                f"{qtd} {txt('un_saco_20') if qtd == 1 else txt('un_sacos_20')} ({fmt_moeda(custo_argamassa)})\n"
            )
        texto_res += f"\n{txt('label_custo')}: {fmt_moeda(custo_mat)}"

        resultado = {
            "etapa": txt("secao_esquadrias"),
            "tipo": "esquadrias",
            "esquadrias": [dict(i) for i in self.esquadrias_itens],
            "tubos_espuma": res['tubos_espuma'], "parafusos": res['parafusos'],
            "sacos_argamassa_fix": res['sacos_argamassa'],
            "custo_mat": custo_mat, "custo_mo": 0.0, "custo_total": custo_mat,
            "resumo_texto": texto_res,
            "inputs": {"itens": [dict(i) for i in self.esquadrias_itens], **fix},
        }
        return {"texto": texto_res, "resultado": resultado}

    def _calcular_pintura(self, e):
        parede_txt = (e.get("parede") or "").strip()
        teto_txt = (e.get("teto") or "").strip()
        demaos_txt = (e.get("demaos") or "").strip()
        if not (parede_txt or teto_txt) or not demaos_txt:
            return {"erro": txt("msg_erro_num")}

        parede = self._numero(parede_txt, 0.0)
        teto = self._numero(teto_txt, 0.0)
        demaos = int(demaos_txt)
        rend = self._numero(e.get("rend"), RENDIMENTO_PADRAO_M2_L)
        perda = self._numero(e.get("perda"), PERDA_PADRAO_PINTURA)
        selador = self.selador["pintura"]
        fundo = self.fundo["pintura"]
        massa = self.massa_tipo

        res = calcular_pintura(parede, teto, demaos, rend, perda, selador, massa, fundo)
        if "erro" in res:
            return {"erro": f"Erro: {res['erro']}"}

        custos = {
            item: d['latas'] * PRECO_TINTA[item]["lata"] + d['galoes'] * PRECO_TINTA[item]["galao"]
            for item, d in res['itens'].items()
        }
        custo_massa = res['baldes_massa'] * PRECO_BALDE_MASSA.get(massa, 0.0)
        custo_mat = sum(custos.values()) + custo_massa

        def n(v):
            return fmt_num(v, 0 if float(v).is_integer() else 1)

        texto_res = ""
        if res['area_parede_m2'] > 0:
            texto_res += f"{txt('label_area_parede_pint')}: {fmt_num(res['area_parede_m2'], 2)} m²\n"
        if res['area_teto_m2'] > 0:
            texto_res += f"{txt('label_area_teto_pint')}: {fmt_num(res['area_teto_m2'], 2)} m²\n"
        texto_res += (
            f"{txt('label_demaos')}: {demaos}\n"
            f"{txt('label_rendimento')}: {n(rend)} m²/L\n\n"
        )
        perda_txt = txt('label_com_perda').format(p=fmt_num(perda, 0))
        for item, d in res['itens'].items():
            texto_res += (
                f"• {txt('label_pint_' + item)} ({perda_txt}): {fmt_num(d['litros'], 1)} L = "
                f"{self._texto_latas_galoes(d['latas'], d['galoes'])} ({fmt_moeda(custos[item])})\n"
            )
        if res['baldes_massa'] > 0:
            qtd = res['baldes_massa']
            texto_res += (
                f"• {self._rotulo_massa(massa)} ({perda_txt}): {fmt_num(res['massa_kg'], 1)} kg = "
                f"{qtd} {txt('un_balde_25') if qtd == 1 else txt('un_baldes_25')} ({fmt_moeda(custo_massa)})\n"
            )
        texto_res += f"\n{txt('label_custo')}: {fmt_moeda(custo_mat)}"

        resultado = {
            "etapa": txt("secao_pintura"),
            "tipo": "pintura",
            "pintura": {item: [d['latas'], d['galoes']] for item, d in res['itens'].items()},
            "massa_tipo": massa, "baldes_massa": res['baldes_massa'],
            "custo_mat": custo_mat, "custo_mo": 0.0, "custo_total": custo_mat,
            "resumo_texto": texto_res,
            "inputs": {
                "parede": parede if parede > 0 else "", "teto": teto if teto > 0 else "",
                "demaos": demaos, "rend": rend, "perda": perda,
                "selador": selador, "fundo": fundo, "massa": massa,
            }
        }
        return {"texto": texto_res, "resultado": resultado}

    def _calcular_hidraulica(self, e):
        def inteiro(chave):
            texto = (e.get(chave) or "").strip()
            return int(texto) if texto else 0

        pontos = {chave: inteiro(chave) for chave in ("fria", "quente", "esgoto")}
        tubos_projeto = {}
        for tubo in TUBOS:
            texto = (e.get(f"tubo_{tubo}") or "").strip()
            if texto:  # vazio = o app estima
                tubos_projeto[tubo] = self._numero(texto)
        perda = self._numero(e.get("perda"), PERDA_PADRAO_HIDRAULICA)

        res = calcular_hidraulica(pontos["fria"], pontos["quente"], pontos["esgoto"], tubos_projeto, perda)
        if "erro" in res:
            return {"erro": f"Erro: {res['erro']}"}

        custo_tubos = {t: d['barras'] * PRECO_BARRA_TUBO[t] for t, d in res['tubos'].items()}
        custo_conexoes = {t: q * PRECO_CONEXAO[t] for t, q in res['conexoes'].items()}
        custo_registros = res['registros'] * PRECO_REGISTRO
        custo_mat = sum(custo_tubos.values()) + sum(custo_conexoes.values()) + custo_registros

        texto_res = ""
        for chave in ("fria", "quente", "esgoto"):
            texto_res += f"{txt('label_pontos_' + chave)}: {pontos[chave]}\n"
        texto_res += "\n"
        for tubo, dados in res['tubos'].items():
            origem = txt("label_do_projeto") if dados['do_projeto'] else txt("label_estimado")
            texto_res += (
                f"• {txt('label_tubo_' + tubo)} ({origem}, {txt('label_com_perda').format(p=fmt_num(perda, 0))}): {fmt_num(dados['metros'], 1)} m = "
                f"{self._texto_barras(dados['barras'], BARRA_TUBO_M[tubo])} ({fmt_moeda(custo_tubos[tubo])})\n"
            )
        for tipo, qtd in res['conexoes'].items():
            texto_res += f"• {txt('label_conexoes_' + tipo)}: {qtd} {txt('un_unidades')} ({fmt_moeda(custo_conexoes[tipo])})\n"
        if res['registros'] > 0:
            texto_res += f"• {txt('label_registros')}: {res['registros']} {txt('un_unidades')} ({fmt_moeda(custo_registros)})\n"
        texto_res += f"\n{txt('label_custo')}: {fmt_moeda(custo_mat)}"

        inputs = {chave: (qtd if qtd else "") for chave, qtd in pontos.items()}
        for tubo in TUBOS:
            inputs[f"tubo_{tubo}"] = tubos_projeto.get(tubo, "")
        inputs["perda"] = perda

        resultado = {
            "etapa": txt("secao_hidraulica"),
            "tipo": "hidraulica",
            "tubos": {t: d['barras'] for t, d in res['tubos'].items()},
            "conexoes": res['conexoes'],
            "registros": res['registros'],
            "custo_mat": custo_mat, "custo_mo": 0.0, "custo_total": custo_mat,
            "resumo_texto": texto_res,
            "inputs": inputs,
        }
        return {"texto": texto_res, "resultado": resultado}

    def _calcular_eletrica(self, e):
        def inteiro(chave):
            texto = (e.get(chave) or "").strip()
            return int(texto) if texto else 0

        def metros(chave):
            texto = (e.get(chave) or "").strip()
            return self._numero(texto) if texto else None  # vazio = o app estima

        tomadas = inteiro("tomadas")
        interruptores = inteiro("interruptores")
        luzes = inteiro("luzes")
        conduite = metros("conduite")
        fios_projeto = {}
        for bitola in BITOLAS_FIO:
            valor = metros(self._chave_fio(bitola))
            if valor is not None:
                fios_projeto[bitola] = valor
        perda = self._numero(e.get("perda"), PERDA_PADRAO_ELETRICA)

        res = calcular_eletrica(tomadas, interruptores, luzes, conduite, fios_projeto, perda)
        if "erro" in res:
            return {"erro": f"Erro: {res['erro']}"}

        custo_conduite = res['rolos_conduite'] * PRECO_ROLO_CONDUITE
        custo_fios = {b: f['rolos'] * PRECO_ROLO_FIO[b] for b, f in res['fios'].items()}
        custo_caixas_4x2 = res['caixas_4x2'] * PRECO_CAIXA_4X2
        custo_caixas_oct = res['caixas_octogonais'] * PRECO_CAIXA_OCTOGONAL
        custo_caixas = custo_caixas_4x2 + custo_caixas_oct
        custo_tomadas = tomadas * PRECO_TOMADA
        custo_interruptores = interruptores * PRECO_INTERRUPTOR
        custo_mat = custo_conduite + sum(custo_fios.values()) + custo_caixas + custo_tomadas + custo_interruptores

        def origem(do_projeto):
            return txt("label_do_projeto") if do_projeto else txt("label_estimado")

        def rolos(qtd, un1, un2):
            return f"{qtd} {txt(un1) if qtd == 1 else txt(un2)}"

        texto_res = (
            f"{txt('label_tomadas')}: {tomadas}\n"
            f"{txt('label_interruptores')}: {interruptores}\n"
            f"{txt('label_luzes')}: {luzes}\n\n"
        )
        if res['rolos_conduite'] > 0:
            texto_res += (
                f"• {txt('label_conduite')} ({origem(not res['conduite_estimado'])}, {txt('label_com_perda').format(p=fmt_num(perda, 0))}): "
                f"{fmt_num(res['conduite_m'], 1)} m = {rolos(res['rolos_conduite'], 'un_rolo_conduite', 'un_rolos_conduite')} ({fmt_moeda(custo_conduite)})\n"
            )
        for bitola, fio in res['fios'].items():
            texto_res += (
                f"• {txt('label_fio').format(b=self._rotulo_bitola_fio(bitola))} ({origem(fio['do_projeto'])}, {txt('label_com_perda').format(p=fmt_num(perda, 0))}): "
                f"{fmt_num(fio['metros'], 1)} m = {rolos(fio['rolos'], 'un_rolo_fio', 'un_rolos_fio')} ({fmt_moeda(custo_fios[bitola])})\n"
            )
        if res['caixas_4x2'] > 0:
            texto_res += f"• {txt('label_caixa_4x2')}: {res['caixas_4x2']} {txt('un_unidades')} ({fmt_moeda(custo_caixas_4x2)})\n"
        if res['caixas_octogonais'] > 0:
            texto_res += f"• {txt('label_caixa_oct')}: {res['caixas_octogonais']} {txt('un_unidades')} ({fmt_moeda(custo_caixas_oct)})\n"
        if tomadas > 0:
            texto_res += f"• {txt('label_tomadas')}: {tomadas} {txt('un_unidades')} ({fmt_moeda(custo_tomadas)})\n"
        if interruptores > 0:
            texto_res += f"• {txt('label_interruptores')}: {interruptores} {txt('un_unidades')} ({fmt_moeda(custo_interruptores)})\n"
        texto_res += f"\n{txt('label_custo')}: {fmt_moeda(custo_mat)}"

        inputs = {
            "tomadas": tomadas if tomadas else "", "interruptores": interruptores if interruptores else "",
            "luzes": luzes if luzes else "", "conduite": conduite if conduite is not None else "", "perda": perda,
        }
        for bitola in BITOLAS_FIO:
            inputs[self._chave_fio(bitola)] = fios_projeto.get(bitola, "")

        resultado = {
            "etapa": txt("secao_eletrica"),
            "tipo": "eletrica",
            "rolos_conduite": res['rolos_conduite'],
            "fios": {str(b): f['rolos'] for b, f in res['fios'].items()},
            "caixas_4x2": res['caixas_4x2'], "caixas_octogonais": res['caixas_octogonais'],
            "tomadas": tomadas, "interruptores": interruptores,
            "custo_mat": custo_mat, "custo_mo": 0.0, "custo_total": custo_mat,
            "resumo_texto": texto_res,
            "inputs": inputs,
        }
        return {"texto": texto_res, "resultado": resultado}

    def _calcular_contrapiso(self, e):
        if not (e.get("area") or "").strip() or not (e.get("esp") or "").strip():
            return {"erro": txt("msg_erro_num")}

        area = self._numero(e["area"])
        esp = self._numero(e["esp"])
        perda = self._numero(e.get("perda"), PERDA_PADRAO_CONTRAPISO)

        res = calcular_contrapiso(area_m2=area, espessura_cm=esp, perda_percentual=perda, traco=self.traco["contrapiso"])
        if "erro" in res:
            return {"erro": f"Erro: {res['erro']}"}

        custo_cimento = res['sacos_cimento'] * TABELA_PRECOS_GLOBAL.cimento_50kg
        custo_areia = res['areia_m3'] * TABELA_PRECOS_GLOBAL.areia_m3
        custo_pedra = res['pedra_m3'] * TABELA_PRECOS_GLOBAL.pedra_m3
        custo_mat = custo_cimento + custo_areia + custo_pedra

        texto_res = (
            f"{txt('label_area_contrapiso')}: {fmt_num(res['area_m2'], 2)} m²\n"
            f"{txt('label_traco_curto')}: {res['traco']}\n"
            f"{txt('label_volume')} ({fmt_num(perda, 0)}% perda): {fmt_num(res['volume_com_perda_m3'], 3)} m³\n"
            f"• {txt('label_cimento')}: {res['sacos_cimento']} {txt('un_sacos')} ({fmt_moeda(custo_cimento)})\n"
            f"• {txt('label_areia')}: {fmt_num(res['areia_m3'], 2)} m³ ({fmt_moeda(custo_areia)})\n"
            f"• {txt('label_pedra')}: {fmt_num(res['pedra_m3'], 2)} m³ ({fmt_moeda(custo_pedra)})\n"
            f"\n{txt('label_custo')}: {fmt_moeda(custo_mat)}"
        )

        resultado = {
            "etapa": txt("secao_contrapiso"),
            "tipo": "contrapiso",
            "cimento": res['sacos_cimento'], "areia": res['areia_m3'], "pedra": res['pedra_m3'],
            "custo_mat": custo_mat, "custo_mo": 0.0, "custo_total": custo_mat,
            "resumo_texto": texto_res,
            "inputs": {"area": area, "esp": esp, "perda": perda, "traco": res["traco"]}
        }
        return {"texto": texto_res, "resultado": resultado}

    def _calcular_paredes(self, e):
        if not (e.get("area") or "").strip():
            return {"erro": txt("msg_erro_num")}

        area = self._numero(e["area"])
        vaos = self._numero(e.get("vaos"), 0.0)
        junta = self._numero(e.get("junta"), JUNTA_PADRAO_CM)
        quebra = self._numero(e.get("quebra"), QUEBRA_PADRAO_PERCENTUAL)
        tijolo = self.tijolo["paredes"]
        assent = self.assent["paredes"]

        res = calcular_paredes(
            area_bruta_m2=area, tijolo=tijolo, assentamento=assent,
            desconto_vaos_m2=vaos, junta_cm=junta, quebra_percentual=quebra,
            traco=self.traco["paredes"]
        )
        if "erro" in res:
            return {"erro": f"Erro: {res['erro']}"}

        custo_tijolo = res['unidades'] * res['preco_unitario']
        custo_cimento = res['sacos_cimento'] * TABELA_PRECOS_GLOBAL.cimento_50kg
        custo_cal = res['sacos_cal'] * TABELA_PRECOS_GLOBAL.cal_20kg
        custo_areia = res['areia_m3'] * TABELA_PRECOS_GLOBAL.areia_m3
        custo_mat = custo_tijolo + custo_cimento + custo_cal + custo_areia

        milheiros = fmt_num(res['milheiros'], 2)
        un_milheiro = txt('un_milheiro') if res['milheiros'] == 1 else txt('un_milheiros')
        texto_res = f"{txt('label_area_bruta')}: {fmt_num(res['area_bruta_m2'], 2)} m²\n"
        if res['desconto_vaos_m2'] > 0:
            texto_res += f"{txt('label_vaos')}: {fmt_num(res['desconto_vaos_m2'], 2)} m²\n"
        texto_res += (
            f"{txt('label_area_liquida')}: {fmt_num(res['area_liquida_m2'], 2)} m²\n"
            f"{txt('label_traco_curto')}: {res['traco']}\n"
            f"• {self._rotulo_tijolo(tijolo)}: {res['unidades']} {txt('un_unidades')} "
            f"({milheiros} {un_milheiro}) ({fmt_moeda(custo_tijolo)})\n"
            f"• {txt('label_cimento')}: {res['sacos_cimento']} {txt('un_sacos')} ({fmt_moeda(custo_cimento)})\n"
            f"• {txt('label_cal')}: {res['sacos_cal']} {txt('un_sacos_cal')} ({fmt_moeda(custo_cal)})\n"
            f"• {txt('label_areia')}: {fmt_num(res['areia_m3'], 2)} m³ ({fmt_moeda(custo_areia)})\n"
            f"\n{txt('label_custo')}: {fmt_moeda(custo_mat)}"
        )

        resultado = {
            "etapa": txt("secao_paredes"),
            "tipo": "paredes",
            "cimento": res['sacos_cimento'], "cal": res['sacos_cal'], "areia": res['areia_m3'],
            "tijolos": res['unidades'],
            "custo_mat": custo_mat, "custo_mo": 0.0, "custo_total": custo_mat,
            "resumo_texto": texto_res,
            "inputs": {
                "area": area, "vaos": vaos, "junta": junta, "quebra": quebra,
                "tijolo": tijolo, "assent": assent, "traco": res["traco"]
            }
        }
        return {"texto": texto_res, "resultado": resultado}

    def executar_calculo(self, instance=None):
        """Botão Calcular: calcula a aba aberta e mostra o resultado."""
        self._capturar_estado()
        aba = self.aba_atual
        r = self._calcular_aba(aba, self.estado_abas.get(aba, {}))
        if "erro" in r:
            self.textos_resultado.pop(aba, None)
            self._lbl_resultado.text = r["erro"]
            return
        self.textos_resultado[aba] = r["texto"]
        self._lbl_resultado.text = r["texto"]

    # --- USADO PELO HISTÓRICO (visualizar / editar) ---
    @staticmethod
    def _texto_campo(valor) -> str:
        if isinstance(valor, float) and valor.is_integer():
            valor = int(valor)
        return str(valor).replace('.', CONFIG_APP["separador_decimal"])

    def preencher_campos(self, inputs_dict: dict, modo_leitura: bool = False, tipo: str = "brocas"):
        """Carrega os valores salvos de UMA aba (o Histórico chama uma vez por aba)."""
        aba = tipo if tipo in ABAS_ORDEM else ABAS_ORDEM[0]
        self.modo_somente_leitura = modo_leitura
        self.aba_atual = aba

        tabela_tracos, traco_padrao, _ = self._tabela_traco(aba)
        traco = inputs_dict.get("traco")
        self.traco[aba] = traco if traco in tabela_tracos else traco_padrao
        if aba in self.tijolo:
            self.tijolo[aba] = inputs_dict.get("tijolo") if inputs_dict.get("tijolo") in TIJOLOS else TIJOLO_PADRAO
        if aba in self.assent:
            self.assent[aba] = inputs_dict.get("assent") if inputs_dict.get("assent") in ASSENTAMENTOS else ASSENTAMENTO_PADRAO
        if aba in self.bitola:
            bitola = inputs_dict.get("bitola")
            self.bitola[aba] = bitola if bitola in BITOLAS_LONGITUDINAL else BITOLA_PADRAO
        if aba in self.imperm:
            self.imperm[aba] = bool(inputs_dict.get("imperm"))
        if aba in self.dois_lados:
            self.dois_lados[aba] = bool(inputs_dict.get("dois_lados"))
        if aba in self.chapisco:
            self.chapisco[aba] = bool(inputs_dict.get("chapisco"))
        if aba in self.argamassa:
            padrao = ARGAMASSA_PADRAO_PISO if aba == "piso" else ARGAMASSA_PADRAO_AZULEJO
            self.argamassa[aba] = inputs_dict.get("argamassa") if inputs_dict.get("argamassa") in TIPOS_ARGAMASSA else padrao
        if aba == "laje":
            tipo = inputs_dict.get("tipo_laje")
            self.laje_tipo = tipo if tipo in TIPOS_LAJE else TIPO_LAJE_PADRAO
            ench = inputs_dict.get("enchimento")
            self.laje_enchimento = ench if ench in ENCHIMENTOS else ENCHIMENTO_PADRAO
        if aba == "telhado":
            telha = inputs_dict.get("tipo_telha")
            self.telha_tipo = telha if telha in TIPOS_TELHA else TIPO_TELHA_PADRAO
            self.madeiramento[aba] = bool(inputs_dict.get("madeiramento"))
        if aba == "pintura":
            self.selador[aba] = bool(inputs_dict.get("selador"))
            self.fundo[aba] = bool(inputs_dict.get("fundo"))
            massa = inputs_dict.get("massa")
            self.massa_tipo = massa if massa in TIPOS_MASSA else "nenhuma"
        if aba == "esquadrias":
            self.esquadrias_itens = [dict(item) for item in inputs_dict.get("itens", [])]
            for chave in self.esq_fixacao:
                self.esq_fixacao[chave] = bool(inputs_dict.get(chave))

        estado = {}
        for chave in CAMPOS_ABA[aba]:
            if chave in inputs_dict:
                valor = inputs_dict[chave]
                estado[chave] = "" if (chave == "esp_estribo" and not valor) else self._texto_campo(valor)
            elif chave == "esp_estribo":
                estado[chave] = ""  # orçamento antigo: não tinha estribos
        self.estado_abas[aba] = estado
        self._campos = {}  # não deixa os campos antigos sobrescreverem o que foi carregado
        self.montar_tela()

    def voltar_home(self, instance):
        destino = "history" if self.origem == "history" else "home"
        self.origem = "home"
        self.manager.current = destino

    def finalizar_e_ir_resumo(self, instance=None):
        """Soma todas as abas preenchidas (aba em branco é ignorada) e abre o Resumo."""
        self._capturar_estado()
        itens = []
        for aba in ABAS_ORDEM:
            estado = self.estado_abas.get(aba) or {}
            if not self._aba_iniciada(aba, estado):
                continue
            r = self._calcular_aba(aba, estado)
            if "erro" in r:
                if aba != self.aba_atual:
                    self.trocar_aba(aba)
                self._lbl_resultado.text = r["erro"]
                return
            self.textos_resultado[aba] = r["texto"]
            itens.append(r["resultado"])

        if not itens:
            self._lbl_resultado.text = txt("msg_inicial")
            return

        ORCAMENTO_FINAL.clear()
        ORCAMENTO_FINAL.extend(itens)
        summary_screen = self.manager.get_screen("summary")
        summary_screen.atualizar_resumo()
        self.manager.current = "summary"