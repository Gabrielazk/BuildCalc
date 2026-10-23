"""Tela de Configurações (país, estado, tema e preços da região)."""
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDButton, MDButtonText, MDIconButton
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivymd.uix.scrollview import MDScrollView
from src.views.comum import CONFIG_APP, PRECOS_EUA, PRECOS_BR, ESTADOS_BR, ESTADOS_US, TABELA_PRECOS_GLOBAL, txt


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