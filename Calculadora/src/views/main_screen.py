from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDButton, MDButtonText, MDIconButton
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogHeadlineText,
    MDDialogSupportingText,
    MDDialogButtonContainer,
    MDDialogContentContainer
)

from src.calculators.brocas import calcular_brocas
from src.calculators.baldrame import calcular_baldrame
from src.models.material import TabelaPrecos
from src.models.database import (
    salvar_orcamento,
    listar_orcamentos,
    atualizar_nome_orcamento,
    excluir_orcamento,
    duplicar_orcamento,
    cadastrar_usuario,     
    autenticar_usuario,
    quantidade_orcamentos_salvos
)

from kivymd.uix.card import MDCard
from kivymd.uix.divider import MDDivider
from kivymd.uix.widget import MDWidget
from kivymd.uix.tab import (
    MDTabsPrimary,
    MDTabsItem,
    MDTabsItemText,
    MDTabsItemIcon,
)

# Dicionário completo com todas as chaves traduzidas
TEXTOS = {
    "pt": {
        "titulo_app": "BuildCalc Pro",
        "subtitulo_app": "Calculadora Profissional de Materiais e Orçamentos",
        "btn_iniciar": "Iniciar Orçamento",
        "btn_precos": "Configurar Preços da Região",
        "btn_historico": "Histórico de Orçamentos",
        "btn_idioma": "PT",
        "btn_pais": "BR (R$)",
        "btn_estado": "SP",
        "btn_tema": "Escuro",
        "btn_tema_light": "Claro",
        "btn_voltar": "<- Voltar",
        "titulo_calculadora": "Calculadora de Materiais",
        "aba_brocas": "Brocas",
        "aba_baldrame": "Baldrame",
        "secao_dimensoes": "Dimensões (Obrigatório)",
        "titulo_brocas": "Brocas / Estacas",
        "secao_brocas": "1. Brocas / Estacas (Obrigatório)",
        "secao_opcional": "Opções Avançadas (Opcional)",
        "hint_qtd": "Quantidade de brocas (ex: 10)",
        "hint_prof": "Profundidade em metros (ex: 3,0)",
        "hint_diam": "Diâmetro em cm (ex: 20)",
        "hint_perda": "Taxa de Perda % (opcional, ex: 10)",
        "hint_barras": "Nº de barras por broca (opcional, ex: 4)",
        "hint_mo": "Mão de obra por metro (opcional, ex: 25,00)",
        "btn_calcular": "Calcular Material e Valor",
        "btn_finalizar": "Ir para o Resumo ->",
        "msg_inicial": "Preencha os dados e clique em calcular.",
        "msg_erro_num": "Por favor, digite números válidos nos campos obrigatórios!",
        "label_volume": "Volume Total",
        "label_cimento": "Cimento",
        "label_areia": "Areia",
        "label_pedra": "Pedra",
        "label_aco": "Aço/Ferragem",
        "label_mo": "Mão de Obra",
        "label_custo": "Custo Estimado da Etapa",
        "un_sacos": "sacos",
        "titulo_resumo": "Orçamento Consolidado",
        "lbl_resumo_vazio": "Nenhum cálculo finalizado ainda.",
        "btn_novo_calc": "<- Voltar aos Cálculos",
        "btn_pdf": "Gerar / Exportar PDF",
        "btn_editar": "Editar Cálculos",
        "btn_salvar_hist": "Salvar no Histórico",
        "titulo_precos": "Configurar Preços",
        "btn_salvar_precos": "Salvar e Voltar",
        "titulo_historico": "Histórico de Orçamentos",
        "lbl_hist_vazio": "Nenhum orçamento salvo no histórico.",
        "login_titulo": "Bem-vindo ao BuildCalc",
        "login_sub": "Faça login ou crie sua conta para salvar orçamentos",
        "hint_nome": "Seu Nome",
        "hint_email": "E-mail",
        "hint_senha": "Senha",
        "hint_conf_senha": "Confirmar Senha",
        "btn_entrar": "Entrar",
        "btn_cadastrar": "Cadastrar",
        "btn_criar_conta": "Criar nova conta",
        "btn_ja_conta": "Já tenho uma conta",
        "btn_visitante": "Continuar como Visitante ->",
        "dialog_salvar_titulo": "Salvar no Histórico",
        "dialog_salvar_sub": "Digite o nome da obra ou cliente para salvar:",
        "hint_nome_obra": "Nome da Obra (ex: Casa Ana)",
        "btn_cancelar": "Cancelar",
        "btn_salvar": "Salvar",
        "lbl_data": "Data",
        "lbl_uf": "UF",
        "lbl_valor_total": "Valor Total",
        "btn_vis": "Visualizar",
        "btn_edit": "Editar",
        "btn_dup": "Duplicar",
        "btn_ren": "Renomear",
        "btn_exc": "Excluir",
        "dialog_visitante_titulo": "Modo Visitante",
        "dialog_visitante_sub": "Você está usando o app sem login. Crie uma conta para salvar seus orçamentos!",
        "btn_login_criar": "Fazer Login / Criar Conta",
        "btn_fechar": "Fechar",
        "btn_sair": "Sair da Conta",
        "hint_cimento": "Saco de Cimento (50kg)",
        "hint_areia": "Areia (m³)",
        "hint_brita": "Brita (m³)",
        "hint_mao_obra": "Mão de Obra (m²)",
        "titulo_baldrame": "Cálculo de Baldrame",
        "secao_baldrame": "Dimensões da Viga Baldrame",
        "hint_comprimento": "Comprimento total em metros (ex: 12,5)",
        "hint_largura": "Largura da viga em cm (ex: 20)",
        "hint_altura": "Altura da viga em cm (ex: 30)"
    },
    "en": {
        "titulo_app": "BuildCalc Pro",
        "subtitulo_app": "Professional Material & Cost Estimator",
        "btn_iniciar": "Start Estimate",
        "btn_precos": "Configure Region Prices",
        "btn_historico": "Estimate History",
        "btn_idioma": "EN",
        "btn_pais": "US ($)",
        "btn_estado": "NY",
        "btn_tema": "Dark",
        "btn_tema_light": "Light",
        "btn_voltar": "<- Back",
        "titulo_calculadora": "Materials Calculator",
        "aba_brocas": "Drilled Shafts",
        "aba_baldrame": "Grade Beam",
        "secao_dimensoes": "Dimensions (Required)",
        "titulo_brocas": "Drilled Shafts / Piles",
        "secao_brocas": "1. Drilled Shafts / Piles (Required)",
        "secao_opcional": "Advanced Options (Optional)",
        "hint_qtd": "Quantity of shafts (ex: 10)",
        "hint_prof": "Depth in meters (ex: 3.0)",
        "hint_diam": "Diameter in cm (ex: 20)",
        "hint_perda": "Waste Rate % (optional, ex: 10)",
        "hint_barras": "Rebars per shaft (optional, ex: 4)",
        "hint_mo": "Labor cost per meter (optional, ex: 25.00)",
        "btn_calcular": "Calculate Materials & Price",
        "btn_finalizar": "View Summary ->",
        "msg_inicial": "Fill in the fields and click calculate.",
        "msg_erro_num": "Please enter valid numbers in required fields!",
        "label_volume": "Total Volume",
        "label_cimento": "Cement",
        "label_areia": "Sand",
        "label_pedra": "Gravel",
        "label_aco": "Steel Rebar",
        "label_mo": "Labor Cost",
        "label_custo": "Estimated Stage Cost",
        "un_sacos": "bags",
        "titulo_resumo": "Consolidated Estimate",
        "lbl_resumo_vazio": "No calculation finalized yet.",
        "btn_novo_calc": "<- Back to Calculations",
        "btn_pdf": "Export / Share PDF",
        "btn_editar": "Edit Calculations",
        "btn_salvar_hist": "Save to History",
        "titulo_precos": "Region Price Settings",
        "btn_salvar_precos": "Save & Back",
        "titulo_historico": "Estimate History",
        "lbl_hist_vazio": "No saved estimates in history.",
        "login_titulo": "Welcome to BuildCalc",
        "login_sub": "Log in or create an account to save estimates",
        "hint_nome": "Your Name",
        "hint_email": "Email",
        "hint_senha": "Password",
        "hint_conf_senha": "Confirm Password",
        "btn_entrar": "Sign In",
        "btn_cadastrar": "Sign Up",
        "btn_criar_conta": "Create new account",
        "btn_ja_conta": "Already have an account",
        "btn_visitante": "Continue as Guest ->",
        "dialog_salvar_titulo": "Save to History",
        "dialog_salvar_sub": "Enter client or project name to save:",
        "hint_nome_obra": "Project Name (ex: Ana's House)",
        "btn_cancelar": "Cancel",
        "btn_salvar": "Save",
        "lbl_data": "Date",
        "lbl_uf": "State",
        "lbl_valor_total": "Total Amount",
        "btn_vis": "View",
        "btn_edit": "Edit",
        "btn_dup": "Duplicate",
        "btn_ren": "Rename",
        "btn_exc": "Delete",
        "dialog_visitante_titulo": "Guest Mode",
        "dialog_visitante_sub": "You are using the app as a guest. Create an account to save your estimates!",
        "btn_login_criar": "Log In / Sign Up",
        "btn_fechar": "Close",
        "btn_sair": "Sign Out",
        "hint_cimento": "Cement Bag (50kg)",
        "hint_areia": "Sand (m³)",
        "hint_brita": "Gravel (m³)",
        "hint_mao_obra": "Labor Cost (m²)",
        "titulo_baldrame": "Grade Beam Calculation",
        "secao_baldrame": "Grade Beam Dimensions",
        "hint_comprimento": "Total length in meters (ex: 12.5)",
        "hint_largura": "Beam width in cm (ex: 20)",
        "hint_altura": "Beam height in cm (ex: 30)"
    }
}

CONFIG_APP = {
    "pais": "BR (R$)",
    "estado": "SP",
    "idioma": "pt",
    "tema": "Escuro",  
    "cimento": "32.00",
    "areia": "110.00",
    "brita": "95.00",
    "mao_obra": "80.00",
    "separador_decimal": ",",
    "moeda": "R$"
}

PRECOS_EUA = {
    "cimento": 12.00,
    "areia": 45.00,
    "brita": 40.00,
    "aco": 2.50,
    "mao_obra": 15.00
}

PRECOS_BR = {
    "cimento": 32.00,
    "areia": 110.00,
    "brita": 95.00,
    "aco": 9.50,
    "mao_obra": 25.00
}

ESTADOS_BR = ["SP", "RJ", "MG", "BA", "PR", "CE"]
ESTADOS_US = ["NY", "CA", "FL", "TX", "IL", "GA"]
USUARIO_LOGADO = None

TABELA_PRECOS_GLOBAL = TabelaPrecos()
ORCAMENTO_FINAL = []

def txt(chave: str) -> str:
    lang = CONFIG_APP.get("idioma", "pt").lower()
    dicionario_lang = TEXTOS.get(lang, TEXTOS.get("pt", {}))
    return dicionario_lang.get(chave, chave)

def fmt_moeda(valor: float) -> str:
    sep = CONFIG_APP["separador_decimal"]
    moeda = CONFIG_APP["moeda"]
    texto = f"{valor:.2f}".replace('.', sep)
    return f"{moeda} {texto}"

def fmt_num(valor: float, casas: int = 2) -> str:
    sep = CONFIG_APP["separador_decimal"]
    return f"{valor:.{casas}f}".replace('.', sep)

# --- TELA DE LOGIN / CADASTRO ---
class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "login"
        self.md_bg_color = self.theme_cls.backgroundColor
        self.modo_cadastro = False
        
        self.layout_main = MDBoxLayout(orientation="vertical", padding="16dp", spacing="10dp")
        self.add_widget(self.layout_main)
        self.montar_tela()

    def montar_tela(self):
        self.layout_main.clear_widgets()
        
        top_bar = MDBoxLayout(size_hint_y=None, height="40dp")
        espacador = MDWidget()
        self.btn_settings = MDIconButton(
            icon="cog",
            pos_hint={"center_y": 0.5},
            on_release=self.ir_para_configuracoes
        )
        top_bar.add_widget(espacador)
        top_bar.add_widget(self.btn_settings)
        
        self.lbl_titulo = MDLabel(
            text=txt("btn_cadastrar") if self.modo_cadastro else txt("login_titulo"),
            font_style="Headline",
            role="small",
            bold=True,
            halign="center",
            theme_text_color="Primary"
        )
        self.lbl_sub = MDLabel(
            text=txt("login_sub"),
            font_style="Body",
            role="medium",
            halign="center",
            theme_text_color="Secondary"
        )
        
        self.in_nome = MDTextField(
            MDTextFieldHintText(text=txt("hint_nome")),
            mode="outlined",
            write_tab=False
        )
        
        self.in_email = MDTextField(
            MDTextFieldHintText(text=txt("hint_email")),
            mode="outlined",
            write_tab=False
        )
        
        box_senha = MDBoxLayout(orientation="horizontal", spacing="4dp", size_hint_y=None, height="56dp")
        self.in_senha = MDTextField(
            MDTextFieldHintText(text=txt("hint_senha")),
            mode="outlined",
            password=True,
            write_tab=False
        )
        self.btn_olho = MDIconButton(
            icon="eye-off",
            pos_hint={"center_y": 0.5},
            on_release=self.alternar_visibilidade_senha
        )
        box_senha.add_widget(self.in_senha)
        box_senha.add_widget(self.btn_olho)
        
        self.box_conf_senha = MDBoxLayout(orientation="horizontal", spacing="4dp", size_hint_y=None, height="56dp")
        self.in_conf_senha = MDTextField(
            MDTextFieldHintText(text=txt("hint_conf_senha")),
            mode="outlined",
            password=True,
            write_tab=False
        )
        self.btn_olho_conf = MDIconButton(
            icon="eye-off",
            pos_hint={"center_y": 0.5},
            on_release=self.alternar_visibilidade_conf_senha
        )
        self.box_conf_senha.add_widget(self.in_conf_senha)
        self.box_conf_senha.add_widget(self.btn_olho_conf)
        
        if not self.modo_cadastro:
            self.in_nome.opacity = 0
            self.in_nome.disabled = True
            self.box_conf_senha.opacity = 0
            self.box_conf_senha.disabled = True
        
        self.btn_acao = MDButton(
            MDButtonText(text=txt("btn_cadastrar") if self.modo_cadastro else txt("btn_entrar")),
            pos_hint={"center_x": 0.5},
            on_release=self.executar_acao
        )
        
        self.btn_alternar = MDButton(
            MDButtonText(text=txt("btn_ja_conta") if self.modo_cadastro else txt("btn_criar_conta")),
            pos_hint={"center_x": 0.5},
            on_release=self.alternar_modo
        )
        
        self.btn_visitante = MDButton(
            MDButtonText(text=txt("btn_visitante")),
            pos_hint={"center_x": 0.5},
            on_release=self.entrar_visitante
        )
        
        self.lbl_status = MDLabel(text="", halign="center", theme_text_color="Error")
        
        self.layout_main.add_widget(top_bar)
        self.layout_main.add_widget(self.lbl_titulo)
        self.layout_main.add_widget(self.lbl_sub)
        self.layout_main.add_widget(self.in_nome)
        self.layout_main.add_widget(self.in_email)
        self.layout_main.add_widget(box_senha)
        self.layout_main.add_widget(self.box_conf_senha)
        self.layout_main.add_widget(self.lbl_status)
        self.layout_main.add_widget(self.btn_acao)
        self.layout_main.add_widget(self.btn_alternar)
        self.layout_main.add_widget(self.btn_visitante)

    def atualizar_interface(self):
        self.montar_tela()

    def ir_para_configuracoes(self, instance):
        settings_screen = self.manager.get_screen("settings")
        settings_screen.atualizar_interface()
        self.manager.current = "settings"

    def alternar_visibilidade_senha(self, instance):
        self.in_senha.password = not self.in_senha.password
        self.btn_olho.icon = "eye" if not self.in_senha.password else "eye-off"

    def alternar_visibilidade_conf_senha(self, instance):
        self.in_conf_senha.password = not self.in_conf_senha.password
        self.btn_olho_conf.icon = "eye" if not self.in_conf_senha.password else "eye-off"

    def alternar_modo(self, instance):
        self.modo_cadastro = not self.modo_cadastro
        self.montar_tela()

    def executar_acao(self, instance):
        global USUARIO_LOGADO
        email = self.in_email.text.strip()
        senha = self.in_senha.text.strip()
        
        if not email or not senha:
            self.lbl_status.text = "Preencha e-mail e senha!"
            return
            
        if self.modo_cadastro:
            nome = self.in_nome.text.strip()
            conf_senha = self.in_conf_senha.text.strip()
            
            if not nome:
                self.lbl_status.text = "Digite o seu nome!"
                return
                
            if senha != conf_senha:
                self.lbl_status.text = "As senhas não coincidem!"
                return
                
            sucesso = cadastrar_usuario(nome, email, senha)
            if sucesso:
                self.lbl_status.text = "Conta criada com sucesso! Faça login."
                self.alternar_modo(None)
            else:
                self.lbl_status.text = "Este e-mail já está cadastrado!"
        else:
            usr = autenticar_usuario(email, senha)
            if usr:
                USUARIO_LOGADO = usr
                home_screen = self.manager.get_screen("home")
                home_screen.atualizar_avatar()
                self.manager.current = "home"
            else:
                self.lbl_status.text = "E-mail ou senha incorretos!"

    def entrar_visitante(self, instance):
        global USUARIO_LOGADO
        USUARIO_LOGADO = None
        home_screen = self.manager.get_screen("home")
        home_screen.atualizar_avatar()
        self.manager.current = "home"

# --- TELA INICIAL (HOME) ---
class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "home"
        self.md_bg_color = self.theme_cls.backgroundColor
        self.dialog_perfil = None
        
        layout_main = MDBoxLayout(orientation="vertical", padding="16dp", spacing="12dp")
        
        top_bar = MDBoxLayout(size_hint_y=None, height="40dp", spacing="8dp")
        espacador = MDWidget()
        
        self.btn_avatar = MDButton(
            MDButtonText(text="V"),
            style="tonal",
            pos_hint={"center_y": 0.5},
            on_release=self.abrir_menu_perfil
        )
        
        top_bar.add_widget(espacador)
        top_bar.add_widget(self.btn_avatar)
        
        center_box = MDBoxLayout(orientation="vertical", spacing="16dp", padding=("10dp", "30dp", "10dp", "10dp"))
        
        self.lbl_titulo = MDLabel(
            text=txt("titulo_app"),
            halign="center",
            font_style="Headline",
            role="medium",
            bold=True,
            theme_text_color="Primary"
        )
        self.lbl_subtitulo = MDLabel(
            text=txt("subtitulo_app"),
            halign="center",
            font_style="Title",
            role="small",
            theme_text_color="Secondary"
        )
        
        self.btn_iniciar = MDButton(
            MDButtonText(text=txt("btn_iniciar")),
            pos_hint={"center_x": 0.5},
            on_release=self.ir_para_calculadora
        )
        self.btn_historico = MDButton(
            MDButtonText(text=txt("btn_historico")),
            pos_hint={"center_x": 0.5},
            on_release=self.ir_para_historico
        )
        
        center_box.add_widget(self.lbl_titulo)
        center_box.add_widget(self.lbl_subtitulo)
        center_box.add_widget(self.btn_iniciar)
        center_box.add_widget(self.btn_historico)
        
        layout_main.add_widget(top_bar)
        layout_main.add_widget(center_box)
        self.add_widget(layout_main)

    def atualizar_avatar(self):
        if USUARIO_LOGADO and USUARIO_LOGADO.get("nome"):
            inicial = USUARIO_LOGADO["nome"][0].upper()
            self.btn_avatar.children[0].text = inicial
        else:
            self.btn_avatar.children[0].text = "V"
            
    def atualizar_interface(self):
        self.lbl_titulo.text = txt("titulo_app")
        self.lbl_subtitulo.text = txt("subtitulo_app")
        self.btn_iniciar.children[0].text = txt("btn_iniciar")
        self.btn_historico.children[0].text = txt("btn_historico")
        self.atualizar_avatar()

    def abrir_menu_perfil(self, instance):
        if USUARIO_LOGADO:
            nome = USUARIO_LOGADO["nome"]
            email = USUARIO_LOGADO["email"]
            plano = USUARIO_LOGADO.get("plano", "Gratuito")
            
            self.dialog_perfil = MDDialog(
                MDDialogHeadlineText(text=f"Olá, {nome}!"),
                MDDialogSupportingText(text=f"E-mail: {email}\nPlano Atual: {plano} (limite: 5)"),
                MDDialogButtonContainer(
                    MDButton(MDButtonText(text=txt("btn_sair")), on_release=self.deslogar),
                    MDButton(MDButtonText(text=txt("btn_fechar")), on_release=lambda x: self.dialog_perfil.dismiss())
                )
            )
        else:
            self.dialog_perfil = MDDialog(
                MDDialogHeadlineText(text=txt("dialog_visitante_titulo")),
                MDDialogSupportingText(text=txt("dialog_visitante_sub")),
                MDDialogButtonContainer(
                    MDButton(MDButtonText(text=txt("btn_login_criar")), on_release=self.ir_para_login),
                    MDButton(MDButtonText(text=txt("btn_fechar")), on_release=lambda x: self.dialog_perfil.dismiss())
                )
            )
        self.dialog_perfil.open()

    def deslogar(self, instance):
        global USUARIO_LOGADO
        USUARIO_LOGADO = None
        if self.dialog_perfil:
            self.dialog_perfil.dismiss()
        self.atualizar_avatar()
        self.manager.current = "login"

    def ir_para_login(self, instance):
        if self.dialog_perfil:
            self.dialog_perfil.dismiss()
        self.manager.current = "login"

    def ir_para_calculadora(self, instance):
        ORCAMENTO_FINAL.clear()
        calc_screen = self.manager.get_screen("calculator")
        calc_screen.ultimo_resultado = None
        calc_screen.modo_somente_leitura = False
        calc_screen.origem = "home"
        calc_screen.aba_atual = "brocas"
        calc_screen.atualizar_interface()
        for child in calc_screen.layout_principal.children:
            if isinstance(child, MDScrollView):
                child.scroll_y = 1.0
        self.manager.current = "calculator"

    def ir_para_historico(self, instance):
        hist_screen = self.manager.get_screen("history")
        hist_screen.carregar_historico()
        self.manager.current = "history"


# --- TELA DE CÁLCULO COM ABAS (Navegação Interna) ---
class CalculatorScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "calculator"
        self.aba_atual = "brocas"
        self.origem = "home"
        self.md_bg_color = self.theme_cls.backgroundColor
        self.ultimo_resultado = None
        self.modo_somente_leitura = False
        
        self.layout_principal = MDBoxLayout(orientation="vertical", padding="16dp", spacing="12dp")
        self.add_widget(self.layout_principal)
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

        # --- CONTAINER DE ABAS (MDTabs) --
        # Se estiver usando KivyMD 3.0 com MDTabsPrimary / MDTabsItem:
        box_tabs = MDBoxLayout(size_hint_y=None, height="48dp", spacing="8dp")
        
        self.btn_tab_brocas = MDButton(
            MDButtonText(text=txt("aba_brocas")), 
            style="outlined", 
            disabled=self.modo_somente_leitura,
            on_release=lambda x: self.trocar_aba("brocas")
        )
        self.btn_tab_baldrame = MDButton(
            MDButtonText(text=txt("aba_baldrame")), 
            style="outlined", 
            disabled=self.modo_somente_leitura,
            on_release=lambda x: self.trocar_aba("baldrame")
        )
        
        box_tabs.add_widget(self.btn_tab_brocas)
        box_tabs.add_widget(self.btn_tab_baldrame)
        self.layout_principal.add_widget(box_tabs)

        # --- ÁREA DINÂMICA (Conteúdo das Abas) ---
        self.container_conteudo = MDBoxLayout(orientation="vertical")
        self.layout_principal.add_widget(self.container_conteudo)

        # Reabre a aba que estava ativa (brocas por padrão)
        self.trocar_aba(self.aba_atual)

    def atualizar_interface(self):
        self.montar_tela()

    def trocar_aba(self, aba_nome):
        self.aba_atual = aba_nome
        self.ultimo_resultado = None
        self.container_conteudo.clear_widgets()

        if aba_nome == "brocas":
            self.container_conteudo.add_widget(self.montar_conteudo_brocas())
        elif aba_nome == "baldrame":
            self.container_conteudo.add_widget(self.montar_conteudo_baldrame())

    # ==========================================
    # CONTEÚDO DA ABA 1: BROCAS
    # ==========================================
    def montar_conteudo_brocas(self):
        scroll = MDScrollView()
        box_form = MDBoxLayout(orientation="vertical", spacing="16dp", padding="8dp", size_hint_y=None)
        box_form.bind(minimum_height=box_form.setter('height'))

        self.in_qtd = MDTextField(MDTextFieldHintText(text=txt("hint_qtd")), mode="outlined", write_tab=False, readonly=self.modo_somente_leitura)
        self.in_prof = MDTextField(MDTextFieldHintText(text=txt("hint_prof")), mode="outlined", write_tab=False, readonly=self.modo_somente_leitura)
        self.in_diam = MDTextField(MDTextFieldHintText(text=txt("hint_diam")), mode="outlined", write_tab=False, readonly=self.modo_somente_leitura)

        self.lbl_opcional = MDLabel(text=txt("secao_opcional"), font_style="Title", role="small", bold=True, theme_text_color="Primary")
        self.in_perda = MDTextField(MDTextFieldHintText(text=txt("hint_perda")), mode="outlined", write_tab=False, readonly=self.modo_somente_leitura)
        self.in_barras = MDTextField(MDTextFieldHintText(text=txt("hint_barras")), mode="outlined", write_tab=False, readonly=self.modo_somente_leitura)
        self.in_mo = MDTextField(MDTextFieldHintText(text=txt("hint_mo")), mode="outlined", write_tab=False, readonly=self.modo_somente_leitura)

        self.lbl_obrigatorio = MDLabel(text=txt("secao_dimensoes"), font_style="Title", role="small", bold=True, theme_text_color="Primary")
        box_form.add_widget(self.lbl_obrigatorio)
        box_form.add_widget(self.in_qtd)
        box_form.add_widget(self.in_prof)
        box_form.add_widget(self.in_diam)
        box_form.add_widget(self.lbl_opcional)
        box_form.add_widget(self.in_perda)
        box_form.add_widget(self.in_barras)
        box_form.add_widget(self.in_mo)

        if not self.modo_somente_leitura:
            self.btn_calcular = MDButton(MDButtonText(text=txt("btn_calcular")), pos_hint={"center_x": 0.5}, on_release=self.executar_calculo_brocas)
            box_form.add_widget(self.btn_calcular)

        box_resultado = MDBoxLayout(orientation="vertical", spacing="12dp", padding=("0dp", "16dp", "0dp", "0dp"), size_hint_y=None)
        box_resultado.bind(minimum_height=box_resultado.setter('height'))

        self.lbl_resultado = MDLabel(text=txt("msg_inicial"), theme_text_color="Secondary", size_hint_y=None)
        self.lbl_resultado.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))

        box_resultado.add_widget(self.lbl_resultado)

        if not self.modo_somente_leitura:
            self.btn_finalizar = MDButton(MDButtonText(text=txt("btn_finalizar")), pos_hint={"center_x": 0.5}, on_release=self.finalizar_e_ir_resumo)
            box_resultado.add_widget(self.btn_finalizar)

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

        self.in_bal_comp = MDTextField(MDTextFieldHintText(text=txt("hint_comprimento")), mode="outlined", write_tab=False, readonly=self.modo_somente_leitura)
        self.in_bal_larg = MDTextField(MDTextFieldHintText(text=txt("hint_largura")), mode="outlined", write_tab=False, readonly=self.modo_somente_leitura)
        self.in_bal_alt = MDTextField(MDTextFieldHintText(text=txt("hint_altura")), mode="outlined", write_tab=False, readonly=self.modo_somente_leitura)

        self.lbl_opcional_bal = MDLabel(text=txt("secao_opcional"), font_style="Title", role="small", bold=True, theme_text_color="Primary")
        self.in_bal_perda = MDTextField(MDTextFieldHintText(text=txt("hint_perda")), mode="outlined", write_tab=False, readonly=self.modo_somente_leitura)
        self.in_bal_mo = MDTextField(MDTextFieldHintText(text=txt("hint_mo")), mode="outlined", write_tab=False, readonly=self.modo_somente_leitura)

        self.lbl_obrigatorio_bal = MDLabel(text=txt("secao_dimensoes"), font_style="Title", role="small", bold=True, theme_text_color="Primary")
        box_form.add_widget(self.lbl_obrigatorio_bal)
        box_form.add_widget(self.in_bal_comp)
        box_form.add_widget(self.in_bal_larg)
        box_form.add_widget(self.in_bal_alt)
        box_form.add_widget(self.lbl_opcional_bal)
        box_form.add_widget(self.in_bal_perda)
        box_form.add_widget(self.in_bal_mo)

        if not self.modo_somente_leitura:
            self.btn_calc_bal = MDButton(MDButtonText(text=txt("btn_calcular")), pos_hint={"center_x": 0.5}, on_release=self.executar_calculo_baldrame)
            box_form.add_widget(self.btn_calc_bal)

        box_res = MDBoxLayout(orientation="vertical", spacing="12dp", padding=("0dp", "16dp", "0dp", "0dp"), size_hint_y=None)
        box_res.bind(minimum_height=box_res.setter('height'))

        self.lbl_res_baldrame = MDLabel(text=txt("msg_inicial"), theme_text_color="Secondary", size_hint_y=None)
        self.lbl_res_baldrame.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))

        box_res.add_widget(self.lbl_res_baldrame)

        if not self.modo_somente_leitura:
            self.btn_fin_bal = MDButton(MDButtonText(text=txt("btn_finalizar")), pos_hint={"center_x": 0.5}, on_release=self.finalizar_e_ir_resumo)
            box_res.add_widget(self.btn_fin_bal)

        box_form.add_widget(box_res)
        scroll.add_widget(box_form)
        return scroll

    # --- EXECUÇÃO DOS CÁLCULOS ---
    def executar_calculo_brocas(self, instance):
        try:
            t_qtd = self.in_qtd.text.strip()
            t_prof = self.in_prof.text.strip()
            t_diam = self.in_diam.text.strip()
            
            if not t_qtd or not t_prof or not t_diam:
                self.lbl_resultado.text = txt("msg_erro_num")
                return
                
            qtd = int(t_qtd)
            prof = float(t_prof.replace(',', '.'))
            diam = float(t_diam.replace(',', '.'))
            
            t_perda = self.in_perda.text.strip()
            perda = float(t_perda.replace(',', '.')) if t_perda else 10.0
            t_barras = self.in_barras.text.strip()
            num_barras = int(t_barras) if t_barras else 0
            t_mo = self.in_mo.text.strip()
            preco_mo = float(t_mo.replace(',', '.')) if t_mo else 0.0
            
            res = calcular_brocas(
                quantidade=qtd, profundidade_m=prof, diametro_cm=diam,
                perda_percentual=perda, incluir_ferragem=(num_barras > 0),
                num_barras_longitudinais=num_barras, preco_mao_obra_metro=preco_mo
            )
            
            if "erro" in res:
                self.lbl_resultado.text = f"Erro: {res['erro']}"
            else:
                custo_cimento = res['sacos_cimento'] * TABELA_PRECOS_GLOBAL.cimento_50kg
                custo_areia = res['areia_m3'] * TABELA_PRECOS_GLOBAL.areia_m3
                custo_pedra = res['pedra_m3'] * TABELA_PRECOS_GLOBAL.pedra_m3
                custo_aco = res['quilos_aco'] * TABELA_PRECOS_GLOBAL.aco_kg if res['incluiu_ferragem'] else 0.0
                custo_mo = res['custo_mao_obra']
                custo_mat = custo_cimento + custo_areia + custo_pedra + custo_aco
                custo_total = custo_mat + custo_mo
                
                texto_res = (
                    f"{txt('label_volume')} ({fmt_num(res['perda_percentual'], 0)}% perda): {fmt_num(res['volume_com_perda_m3'], 3)} m³\n"
                    f"• {txt('label_cimento')}: {res['sacos_cimento']} {txt('un_sacos')} ({fmt_moeda(custo_cimento)})\n"
                    f"• {txt('label_areia')}: {fmt_num(res['areia_m3'], 2)} m³ ({fmt_moeda(custo_areia)})\n"
                    f"• {txt('label_pedra')}: {fmt_num(res['pedra_m3'], 2)} m³ ({fmt_moeda(custo_pedra)})\n"
                )
                if res['incluiu_ferragem']:
                    texto_res += f"• Aço: {fmt_num(res['quilos_aco'], 1)} kg ({res['barras_12m']} barras 12m)\n  {fmt_moeda(custo_aco)}\n"
                if custo_mo > 0:
                    texto_res += f"• {txt('label_mo')}: {fmt_num(res['total_metros_escavados'], 1)}m ({fmt_moeda(custo_mo)})\n"
                
                texto_res += f"\n{txt('label_custo')}: {fmt_moeda(custo_total)}"
                self.lbl_resultado.text = texto_res
                
                self.ultimo_resultado = {
                    "etapa": txt("secao_brocas"),
                    "tipo": "brocas",
                    "inputs": {"qtd": qtd, "prof": prof, "diam": diam, "perda": perda, "barras": num_barras, "mo": preco_mo},
                    "cimento": res['sacos_cimento'], "areia": res['areia_m3'], "pedra": res['pedra_m3'],
                    "aco_kg": res['quilos_aco'], "barras_12m": res['barras_12m'],
                    "custo_mat": custo_mat, "custo_mo": custo_mo, "custo_total": custo_total,
                    "resumo_texto": texto_res
                }
        except ValueError:
            self.lbl_resultado.text = txt("msg_erro_num")

    def executar_calculo_baldrame(self, instance=None):
        self.ultimo_resultado = None
        try:
            t_comp = self.in_bal_comp.text.strip()
            t_larg = self.in_bal_larg.text.strip()
            t_alt = self.in_bal_alt.text.strip()

            if not t_comp or not t_larg or not t_alt:
                self.lbl_res_baldrame.text = txt("msg_erro_num")
                return

            comp = float(t_comp.replace(',', '.'))
            larg = float(t_larg.replace(',', '.'))
            alt = float(t_alt.replace(',', '.'))

            t_perda = self.in_bal_perda.text.strip()
            perda = float(t_perda.replace(',', '.')) if t_perda else 10.0

            t_mo = self.in_bal_mo.text.strip()
            preco_mo = float(t_mo.replace(',', '.')) if t_mo else 0.0

            res = calcular_baldrame(
                comprimento_m=comp, largura_cm=larg, altura_cm=alt,
                perda_percentual=perda
            )

            if "erro" in res:
                self.lbl_res_baldrame.text = f"Erro: {res['erro']}"
                return

            custo_cimento = res['sacos_cimento'] * TABELA_PRECOS_GLOBAL.cimento_50kg
            custo_areia = res['areia_m3'] * TABELA_PRECOS_GLOBAL.areia_m3
            custo_pedra = res['pedra_m3'] * TABELA_PRECOS_GLOBAL.pedra_m3
            custo_mo = comp * preco_mo
            custo_mat = custo_cimento + custo_areia + custo_pedra
            custo_total = custo_mat + custo_mo

            texto_res = (
                f"{txt('label_volume')} ({fmt_num(perda, 0)}% perda): {fmt_num(res['volume_com_perda_m3'], 3)} m³\n"
                f"• {txt('label_cimento')}: {res['sacos_cimento']} {txt('un_sacos')} ({fmt_moeda(custo_cimento)})\n"
                f"• {txt('label_areia')}: {fmt_num(res['areia_m3'], 2)} m³ ({fmt_moeda(custo_areia)})\n"
                f"• {txt('label_pedra')}: {fmt_num(res['pedra_m3'], 2)} m³ ({fmt_moeda(custo_pedra)})\n"
            )
            if custo_mo > 0:
                texto_res += f"• {txt('label_mo')}: {fmt_num(comp, 1)}m ({fmt_moeda(custo_mo)})\n"

            texto_res += f"\n{txt('label_custo')}: {fmt_moeda(custo_total)}"
            self.lbl_res_baldrame.text = texto_res

            self.ultimo_resultado = {
                "etapa": txt("secao_baldrame"),
                "tipo": "baldrame",
                "cimento": res['sacos_cimento'], "areia": res['areia_m3'], "pedra": res['pedra_m3'],
                "custo_mat": custo_mat, "custo_mo": custo_mo, "custo_total": custo_total,
                "resumo_texto": texto_res,
                "inputs": {"comp": comp, "larg": larg, "alt": alt, "perda": perda, "mo": preco_mo}
            }
        except ValueError:
            self.lbl_res_baldrame.text = txt("msg_erro_num")

    # --- USADO PELO HISTÓRICO (visualizar / editar) ---
    @staticmethod
    def _texto_campo(valor) -> str:
        if isinstance(valor, float) and valor.is_integer():
            valor = int(valor)
        return str(valor).replace('.', CONFIG_APP["separador_decimal"])

    def preencher_campos(self, inputs_dict: dict, modo_leitura: bool = False, tipo: str = "brocas"):
        self.modo_somente_leitura = modo_leitura
        self.aba_atual = tipo if tipo in ("brocas", "baldrame") else "brocas"
        self.montar_tela()

        if self.aba_atual == "baldrame":
            campos = {
                "comp": self.in_bal_comp, "larg": self.in_bal_larg, "alt": self.in_bal_alt,
                "perda": self.in_bal_perda, "mo": self.in_bal_mo,
            }
        else:
            campos = {
                "qtd": self.in_qtd, "prof": self.in_prof, "diam": self.in_diam,
                "perda": self.in_perda, "barras": self.in_barras, "mo": self.in_mo,
            }
        for chave, campo in campos.items():
            if chave in inputs_dict:
                campo.text = self._texto_campo(inputs_dict[chave])

    def executar_calculo(self, instance=None):
        if self.aba_atual == "baldrame":
            self.executar_calculo_baldrame(instance)
        else:
            self.executar_calculo_brocas(instance)

    def voltar_home(self, instance):
        destino = "history" if self.origem == "history" else "home"
        self.origem = "home"
        self.manager.current = destino

    def finalizar_e_ir_resumo(self, instance):
        if self.ultimo_resultado:
            ORCAMENTO_FINAL.clear()
            ORCAMENTO_FINAL.append(self.ultimo_resultado)
            summary_screen = self.manager.get_screen("summary")
            summary_screen.atualizar_resumo()
            self.manager.current = "summary"
        else:
            lbl = self.lbl_res_baldrame if self.aba_atual == "baldrame" else self.lbl_resultado
            lbl.text = txt("msg_inicial")


# --- TELA DE RESUMO CONSOLIDADO ---
class SummaryScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "summary"
        self.md_bg_color = self.theme_cls.backgroundColor
        self.dialog_salvar = None
        
        layout_main = MDBoxLayout(orientation="vertical", padding="16dp", spacing="12dp")
        
        topo = MDBoxLayout(size_hint_y=None, height="40dp", spacing="10dp")
        self.titulo_topo = MDLabel(text=txt("titulo_resumo"), font_style="Title", role="medium", bold=True, theme_text_color="Primary")
        topo.add_widget(self.titulo_topo)
        
        scroll = MDScrollView()
        self.box_conteudo = MDBoxLayout(orientation="vertical", spacing="16dp", padding="8dp", size_hint_y=None)
        self.box_conteudo.bind(minimum_height=self.box_conteudo.setter('height'))
        
        self.lbl_detalhes = MDLabel(text=txt("lbl_resumo_vazio"), theme_text_color="Primary", size_hint_y=None)
        self.lbl_detalhes.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        
        box_botoes = MDBoxLayout(orientation="vertical", spacing="8dp", size_hint_y=None)
        box_botoes.bind(minimum_height=box_botoes.setter('height'))
        
        self.btn_salvar_hist = MDButton(MDButtonText(text=txt("btn_salvar_hist")), pos_hint={"center_x": 0.5}, on_release=self.abrir_dialog_salvar)
        self.btn_pdf = MDButton(MDButtonText(text=txt("btn_pdf")), pos_hint={"center_x": 0.5})
        self.btn_editar = MDButton(MDButtonText(text=txt("btn_editar")), pos_hint={"center_x": 0.5}, on_release=self.editar_calculos)
        
        box_botoes.add_widget(self.btn_salvar_hist)
        box_botoes.add_widget(self.btn_pdf)
        box_botoes.add_widget(self.btn_editar)
        
        self.box_conteudo.add_widget(self.lbl_detalhes)
        self.box_conteudo.add_widget(box_botoes)
        
        scroll.add_widget(self.box_conteudo)
        layout_main.add_widget(topo)
        layout_main.add_widget(scroll)
        self.add_widget(layout_main)

    def editar_calculos(self, instance):
        calc_screen = self.manager.get_screen("calculator")
        for child in calc_screen.layout_principal.children:
            if isinstance(child, MDScrollView):
                child.scroll_y = 1.0
        self.manager.current = "calculator"

    def abrir_dialog_salvar(self, instance):
        if not ORCAMENTO_FINAL:
            return
            
        user_id = USUARIO_LOGADO.get("id") if USUARIO_LOGADO else None
        LIMITE_HISTORICO_GRATIS = 5
        if quantidade_orcamentos_salvos(user_id) >= LIMITE_HISTORICO_GRATIS:
            self.dialog_limite = MDDialog(
                MDDialogHeadlineText(text="Limite Alcançado"),
                MDDialogSupportingText(text="Você atingiu o limite de 5 orçamentos. Exclua um item antigo no Histórico!"),
                MDDialogButtonContainer(
                    MDButton(MDButtonText(text=txt("btn_fechar")), on_release=lambda x: self.dialog_limite.dismiss())
                )
            )
            self.dialog_limite.open()
            return

        self.input_nome_obra = MDTextField(
            MDTextFieldHintText(text=txt("hint_nome_obra")),
            mode="outlined"
        )
        
        self.dialog_salvar = MDDialog(
            MDDialogHeadlineText(text=txt("dialog_salvar_titulo")),
            MDDialogSupportingText(text=txt("dialog_salvar_sub")),
            MDDialogContentContainer(self.input_nome_obra, orientation="vertical", padding="12dp"),
            MDDialogButtonContainer(
                MDButton(MDButtonText(text=txt("btn_cancelar")), on_release=lambda x: self.dialog_salvar.dismiss()),
                MDButton(MDButtonText(text=txt("btn_salvar")), on_release=self.confirmar_salvar)
            )
        )
        self.dialog_salvar.open()

    def confirmar_salvar(self, instance):
        nome = self.input_nome_obra.text.strip()
        if not nome:
            nome = "Orçamento Sem Nome"
            
        subtotal_mat = sum(item.get("custo_mat", 0) for item in ORCAMENTO_FINAL)
        subtotal_mo = sum(item.get("custo_mo", 0) for item in ORCAMENTO_FINAL)
        valor_total = subtotal_mat + subtotal_mo
        
        user_id = USUARIO_LOGADO.get("id") if USUARIO_LOGADO else None
        salvar_orcamento(
            usuario_id=user_id,
            nome=nome,
            estado=CONFIG_APP["estado"],
            dados=ORCAMENTO_FINAL,
            valor_total=valor_total
        )
        self.dialog_salvar.dismiss()
        self.manager.get_screen("history").carregar_historico()
        self.manager.current = "history"

    def atualizar_resumo(self):
        self.titulo_topo.text = txt("titulo_resumo")
        self.btn_salvar_hist.children[0].text = txt("btn_salvar_hist")
        self.btn_pdf.children[0].text = txt("btn_pdf")
        self.btn_editar.children[0].text = txt("btn_editar")
        
        if ORCAMENTO_FINAL:
            total_cimento = sum(item.get("cimento", 0) for item in ORCAMENTO_FINAL)
            total_areia = sum(item.get("areia", 0) for item in ORCAMENTO_FINAL)
            total_pedra = sum(item.get("pedra", 0) for item in ORCAMENTO_FINAL)
            total_aco = sum(item.get("aco_kg", 0) for item in ORCAMENTO_FINAL)
            total_barras = sum(item.get("barras_12m", 0) for item in ORCAMENTO_FINAL)
            
            subtotal_materiais = sum(item.get("custo_mat", 0) for item in ORCAMENTO_FINAL)
            subtotal_mo = sum(item.get("custo_mo", 0) for item in ORCAMENTO_FINAL)
            total_geral = subtotal_materiais + subtotal_mo
            
            texto = "========================================\n"
            texto += f"ORÇAMENTO CONSOLIDADO DA OBRA\n"
            texto += f"Região / Estado: {CONFIG_APP['pais']} ({CONFIG_APP['estado']})\n"
            texto += "========================================\n\n"
            
            texto += "ETAPAS INCLUÍDAS:\n"
            for idx, item in enumerate(ORCAMENTO_FINAL, 1):
                texto += f"\n[{idx}] {item['etapa']}\n{item['resumo_texto']}\n"
                
            texto += "\n----------------------------------------\n"
            texto += "LISTA DE COMPRAS CONSOLIDADA (TOTAL):\n"
            texto += "----------------------------------------\n"
            texto += f"• Cimento 50kg: {total_cimento} sacos\n"
            texto += f"• Areia: {fmt_num(total_areia, 2)} m³\n"
            texto += f"• Brita/Pedra: {fmt_num(total_pedra, 2)} m³\n"
            if total_aco > 0:
                texto += f"• Aço: {fmt_num(total_aco, 1)} kg ({total_barras} barras de 12m)\n"
                
            texto += "\n----------------------------------------\n"
            texto += "RESUMO FINANCEIRO FINAL:\n"
            texto += "----------------------------------------\n"
            texto += f"• Subtotal Materiais: {fmt_moeda(subtotal_materiais)}\n"
            texto += f"• Subtotal Mão de Obra: {fmt_moeda(subtotal_mo)}\n\n"
            texto += f"TOTAL GERAL DA OBRA: {fmt_moeda(total_geral)}\n"
            texto += "========================================"
            
            self.lbl_detalhes.text = texto
        else:
            self.lbl_detalhes.text = txt("lbl_resumo_vazio")


# --- TELA DE HISTÓRICO ---
class HistoryScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "history"
        self.md_bg_color = self.theme_cls.backgroundColor
        self.dialog_ativo = None
        
        layout_main = MDBoxLayout(orientation="vertical", padding="12dp", spacing="10dp")
        
        topo = MDBoxLayout(size_hint_y=None, height="40dp", spacing="10dp")
        self.btn_voltar = MDButton(MDButtonText(text=txt("btn_voltar")), on_release=self.voltar_home)
        self.lbl_titulo = MDLabel(text=txt("titulo_historico"), font_style="Title", role="medium", bold=True, theme_text_color="Primary")
        topo.add_widget(self.btn_voltar)
        topo.add_widget(self.lbl_titulo)
        
        scroll = MDScrollView()
        self.box_cards = MDBoxLayout(orientation="vertical", spacing="12dp", padding="4dp", size_hint_y=None)
        self.box_cards.bind(minimum_height=self.box_cards.setter('height'))
        
        scroll.add_widget(self.box_cards)
        layout_main.add_widget(topo)
        layout_main.add_widget(scroll)
        self.add_widget(layout_main)

    def atualizar_interface(self):
        self.btn_voltar.children[0].text = txt("btn_voltar")
        self.lbl_titulo.text = txt("titulo_historico")

    def voltar_home(self, instance):
        self.manager.current = "home"

    def carregar_historico(self):
        self.atualizar_interface()
        self.box_cards.clear_widgets()
        
        user_id = USUARIO_LOGADO.get("id") if USUARIO_LOGADO else None
        lista = listar_orcamentos(user_id)
        if not lista:
            lbl_vazio = MDLabel(text=txt("lbl_hist_vazio"), theme_text_color="Secondary", halign="center")
            self.box_cards.add_widget(lbl_vazio)
            return
            
        for item in lista:
            card = MDCard(
                orientation="vertical",
                padding="12dp",
                spacing="8dp",
                size_hint_y=None,
                style="outlined"
            )
            card.bind(minimum_height=card.setter('height'))
            
            lbl_nome = MDLabel(
                text=item['nome'],
                font_style="Title",
                role="small",
                bold=True,
                theme_text_color="Primary",
                size_hint_y=None,
                height="24dp"
            )
            
            lbl_detalhes = MDLabel(
                text=f"{txt('lbl_data')}: {item['data_criacao']} | {txt('lbl_uf')}: {item['estado']}\n{txt('lbl_valor_total')}: {fmt_moeda(item['valor_total'])}",
                font_style="Body",
                role="small",
                theme_text_color="Secondary",
                size_hint_y=None,
                height="36dp"
            )
            
            divisoria = MDDivider()
            
            row1 = MDBoxLayout(orientation="horizontal", spacing="6dp", size_hint_y=None, height="36dp")
            btn_vis = MDButton(MDButtonText(text=txt("btn_vis")), on_release=lambda x, it=item: self.visualizar_orcamento(it))
            btn_edit = MDButton(MDButtonText(text=txt("btn_edit")), on_release=lambda x, it=item: self.editar_orcamento(it))
            btn_dup = MDButton(MDButtonText(text=txt("btn_dup")), on_release=lambda x, it=item: self.duplicar_popup(it))
            row1.add_widget(btn_vis)
            row1.add_widget(btn_edit)
            row1.add_widget(btn_dup)
            
            row2 = MDBoxLayout(orientation="horizontal", spacing="6dp", size_hint_y=None, height="36dp")
            btn_ren = MDButton(MDButtonText(text=txt("btn_ren")), on_release=lambda x, it=item: self.renomear_popup(it))
            btn_exc = MDButton(MDButtonText(text=txt("btn_exc")), on_release=lambda x, it=item: self.excluir_popup(it))
            row2.add_widget(btn_ren)
            row2.add_widget(btn_exc)
            
            card.add_widget(lbl_nome)
            card.add_widget(lbl_detalhes)
            card.add_widget(divisoria)
            card.add_widget(row1)
            card.add_widget(row2)
            
            self.box_cards.add_widget(card)

    def visualizar_orcamento(self, item):
        dados = item["dados_json"]
        if dados and len(dados) > 0:
            inputs = dados[0].get("inputs", {})
            calc_screen = self.manager.get_screen("calculator")
            calc_screen.origem = "history"
            calc_screen.preencher_campos(inputs, modo_leitura=True, tipo=dados[0].get("tipo", "brocas"))
            calc_screen.executar_calculo(None)
            self.manager.current = "calculator"

    def editar_orcamento(self, item):
        dados = item["dados_json"]
        if dados and len(dados) > 0:
            inputs = dados[0].get("inputs", {})
            calc_screen = self.manager.get_screen("calculator")
            calc_screen.origem = "history"
            calc_screen.preencher_campos(inputs, modo_leitura=False, tipo=dados[0].get("tipo", "brocas"))
            self.manager.current = "calculator"

    def duplicar_popup(self, item):
        input_dup = MDTextField(MDTextFieldHintText(text=txt("hint_nome_obra")), mode="outlined")
        input_dup.text = f"{item['nome']} (Copy)" if CONFIG_APP.get("idioma") == "en" else f"{item['nome']} (Cópia)"
        
        self.dialog_ativo = MDDialog(
            MDDialogHeadlineText(text=txt("btn_dup")),
            MDDialogContentContainer(input_dup, orientation="vertical", padding="12dp"),
            MDDialogButtonContainer(
                MDButton(MDButtonText(text=txt("btn_cancelar")), on_release=lambda x: self.dialog_ativo.dismiss()),
                MDButton(MDButtonText(text=txt("btn_dup")), on_release=lambda x: self.confirmar_duplicar(item["id"], input_dup.text))
            )
        )
        self.dialog_ativo.open()

    def confirmar_duplicar(self, item_id, novo_nome):
        user_id = USUARIO_LOGADO.get("id") if USUARIO_LOGADO else None
        duplicar_orcamento(item_id, user_id, novo_nome.strip() or "Cópia")
        self.dialog_ativo.dismiss()
        self.carregar_historico()

    def renomear_popup(self, item):
        input_ren = MDTextField(MDTextFieldHintText(text=txt("hint_nome_obra")), mode="outlined")
        input_ren.text = item["nome"]
        
        self.dialog_ativo = MDDialog(
            MDDialogHeadlineText(text=txt("btn_ren")),
            MDDialogContentContainer(input_ren, orientation="vertical", padding="12dp"),
            MDDialogButtonContainer(
                MDButton(MDButtonText(text=txt("btn_cancelar")), on_release=lambda x: self.dialog_ativo.dismiss()),
                MDButton(MDButtonText(text=txt("btn_salvar")), on_release=lambda x: self.confirmar_renomear(item["id"], input_ren.text))
            )
        )
        self.dialog_ativo.open()

    def confirmar_renomear(self, item_id, novo_nome):
        atualizar_nome_orcamento(item_id, novo_nome.strip() or "Orçamento")
        self.dialog_ativo.dismiss()
        self.carregar_historico()

    def excluir_popup(self, item):
        self.dialog_ativo = MDDialog(
            MDDialogHeadlineText(text=txt("btn_exc")),
            MDDialogSupportingText(text=f"Excluir '{item['nome']}'?"),
            MDDialogButtonContainer(
                MDButton(MDButtonText(text=txt("btn_cancelar")), on_release=lambda x: self.dialog_ativo.dismiss()),
                MDButton(MDButtonText(text=txt("btn_exc")), on_release=lambda x: self.confirmar_excluir(item["id"]))
            )
        )
        self.dialog_ativo.open()

    def confirmar_excluir(self, item_id):
        excluir_orcamento(item_id)
        self.dialog_ativo.dismiss()
        self.carregar_historico()

# --- TELA DE CONFIGURAÇÕES ---
class SettingsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "settings"
        self.md_bg_color = self.theme_cls.backgroundColor
        
        self.estados_br = ESTADOS_BR
        self.estados_eua = ESTADOS_US
        
        self.layout = MDBoxLayout(orientation="vertical", padding=("16dp", "12dp", "16dp", "12dp"), spacing="8dp")
        self.add_widget(self.layout)
        self.montar_tela()

    def montar_tela(self):
        self.layout.clear_widgets()
        
        top_bar = MDBoxLayout(size_hint_y=None, height="48dp", spacing="8dp")
        btn_voltar = MDIconButton(icon="arrow-left", on_release=self.voltar, pos_hint={"center_y": 0.5})
        
        lang = CONFIG_APP.get("idioma", "pt")
        titulo_texto = "Settings & Preferences" if lang == "en" else "Configurações & Preferências"
        
        self.lbl_titulo = MDLabel(
            text=titulo_texto,
            font_style="Title",
            role="medium",
            bold=True,
            pos_hint={"center_y": 0.5}
        )
        top_bar.add_widget(btn_voltar)
        top_bar.add_widget(self.lbl_titulo)
        
        self.scroll = MDScrollView()
        box_conteudo = MDBoxLayout(
            orientation="vertical",
            spacing="12dp",
            padding=("0dp", "8dp", "0dp", "16dp"),
            size_hint_y=None
        )
        box_conteudo.bind(minimum_height=box_conteudo.setter('height'))
        
        pais = CONFIG_APP.get("pais", "BR (R$)")
        estado = CONFIG_APP.get("estado", "SP")
        tema_val = CONFIG_APP.get("tema", "Escuro")
        moeda = CONFIG_APP.get("moeda", "R$")

        sec_pref_txt = "General Preferences" if lang == "en" else "Preferências Gerais"
        self.lbl_sec_pref = MDLabel(text=sec_pref_txt, font_style="Title", role="small", bold=True, size_hint_y=None, height="30dp")
        box_conteudo.add_widget(self.lbl_sec_pref)
        
        lbl_pais = f"Country: {pais}" if lang == "en" else f"País: {pais}"
        lbl_estado = f"State: {estado}" if lang == "en" else f"Estado: {estado}"
        lbl_tema = f"Theme: {tema_val}" if lang == "en" else f"Tema: {tema_val}"

        self.btn_pais = MDButton(MDButtonText(text=lbl_pais), on_release=self.alternar_pais)
        self.btn_estado = MDButton(MDButtonText(text=lbl_estado), on_release=self.alternar_estado)
        self.btn_tema = MDButton(MDButtonText(text=lbl_tema), on_release=self.alternar_tema)
        
        box_conteudo.add_widget(self.btn_pais)
        box_conteudo.add_widget(self.btn_estado)
        box_conteudo.add_widget(self.btn_tema)
        
        sec_precos_txt = "Material Prices (Region)" if lang == "en" else "Preços dos Materiais (Região)"
        self.lbl_sec_precos = MDLabel(text=sec_precos_txt, font_style="Title", role="small", bold=True, size_hint_y=None, height="30dp")
        box_conteudo.add_widget(self.lbl_sec_precos)
        
        self.in_cimento = MDTextField(MDTextFieldHintText(text=f"{txt('hint_cimento')} ({moeda})"), mode="outlined", write_tab=False)
        self.in_areia = MDTextField(MDTextFieldHintText(text=f"{txt('hint_areia')} ({moeda})"), mode="outlined", write_tab=False)
        self.in_brita = MDTextField(MDTextFieldHintText(text=f"{txt('hint_brita')} ({moeda})"), mode="outlined", write_tab=False)
        self.in_mao_obra = MDTextField(MDTextFieldHintText(text=f"{txt('hint_mao_obra')} ({moeda})"), mode="outlined", write_tab=False)
        
        box_conteudo.add_widget(self.in_cimento)
        box_conteudo.add_widget(self.in_areia)
        box_conteudo.add_widget(self.in_brita)
        box_conteudo.add_widget(self.in_mao_obra)
        
        btn_salvar_txt = "Save Changes" if lang == "en" else "Salvar Alterações"
        self.btn_salvar = MDButton(
            MDButtonText(text=btn_salvar_txt),
            pos_hint={"center_x": 0.5},
            on_release=self.salvar_configuracoes
        )
        box_conteudo.add_widget(self.btn_salvar)
        
        self.scroll.add_widget(box_conteudo)
        self.layout.add_widget(top_bar)
        self.layout.add_widget(self.scroll)

    def voltar(self, instance=None):
        self.manager.current = "login"

    def alternar_pais(self, instance):
        if CONFIG_APP.get("pais") == "BR (R$)":
            CONFIG_APP["pais"] = "EUA ($)"
            CONFIG_APP["idioma"] = "en"
            CONFIG_APP["estado"] = "NY"
            CONFIG_APP["moeda"] = "$"
            CONFIG_APP["separador_decimal"] = "."
            
            TABELA_PRECOS_GLOBAL.cimento_50kg = PRECOS_EUA["cimento"]
            TABELA_PRECOS_GLOBAL.areia_m3 = PRECOS_EUA["areia"]
            TABELA_PRECOS_GLOBAL.pedra_m3 = PRECOS_EUA["brita"]
            TABELA_PRECOS_GLOBAL.aco_kg = PRECOS_EUA["aco"]
            TABELA_PRECOS_GLOBAL.mao_obra_m2 = PRECOS_EUA["mao_obra"]
            
            CONFIG_APP["cimento"] = str(PRECOS_EUA["cimento"])
            CONFIG_APP["areia"] = str(PRECOS_EUA["areia"])
            CONFIG_APP["brita"] = str(PRECOS_EUA["brita"])
            CONFIG_APP["mao_obra"] = str(PRECOS_EUA["mao_obra"])
        else:
            CONFIG_APP["pais"] = "BR (R$)"
            CONFIG_APP["idioma"] = "pt"
            CONFIG_APP["estado"] = "SP"
            CONFIG_APP["moeda"] = "R$"
            CONFIG_APP["separador_decimal"] = ","
            
            TABELA_PRECOS_GLOBAL.cimento_50kg = PRECOS_BR["cimento"]
            TABELA_PRECOS_GLOBAL.areia_m3 = PRECOS_BR["areia"]
            TABELA_PRECOS_GLOBAL.pedra_m3 = PRECOS_BR["brita"]
            TABELA_PRECOS_GLOBAL.aco_kg = PRECOS_BR["aco"]
            TABELA_PRECOS_GLOBAL.mao_obra_m2 = PRECOS_BR["mao_obra"]
            
            CONFIG_APP["cimento"] = str(PRECOS_BR["cimento"])
            CONFIG_APP["areia"] = str(PRECOS_BR["areia"])
            CONFIG_APP["brita"] = str(PRECOS_BR["brita"])
            CONFIG_APP["mao_obra"] = str(PRECOS_BR["mao_obra"])
            
        if self.manager:
            self.manager.atualizar_todas_as_telas()

    def alternar_estado(self, instance):
        pais = CONFIG_APP.get("pais", "BR (R$)")
        lista = self.estados_eua if pais == "EUA ($)" else self.estados_br
        
        est_atual = CONFIG_APP.get("estado", lista[0])
        idx = (lista.index(est_atual) + 1) % len(lista) if est_atual in lista else 0
        CONFIG_APP["estado"] = lista[idx]
        
        if self.manager:
            self.manager.atualizar_todas_as_telas()

    def alternar_tema(self, instance):
        app = MDApp.get_running_app()
        if app.theme_cls.theme_style == "Dark":
            app.theme_cls.theme_style = "Light"
            CONFIG_APP["tema"] = "Claro" if CONFIG_APP.get("idioma") == "pt" else "Light"
        else:
            app.theme_cls.theme_style = "Dark"
            CONFIG_APP["tema"] = "Escuro" if CONFIG_APP.get("idioma") == "pt" else "Dark"
            
        if self.manager:
            self.manager.atualizar_todas_as_telas()

    def salvar_configuracoes(self, instance):
        try:
            if self.in_cimento.text.strip():
                ciment_val = float(self.in_cimento.text.replace(',', '.').strip())
                TABELA_PRECOS_GLOBAL.cimento_50kg = ciment_val
                CONFIG_APP["cimento"] = str(ciment_val)

            if self.in_areia.text.strip():
                areia_val = float(self.in_areia.text.replace(',', '.').strip())
                TABELA_PRECOS_GLOBAL.areia_m3 = areia_val
                CONFIG_APP["areia"] = str(areia_val)

            if self.in_brita.text.strip():
                brita_val = float(self.in_brita.text.replace(',', '.').strip())
                TABELA_PRECOS_GLOBAL.pedra_m3 = brita_val
                CONFIG_APP["brita"] = str(brita_val)

            if self.in_mao_obra.text.strip():
                mo_val = float(self.in_mao_obra.text.replace(',', '.').strip())
                TABELA_PRECOS_GLOBAL.mao_obra_m2 = mo_val
                CONFIG_APP["mao_obra"] = str(mo_val)
        except ValueError:
            pass

        if self.manager:
            self.manager.atualizar_todas_as_telas()
        self.voltar()

    def atualizar_interface(self):
        self.montar_tela()


class MainScreenManager(MDScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(LoginScreen())  
        self.add_widget(HomeScreen())
        self.add_widget(CalculatorScreen())
        self.add_widget(SummaryScreen())
        self.add_widget(HistoryScreen())
        self.add_widget(SettingsScreen())

    def atualizar_todas_as_telas(self):
        for screen in self.screens:
            if hasattr(screen, "atualizar_interface") and callable(screen.atualizar_interface):
                screen.atualizar_interface()