"""Tela de Login / Cadastro."""
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDButton, MDButtonText, MDIconButton
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from src.models.database import cadastrar_usuario, autenticar_usuario
from kivymd.uix.widget import MDWidget
from src.views.comum import txt
from src.views import comum


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
                comum.USUARIO_LOGADO = usr
                home_screen = self.manager.get_screen("home")
                home_screen.atualizar_avatar()
                self.manager.current = "home"
            else:
                self.lbl_status.text = "E-mail ou senha incorretos!"

    def entrar_visitante(self, instance):
        comum.USUARIO_LOGADO = None
        home_screen = self.manager.get_screen("home")
        home_screen.atualizar_avatar()
        self.manager.current = "home"