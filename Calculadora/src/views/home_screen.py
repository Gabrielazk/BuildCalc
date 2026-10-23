"""Tela inicial (Home)."""
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogHeadlineText,
    MDDialogSupportingText,
    MDDialogButtonContainer,
)
from kivymd.uix.widget import MDWidget
from src.views.comum import ORCAMENTO_FINAL, txt
from src.views import comum


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
        if comum.USUARIO_LOGADO and comum.USUARIO_LOGADO.get("nome"):
            inicial = comum.USUARIO_LOGADO["nome"][0].upper()
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
        if comum.USUARIO_LOGADO:
            nome = comum.USUARIO_LOGADO["nome"]
            email = comum.USUARIO_LOGADO["email"]
            plano = comum.USUARIO_LOGADO.get("plano", "Gratuito")
            
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
        comum.USUARIO_LOGADO = None
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
        calc_screen.reiniciar()
        for child in calc_screen.layout_principal.children:
            if isinstance(child, MDScrollView):
                child.scroll_y = 1.0
        self.manager.current = "calculator"

    def ir_para_historico(self, instance):
        hist_screen = self.manager.get_screen("history")
        hist_screen.carregar_historico()
        self.manager.current = "history"