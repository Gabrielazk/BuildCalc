from math import pi, ceil
import math
import os
from datetime import datetime
from kivy.metrics import dp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import SlideTransition
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import Snackbar
import json
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty, NumericProperty
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import warnings
import tkinter as tk
from tkinter import filedialog
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.list import OneLineListItem
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton
from kivymd.uix.widget import MDWidget
import tempfile
import webbrowser
import re
from reportlab.platypus import (HRFlowable, KeepTogether)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.units import mm
from kivy.graphics import Color, Rectangle
from kivymd.uix.label import MDIcon
from kivymd.uix.button import MDIconButton
import copy

Window.size = (400, 700)

KV = '''

ScreenManager:
    TelaInicial:
    TelaAbas:
    TelaHistorico:

<TelaInicial@MDScreen>:
    name: "inicio"

    MDFloatLayout:
        md_bg_color: (1, 1, 1, 1) if app.theme_cls.theme_style == "Light" else (0.10, 0.12, 0.14, 1)

        MDTopAppBar:
            title: "Calculadora: BuildCalc"
            elevation: 4
            pos_hint: {"top": 1}
            md_bg_color: 0.15, 0.30, 0.39, 1
            specific_text_color: 1, 1, 1, 1
            right_action_items: [["theme-light-dark", lambda x: app.alternar_tema()], ["help-circle-outline", lambda x: app.abrir_ajuda_inicial()]]
            height: "90dp"

        Image:
            source: "logo_housesynk-removebg-preview.png"
            size_hint: None, None
            size: "235dp", "235dp"
            pos_hint: {"center_x": 0.5, "center_y": 0.72}
            allow_stretch: True
            keep_ratio: True

        MDLabel:
            text: "Bem-vindo ao"
            halign: "center"
            theme_text_color: "Custom"
            text_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (1, 1, 1, 1)
            font_style: "H4"
            bold: True
            pos_hint: {"center_x": 0.5, "center_y": 0.53}

        MDLabel:
            text: "BuildCalc"
            halign: "center"
            theme_text_color: "Custom"
            text_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (1, 1, 1, 1)
            font_style: "H4"
            bold: True
            pos_hint: {"center_x": 0.5, "center_y": 0.48}

        MDBoxLayout:
            size_hint: None, None
            size: "110dp", "2dp"
            pos_hint: {"center_x": 0.5, "center_y": 0.44}

            canvas.before:
                Color:
                    rgba: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (1, 1, 1, 1)
                Rectangle:
                    pos: self.pos
                    size: self.size

        MDLabel:
            text: "Seu app para cálculos e organização\\nde materiais"
            halign: "center"
            theme_text_color: "Custom"
            text_color: (0.45, 0.45, 0.45, 1) if app.theme_cls.theme_style == "Light" else (0.8, 0.8, 0.8, 1)
            theme_text_color: "Secondary"
            font_style: "Body1"
            pos_hint: {"center_x": 0.5, "center_y": 0.37}

        MDRaisedButton:
            text: "Iniciar"
            md_bg_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (0.22, 0.38, 0.48, 1)
            text_color: 1, 1, 1, 1
            size_hint: 0.45, None
            height: "48dp"
            pos_hint: {"center_x": 0.5, "center_y": 0.22}
            elevation: 3
            on_release: app.abrir_abas()

        MDRaisedButton:
            text: "Histórico"
            md_bg_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (0.22, 0.38, 0.48, 1)
            text_color: 1, 1, 1, 1
            size_hint: 0.45, None
            height: "48dp"
            pos_hint: {"center_x": 0.5, "center_y": 0.14}
            elevation: 3
            on_release: app.abrir_historico()

        MDLabel:
            text: "Versão 1.0"
            halign: "center"
            theme_text_color: "Custom"
            text_color: (0.7, 0.7, 0.7, 1) if app.theme_cls.theme_style == "Light" else (0.5, 0.5, 0.5, 1)
            theme_text_color: "Hint"
            font_style: "Caption"
            pos_hint: {"center_x": 0.5, "center_y": 0.05}

<TelaHistorico@MDScreen>:
    name: "historico"

    MDFloatLayout:
        md_bg_color: (1, 1, 1, 1) if app.theme_cls.theme_style == "Light" else (0.10, 0.12, 0.14, 1)

        MDTopAppBar:
            title: "Histórico de Obras"
            elevation: 4
            pos_hint: {"top": 1}
            left_action_items: [["arrow-left", lambda x: app.voltar_inicio()]]
            md_bg_color: 0.15, 0.30, 0.39, 1
            specific_text_color: 1, 1, 1, 1
            height: "90dp"

        ScrollView:
            size_hint: 1, None
            size: self.parent.width, self.parent.height - dp(80)
            pos_hint: {"x": 0, "y": 0}
            do_scroll_x: False
            bar_width: dp(4)

            MDBoxLayout:
                orientation: "vertical"
                adaptive_height: True
                padding: dp(18), dp(8), dp(18), dp(26)
                spacing: dp(12)

                MDCard:
                    id: card_feedback
                    orientation: "horizontal"
                    size_hint_y: None
                    height: 0
                    opacity: 0
                    disabled: True
                    padding: dp(14)
                    spacing: dp(12)
                    radius: [16, 16, 16, 16]
                    elevation: 2
                    md_bg_color: (0.95, 0.97, 1, 1) if app.theme_cls.theme_style == "Light" else (0.18, 0.22, 0.28, 1)

                    MDIcon:
                        icon: "check-circle"
                        theme_text_color: "Custom"
                        text_color: (0.2, 0.8, 0.5, 1) if app.theme_cls.theme_style == "Light" else (0.35, 0.85, 0.55, 1)
                        font_size: "30sp"
                        size_hint: None, None
                        size: dp(34), dp(34)
                        pos_hint: {"center_y": 0.5}

                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: dp(2)

                        MDLabel:
                            text: "Obra salva com sucesso!"
                            bold: True
                            theme_text_color: "Custom"
                            text_color: (0.08, 0.08, 0.08, 1) if app.theme_cls.theme_style == "Light" else (1, 1, 1, 1)
                            font_style: "Subtitle1"
                            size_hint_y: None
                            height: self.texture_size[1]

                        MDLabel:
                            text: "Ela já está disponível no histórico abaixo."
                            theme_text_color: "Custom"
                            text_color: (0.35, 0.4, 0.45, 1) if app.theme_cls.theme_style == "Light" else (0.78, 0.82, 0.88, 1)
                            font_style: "Caption"
                            size_hint_y: None
                            height: self.texture_size[1]

                    MDRaisedButton:
                        id: btn_ver_resumo
                        text: "Ver resumo"
                        size_hint: None, None
                        size: dp(110), dp(38)
                        pos_hint: {"center_y": 0.5}
                        md_bg_color: (0.15, 0.30, 0.39, 1) if app.theme_cls.theme_style == "Light" else (0.26, 0.42, 0.55, 1)
                        text_color: 1, 1, 1, 1
                        elevation: 0
                        on_release: app.ir_para_resumo_ultima_obra()

                MDTextField:
                    id: filtro_obra
                    hint_text: "Procurar obra..."
                    mode: "round"
                    size_hint_y: None
                    height: dp(50)
                    icon_right: "magnify"
                    line_color_normal: (0, 0, 0, 0)
                    line_color_focus: (0, 0, 0, 0)
                    md_bg_color: (1, 1, 1, 1)
                    text_color_normal: (0, 0, 0, 1)
                    hint_text_color_normal: (0.5, 0.5, 0.5, 1)
                    on_text: app.filtrar_obras(self.text)

                Widget:
                    size_hint_y: None
                    height: dp(10)

                MDBoxLayout:
                    orientation: "horizontal"
                    adaptive_height: True
                    spacing: dp(8)

                    MDIcon:
                        icon: "content-save-outline"
                        theme_text_color: "Custom"
                        text_color: (0.2, 0.25, 0.3, 1) if app.theme_cls.theme_style == "Light" else (0.75, 0.82, 0.9, 1)
                        size_hint: None, None
                        size: dp(22), dp(22)

                    MDLabel:
                        text: "Suas obras salvas"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: (0.12, 0.12, 0.12, 1) if app.theme_cls.theme_style == "Light" else (1, 1, 1, 1)
                        font_style: "H6"
                        adaptive_height: True

                MDBoxLayout:
                    id: container_historico
                    orientation: "vertical"
                    spacing: dp(16)
                    adaptive_height: True

                MDLabel:
                    text: "Dica: clique em uma obra para ver o resumo completo ou continuar editando."
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: (0.55, 0.55, 0.55, 1) if app.theme_cls.theme_style == "Light" else (0.6, 0.64, 0.68, 1)
                    font_style: "Caption"
                    adaptive_height: True

<TelaAbas@MDScreen>:
    name: "abas"
    BoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "BuildCalc - Cálculos"
            md_bg_color: 0.15, 0.30, 0.39, 1
            specific_text_color: 1, 1, 1, 1
            left_action_items: [["arrow-left", lambda x: app.voltar_inicio()]]
            right_action_items: [["help-circle-outline", lambda x: app.abrir_ajuda_abas()]]

        MDTabs:
            id: tabs
            tab_indicator_anim: True
            background_color: 0.15, 0.30, 0.39, 1
            on_tab_switch: app.atualizar_aba_atual(*args)

            TabBrocas:
                id: tab_brocas

            TabBaldrame:
                id: tab_baldrame

            TabParedes:
                id: tab_paredes

            TabReboco:
                id: tab_reboco

            TabContrapiso:
                id: tab_contrapiso

            TabRevestimento:
                id: tab_revestimento

            TabOrcamento:
                id: tab_orcamento

            TabResumo:
                id: tab_resumo

<TabBrocas>:
    title: "Brocas"
    orientation: "vertical"
    md_bg_color: (0.96, 0.96, 0.96, 1) if app.theme_cls.theme_style == "Light" else (0.10, 0.12, 0.14, 1)

    ScrollView:
        do_scroll_x: False

        MDBoxLayout:
            orientation: "vertical"
            padding: [24, 30, 24, 30]
            spacing: "22dp"
            adaptive_height: True
            size_hint_y: None
            height: self.minimum_height

            MDLabel:
                text: "[b]Cálculo de Brocas[/b]"
                markup: True
                font_style: "H6"
                halign: "center"
                theme_text_color: "Custom"
                text_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (1, 1, 1, 1)

            MDCard:
                orientation: "vertical"
                padding: "20dp"
                spacing: "14dp"
                elevation: 6
                size_hint_y: None
                height: self.minimum_height
                md_bg_color: (1, 1, 1, 1) if app.theme_cls.theme_style == "Light" else (0.16, 0.18, 0.21, 1)
                radius: [12, 12, 12, 12]

                MDTextField:
                    id: qtd_brocas
                    hint_text: "Quantidade de brocas"
                    helper_text: "Informe o total de brocas da obra"
                    helper_text_mode: "on_focus"
                    input_filter: "int"
                    multiline: False
                    on_text_validate: app.proximo_campo("abas", "tab_brocas", "diametro_broca")

                MDTextField:
                    id: diametro_broca
                    hint_text: "Diâmetro da broca (m)"
                    helper_text: "Use metro. Exemplo: 0.25"
                    helper_text_mode: "on_focus"
                    input_filter: None
                    multiline: False
                    on_text_validate: app.proximo_campo("abas", "tab_brocas", "profundidade_broca")

                MDTextField:
                    id: profundidade_broca
                    hint_text: "Profundidade da broca (m)"
                    helper_text: "Use metro. Exemplo: 1.50"
                    helper_text_mode: "on_focus"
                    input_filter: None

                MDBoxLayout:
                    orientation: "horizontal"
                    size_hint_y: None
                    height: "56dp"
                    spacing: "10dp"

                    MDLabel:
                        text: "Proporção do concreto:"
                        halign: "left"
                        valign: "center"
                        size_hint_x: 0.55
                        theme_text_color: "Custom"
                        text_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (1, 1, 1, 1)

                    MDBoxLayout:
                        md_bg_color: (0.97, 0.97, 0.97, 1) if app.theme_cls.theme_style == "Light" else (0.22, 0.24, 0.28, 1)
                        radius: [10, 10, 10, 10]
                        elevation: 0
                        padding: [12, 0, 8, 0]
                        size_hint_x: 0.45
                        size_hint_y: None
                        height: "42dp"
                        pos_hint: {"center_y": 0.5}

                        MDDropDownItem:
                            id: proporcao_dropdown
                            text: "Selecione"
                            pos_hint: {"center_y": 0.5}
                            on_release: app.abrir_menu_proporcao(self)

            MDBoxLayout:
                spacing: "20dp"
                padding_y: "10dp"
                adaptive_height: True
                size_hint_y: None
                height: self.minimum_height
                pos_hint: {"center_x": 0.5}

                MDRaisedButton:
                    text: "CALCULAR"
                    md_bg_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (0.22, 0.38, 0.48, 1)
                    text_color: 1, 1, 1, 1
                    on_release: app.calcular_brocas()

                MDRaisedButton:
                    text: "LIMPAR"
                    md_bg_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (0.22, 0.38, 0.48, 1)
                    text_color: 1, 1, 1, 1
                    on_release: app.limpar_brocas()

            MDCard:
                orientation: "vertical"
                padding: "16dp"
                spacing: "8dp"
                md_bg_color: (1, 1, 1, 1) if app.theme_cls.theme_style == "Light" else (0.16, 0.18, 0.21, 1)
                elevation: 6
                size_hint_y: None
                height: self.minimum_height
                radius: [12, 12, 12, 12]

                MDLabel:
                    text: "[b]Resumo do cálculo:[/b]"
                    markup: True
                    font_style: "Subtitle1"
                    halign: "left"
                    theme_text_color: "Custom"
                    text_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (1, 1, 1, 1)

                MDLabel:
                    id: resultado_brocas
                    text: "O resultado aparecerá aqui..."
                    markup: True
                    theme_text_color: "Custom"
                    text_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (1, 1, 1, 1)
                    halign: "left"
                    valign: "top"
                    font_style: "Body2"
                    text_size: self.width, None
                    size_hint_y: None
                    height: self.texture_size[1]

<TabBaldrame>:
    title: "Baldrame"
    orientation: "vertical"
    md_bg_color: (0.96, 0.96, 0.96, 1) if app.theme_cls.theme_style == "Light" else (0.10, 0.12, 0.14, 1)

    ScrollView:
        do_scroll_x: False

        MDBoxLayout:
            orientation: "vertical"
            padding: [24, 30, 24, 30]
            spacing: "22dp"
            adaptive_height: True
            size_hint_y: None
            height: self.minimum_height

            MDLabel:
                text: "[b]Cálculo de Baldrame[/b]"
                markup: True
                font_style: "H6"
                halign: "center"
                theme_text_color: "Custom"
                text_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (1, 1, 1, 1)

            MDCard:
                orientation: "vertical"
                padding: "20dp"
                spacing: "14dp"
                elevation: 6
                size_hint_y: None
                height: self.minimum_height
                md_bg_color: (1, 1, 1, 1) if app.theme_cls.theme_style == "Light" else (0.16, 0.18, 0.21, 1)
                radius: [12, 12, 12, 12]

                MDTextField:
                    id: comprimento_baldrame
                    hint_text: "Comprimento da vala/sapata (m)"
                    helper_text: "Soma total da vala ou sapata em metros"
                    helper_text_mode: "on_focus"
                    input_filter: None
                    multiline: False
                    on_text_validate: app.proximo_campo("abas", "tab_baldrame", "largura_baldrame")

                MDTextField:
                    id: largura_baldrame
                    hint_text: "Largura da vala/sapata (m)"
                    helper_text: "Use metro. Exemplo: 0.20"
                    helper_text_mode: "on_focus"
                    input_filter: None
                    multiline: False
                    on_text_validate: app.proximo_campo("abas", "tab_baldrame", "altura_baldrame")

                MDTextField:
                    id: altura_baldrame
                    hint_text: "Altura da vala/sapata (m)"
                    helper_text: "Use metro. Exemplo: 0.30"
                    helper_text_mode: "on_focus"
                    input_filter: None

                MDBoxLayout:
                    orientation: "horizontal"
                    size_hint_y: None
                    height: "56dp"
                    spacing: "10dp"

                    MDLabel:
                        text: "Proporção do concreto:"
                        halign: "left"
                        valign: "center"
                        size_hint_x: 0.55
                        theme_text_color: "Custom"
                        text_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (1, 1, 1, 1)

                    MDBoxLayout:
                        md_bg_color: (0.97, 0.97, 0.97, 1) if app.theme_cls.theme_style == "Light" else (0.22, 0.24, 0.28, 1)
                        radius: [10, 10, 10, 10]
                        elevation: 0
                        padding: [12, 0, 8, 0]
                        size_hint_x: 0.45
                        size_hint_y: None
                        height: "42dp"
                        pos_hint: {"center_y": 0.5}

                        MDDropDownItem:
                            id: proporcao_concreto_baldrame
                            text: "Selecione"
                            pos_hint: {"center_y": 0.5}
                            on_release: app.abrir_menu_proporcao(self)

            MDBoxLayout:
                spacing: "20dp"
                padding_y: "10dp"
                adaptive_height: True
                size_hint_y: None
                height: self.minimum_height
                pos_hint: {"center_x": 0.5}

                MDRaisedButton:
                    text: "CALCULAR"
                    md_bg_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (0.22, 0.38, 0.48, 1)
                    text_color: 1, 1, 1, 1
                    on_release: app.calcular_baldrame()

                MDRaisedButton:
                    text: "LIMPAR"
                    md_bg_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (0.22, 0.38, 0.48, 1)
                    text_color: 1, 1, 1, 1
                    on_release: app.limpar_baldrame()

            MDCard:
                orientation: "vertical"
                padding: "16dp"
                spacing: "8dp"
                md_bg_color: (1, 1, 1, 1) if app.theme_cls.theme_style == "Light" else (0.16, 0.18, 0.21, 1)
                elevation: 6
                size_hint_y: None
                height: self.minimum_height
                radius: [12, 12, 12, 12]

                MDLabel:
                    text: "[b]Resumo do cálculo:[/b]"
                    markup: True
                    font_style: "Subtitle1"
                    halign: "left"
                    theme_text_color: "Custom"
                    text_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (1, 1, 1, 1)

                MDLabel:
                    id: resultado_baldrame
                    text: "O resultado aparecerá aqui..."
                    markup: True
                    theme_text_color: "Custom"
                    text_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (1, 1, 1, 1)
                    halign: "left"
                    valign: "top"
                    font_style: "Body2"
                    text_size: self.width, None
                    size_hint_y: None
                    height: self.texture_size[1]

<TabParedes>:
    title: "Paredes"
    orientation: "vertical"
    md_bg_color: (0.96, 0.96, 0.96, 1) if app.theme_cls.theme_style == "Light" else (0.10, 0.12, 0.14, 1)

    ScrollView:
        do_scroll_x: False

        MDBoxLayout:
            orientation: "vertical"
            padding: [24, 30, 24, 30]
            spacing: "22dp"
            adaptive_height: True
            size_hint_y: None
            height: self.minimum_height

            MDLabel:
                text: "[b]Cálculo de Paredes[/b]"
                markup: True
                font_style: "H6"
                halign: "center"
                theme_text_color: "Custom"
                text_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (1, 1, 1, 1)

            MDCard:
                orientation: "vertical"
                padding: "20dp"
                spacing: "14dp"
                elevation: 6
                size_hint_y: None
                height: self.minimum_height
                md_bg_color: (1, 1, 1, 1) if app.theme_cls.theme_style == "Light" else (0.16, 0.18, 0.21, 1)
                radius: [12, 12, 12, 12]

                MDTextField:
                    id: area_parede
                    hint_text: "Área da(s) parede(s) em m²"
                    helper_text: "Some as áreas antes de inserir"
                    helper_text_mode: "on_focus"
                    input_filter: None
                    multiline: False
                    on_text_validate: app.proximo_campo("abas", "tab_paredes", "espaco_perdido_parede")

                MDTextField:
                    id: espaco_perdido_parede
                    hint_text: "Espaço perdido (portas/janelas) em m²"
                    helper_text: "Some as áreas de portas e janelas(Opcional)"
                    helper_text_mode: "on_focus"
                    input_filter: None

                MDBoxLayout:
                    orientation: "horizontal"
                    spacing: "10dp"
                    size_hint_y: None
                    height: "56dp"

                    MDLabel:
                        text: "Tipo de tijolo:"
                        halign: "left"
                        valign: "center"
                        size_hint_x: 0.52
                        theme_text_color: "Custom"
                        text_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (1, 1, 1, 1)

                    MDBoxLayout:
                        md_bg_color: (0.97, 0.97, 0.97, 1) if app.theme_cls.theme_style == "Light" else (0.22, 0.24, 0.28, 1)
                        radius: [10, 10, 10, 10]
                        elevation: 0
                        padding: [12, 0, 8, 0]
                        size_hint_x: 0.48
                        size_hint_y: None
                        height: "42dp"
                        pos_hint: {"center_y": 0.5}

                        MDDropDownItem:
                            id: tijolo_dropdown
                            text: "Selecione"
                            pos_hint: {"center_y": 0.5}
                            on_release: app.abrir_menu_tijolo(self)

                MDBoxLayout:
                    orientation: "horizontal"
                    spacing: "10dp"
                    size_hint_y: None
                    height: "56dp"

                    MDLabel:
                        text: "Margem para tijolos:"
                        halign: "left"
                        valign: "center"
                        size_hint_x: 0.52
                        theme_text_color: "Custom"
                        text_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (1, 1, 1, 1)

                    MDBoxLayout:
                        md_bg_color: (0.97, 0.97, 0.97, 1) if app.theme_cls.theme_style == "Light" else (0.22, 0.24, 0.28, 1)
                        radius: [10, 10, 10, 10]
                        elevation: 0
                        padding: [12, 0, 8, 0]
                        size_hint_x: 0.48
                        size_hint_y: None
                        height: "42dp"
                        pos_hint: {"center_y": 0.5}

                        MDDropDownItem:
                            id: margem_paredes_dropdown
                            text: "Selecione"
                            pos_hint: {"center_y": 0.5}
                            on_release: app.abrir_menu_margem(self)

                MDBoxLayout:
                    orientation: "horizontal"
                    size_hint_y: None
                    height: "56dp"
                    spacing: "10dp"

                    MDLabel:
                        text: "Proporção da massa:"
                        halign: "left"
                        valign: "center"
                        size_hint_x: 0.52
                        theme_text_color: "Custom"
                        text_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (1, 1, 1, 1)

                    MDBoxLayout:
                        md_bg_color: (0.97, 0.97, 0.97, 1) if app.theme_cls.theme_style == "Light" else (0.22, 0.24, 0.28, 1)
                        radius: [10, 10, 10, 10]
                        elevation: 0
                        padding: [12, 0, 8, 0]
                        size_hint_x: 0.48
                        size_hint_y: None
                        height: "42dp"
                        pos_hint: {"center_y": 0.5}

                        MDDropDownItem:
                            id: massa_dropdown
                            text: "Selecione"
                            pos_hint: {"center_y": 0.5}
                            on_release: app.abrir_menu_massa(self)

            MDBoxLayout:
                spacing: "20dp"
                padding_y: "10dp"
                adaptive_height: True
                size_hint_y: None
                height: self.minimum_height
                pos_hint: {"center_x": 0.5}

                MDRaisedButton:
                    text: "CALCULAR"
                    md_bg_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (0.22, 0.38, 0.48, 1)
                    text_color: 1, 1, 1, 1
                    on_release: app.calcular_paredes()

                MDRaisedButton:
                    text: "LIMPAR"
                    md_bg_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (0.22, 0.38, 0.48, 1)
                    text_color: 1, 1, 1, 1
                    on_release: app.limpar_paredes()

            MDCard:
                orientation: "vertical"
                padding: "16dp"
                spacing: "8dp"
                md_bg_color: (1, 1, 1, 1) if app.theme_cls.theme_style == "Light" else (0.16, 0.18, 0.21, 1)
                elevation: 6
                size_hint_y: None
                height: self.minimum_height
                radius: [12, 12, 12, 12]

                MDLabel:
                    text: "[b]Resumo do cálculo:[/b]"
                    markup: True
                    font_style: "Subtitle1"
                    halign: "left"
                    theme_text_color: "Custom"
                    text_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (1, 1, 1, 1)

                MDLabel:
                    id: resultado_paredes
                    text: "O resultado aparecerá aqui..."
                    markup: True
                    theme_text_color: "Custom"
                    text_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (1, 1, 1, 1)
                    halign: "left"
                    valign: "top"
                    font_style: "Body2"
                    text_size: self.width, None
                    size_hint_y: None
                    height: self.texture_size[1]

<TabReboco>:
    title: "Reboco"
    orientation: "vertical"
    md_bg_color: (0.96, 0.96, 0.96, 1) if app.theme_cls.theme_style == "Light" else (0.10, 0.12, 0.14, 1)

    ScrollView:
        MDBoxLayout:
            orientation: "vertical"
            padding: [24, 30, 24, 30]
            spacing: "22dp"
            adaptive_height: True
            size_hint_y: None
            height: self.minimum_height
            md_bg_color: (0.96, 0.96, 0.96, 1) if app.theme_cls.theme_style == "Light" else (0.10, 0.12, 0.14, 1)

            MDLabel:
                text: "[b]Cálculo de Reboco[/b]"
                markup: True
                font_style: "H6"
                halign: "center"
                theme_text_color: "Custom"
                text_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (1, 1, 1, 1)

            MDCard:
                orientation: "vertical"
                padding: "20dp"
                spacing: "14dp"
                elevation: 6
                size_hint_y: None
                height: self.minimum_height
                md_bg_color: (1, 1, 1, 1) if app.theme_cls.theme_style == "Light" else (0.16, 0.18, 0.21, 1)
                radius: [12, 12, 12, 12]

                MDTextField:
                    id: area_reboco
                    hint_text: "Área da(s) parede(s) em m²"
                    helper_text: "Some as áreas antes de inserir"
                    helper_text_mode: "on_focus"
                    input_filter: None
                    multiline: False
                    on_text_validate: app.proximo_campo("abas", "tab_reboco", "espaco_perdido_reboco")

                MDTextField:
                    id: espaco_perdido_reboco
                    hint_text: "Espaço perdido (portas/janelas) em m²"
                    helper_text: "Some portas e janelas(Opcional)"
                    helper_text_mode: "on_focus"
                    input_filter: None
                    multiline: False
                    on_text_validate: app.proximo_campo("abas", "tab_reboco", "espessura_reboco")

                MDTextField:
                    id: espessura_reboco
                    hint_text: "Espessura do reboco (m)"
                    helper_text: "Exemplo: 2 cm = 0.02 m"
                    helper_text_mode: "on_focus"
                    input_filter: None

                MDBoxLayout:
                    orientation: "horizontal"
                    size_hint_y: None
                    height: "56dp"
                    spacing: "10dp"

                    MDLabel:
                        text: "Proporção da massa:"
                        halign: "left"
                        valign: "center"
                        size_hint_x: 0.55
                        theme_text_color: "Custom"
                        text_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (1, 1, 1, 1)

                    MDBoxLayout:
                        md_bg_color: (0.97, 0.97, 0.97, 1) if app.theme_cls.theme_style == "Light" else (0.22, 0.24, 0.28, 1)
                        radius: [10, 10, 10, 10]
                        elevation: 0
                        padding: [12, 0, 8, 0]
                        size_hint_x: 0.45
                        size_hint_y: None
                        height: "42dp"
                        pos_hint: {"center_y": 0.5}

                        MDDropDownItem:
                            id: massa_reboco_dropdown
                            text: "Selecione"
                            pos_hint: {"center_y": 0.5}
                            on_release: app.abrir_menu_massa(self)

            MDBoxLayout:
                spacing: "20dp"
                padding_y: "10dp"
                adaptive_height: True
                size_hint_y: None
                height: self.minimum_height
                pos_hint: {"center_x": 0.5}

                MDRaisedButton:
                    text: "CALCULAR"
                    md_bg_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (0.22, 0.38, 0.48, 1)
                    text_color: 1, 1, 1, 1
                    on_release: app.calcular_reboco()

                MDRaisedButton:
                    text: "LIMPAR"
                    md_bg_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (0.22, 0.38, 0.48, 1)
                    text_color: 1, 1, 1, 1
                    on_release: app.limpar_reboco()

            MDCard:
                orientation: "vertical"
                padding: "16dp"
                spacing: "8dp"
                md_bg_color: (1, 1, 1, 1) if app.theme_cls.theme_style == "Light" else (0.16, 0.18, 0.21, 1)
                elevation: 6
                size_hint_y: None
                height: self.minimum_height
                radius: [12, 12, 12, 12]

                MDLabel:
                    text: "[b]Resumo do cálculo:[/b]"
                    markup: True
                    font_style: "Subtitle1"
                    halign: "left"
                    theme_text_color: "Custom"
                    text_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (1, 1, 1, 1)

                MDLabel:
                    id: resultado_reboco
                    text: "O resultado aparecerá aqui..."
                    markup: True
                    theme_text_color: "Custom"
                    text_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (1, 1, 1, 1)
                    halign: "left"
                    valign: "top"
                    font_style: "Body2"
                    text_size: self.width, None
                    size_hint_y: None
                    height: self.texture_size[1]

<TabContrapiso>:
    title: "Contrapiso"
    orientation: "vertical"
    md_bg_color: (0.96, 0.96, 0.96, 1) if app.theme_cls.theme_style == "Light" else (0.10, 0.12, 0.14, 1)

    ScrollView:
        MDBoxLayout:
            orientation: "vertical"
            padding: [24, 30, 24, 30]
            spacing: "22dp"
            adaptive_height: True
            size_hint_y: None
            height: self.minimum_height
            md_bg_color: (0.96, 0.96, 0.96, 1) if app.theme_cls.theme_style == "Light" else (0.10, 0.12, 0.14, 1)

            MDLabel:
                text: "[b]Cálculo de Contrapiso[/b]"
                markup: True
                font_style: "H6"
                halign: "center"
                theme_text_color: "Custom"
                text_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (1, 1, 1, 1)

            MDCard:
                orientation: "vertical"
                padding: "20dp"
                spacing: "14dp"
                elevation: 6
                size_hint_y: None
                height: self.minimum_height
                md_bg_color: (1, 1, 1, 1) if app.theme_cls.theme_style == "Light" else (0.16, 0.18, 0.21, 1)
                radius: [12, 12, 12, 12]

                MDTextField:
                    id: area_contrapiso
                    hint_text: "Área do(s) cômodo(s) em m²"
                    helper_text: "Some as áreas antes de inserir"
                    helper_text_mode: "on_focus"
                    input_filter: None
                    multiline: False
                    on_text_validate: app.proximo_campo("abas", "tab_contrapiso", "espessura_contrapiso")

                MDTextField:
                    id: espessura_contrapiso
                    hint_text: "Espessura do contrapiso (m)"
                    helper_text: "Exemplo: 5 cm = 0.05 m"
                    helper_text_mode: "on_focus"
                    input_filter: None

                MDBoxLayout:
                    orientation: "horizontal"
                    size_hint_y: None
                    height: "56dp"
                    spacing: "10dp"

                    MDLabel:
                        text: "Proporção do concreto:"
                        halign: "left"
                        valign: "center"
                        size_hint_x: 0.55
                        theme_text_color: "Custom"
                        text_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (1, 1, 1, 1)

                    MDBoxLayout:
                        md_bg_color: (0.97, 0.97, 0.97, 1) if app.theme_cls.theme_style == "Light" else (0.22, 0.24, 0.28, 1)
                        radius: [10, 10, 10, 10]
                        elevation: 0
                        padding: [12, 0, 8, 0]
                        size_hint_x: 0.45
                        size_hint_y: None
                        height: "42dp"
                        pos_hint: {"center_y": 0.5}

                        MDDropDownItem:
                            id: proporcao_contrapiso_dropdown
                            text: "Selecione"
                            pos_hint: {"center_y": 0.5}
                            on_release: app.abrir_menu_proporcao(self)

            MDBoxLayout:
                spacing: "20dp"
                padding_y: "10dp"
                adaptive_height: True
                size_hint_y: None
                height: self.minimum_height
                pos_hint: {"center_x": 0.5}

                MDRaisedButton:
                    text: "CALCULAR"
                    md_bg_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (0.22, 0.38, 0.48, 1)
                    text_color: 1, 1, 1, 1
                    on_release: app.calcular_contrapiso()

                MDRaisedButton:
                    text: "LIMPAR"
                    md_bg_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (0.22, 0.38, 0.48, 1)
                    text_color: 1, 1, 1, 1
                    on_release: app.limpar_contrapiso()

            MDCard:
                orientation: "vertical"
                padding: "16dp"
                spacing: "8dp"
                md_bg_color: (1, 1, 1, 1) if app.theme_cls.theme_style == "Light" else (0.16, 0.18, 0.21, 1)
                elevation: 6
                size_hint_y: None
                height: self.minimum_height
                radius: [12, 12, 12, 12]

                MDLabel:
                    text: "[b]Resumo do cálculo:[/b]"
                    markup: True
                    font_style: "Subtitle1"
                    halign: "left"
                    theme_text_color: "Custom"
                    text_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (1, 1, 1, 1)

                MDLabel:
                    id: resultado_contrapiso
                    text: "O resultado aparecerá aqui..."
                    markup: True
                    theme_text_color: "Custom"
                    text_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (1, 1, 1, 1)
                    halign: "left"
                    valign: "top"
                    font_style: "Body2"
                    text_size: self.width, None
                    size_hint_y: None
                    height: self.texture_size[1]

<TabRevestimento>:
    id: tab_revest
    title: "Revestimento"
    orientation: "vertical"
    md_bg_color: (0.96, 0.96, 0.96, 1) if app.theme_cls.theme_style == "Light" else (0.10, 0.12, 0.14, 1)

    ScrollView:
        id: scroll_revestimento
        do_scroll_x: False

        MDBoxLayout:
            orientation: "vertical"
            padding: [20, 20, 20, 20]
            spacing: dp(18)
            adaptive_height: True
            size_hint_y: None
            height: self.minimum_height
            md_bg_color: (0.96, 0.96, 0.96, 1) if app.theme_cls.theme_style == "Light" else (0.10, 0.12, 0.14, 1)

            MDLabel:
                text: "Tipo de revestimento:"
                font_style: "Subtitle1"
                halign: "left"
                size_hint_y: None
                height: dp(28)
                theme_text_color: "Custom"
                text_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (1, 1, 1, 1)

            MDBoxLayout:
                orientation: "vertical"
                spacing: dp(4)
                adaptive_height: True

                MDBoxLayout:
                    spacing: dp(6)
                    size_hint_y: None
                    height: dp(24)

                    MDCheckbox:
                        id: cb_piso
                        group: "rev"
                        on_active: app.mostrar_revestimento("piso", self.active, tab_revest)
                        size_hint_x: None
                        size: dp(24), dp(24)

                    MDLabel:
                        text: "Piso"
                        halign: "left"
                        valign: "middle"
                        theme_text_color: "Custom"
                        text_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (1, 1, 1, 1)

                MDBoxLayout:
                    spacing: dp(6)
                    size_hint_y: None
                    height: dp(24)

                    MDCheckbox:
                        id: cb_azulejo
                        group: "rev"
                        on_active: app.mostrar_revestimento("azulejo", self.active, tab_revest)
                        size_hint_x: None
                        size: dp(24), dp(24)

                    MDLabel:
                        text: "Azulejos"
                        halign: "left"
                        valign: "middle"
                        theme_text_color: "Custom"
                        text_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (1, 1, 1, 1)

                MDBoxLayout:
                    spacing: dp(6)
                    size_hint_y: None
                    height: dp(24)

                    MDCheckbox:
                        id: cb_ambos
                        group: "rev"
                        on_active: app.mostrar_revestimento("ambos", self.active, tab_revest)
                        size_hint_x: None
                        size: dp(24), dp(24)

                    MDLabel:
                        text: "Ambos"
                        halign: "left"
                        valign: "middle"
                        theme_text_color: "Custom"
                        text_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (1, 1, 1, 1)

            MDCard:
                id: card_piso
                orientation: "vertical"
                padding: "20dp"
                spacing: "14dp"
                elevation: 6
                size_hint_y: None
                height: 0
                opacity: 0
                disabled: True
                md_bg_color: (1, 1, 1, 1) if app.theme_cls.theme_style == "Light" else (0.16, 0.18, 0.21, 1)
                radius: [12, 12, 12, 12]

                MDLabel:
                    text: "[b]Cálculo de Piso[/b]"
                    markup: True
                    font_style: "H6"
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (1, 1, 1, 1)

                MDTextField:
                    id: area_piso
                    hint_text: "Área do(s) cômodo(s) em m²"
                    helper_text: "Ex.: 12.5"
                    helper_text_mode: "on_focus"
                    input_filter: None
                    multiline: False

                MDBoxLayout:
                    orientation: "horizontal"
                    size_hint_y: None
                    height: "56dp"
                    spacing: "10dp"

                    MDLabel:
                        text: "Dimensão da peça:"
                        halign: "left"
                        valign: "center"
                        size_hint_x: 0.52
                        theme_text_color: "Custom"
                        text_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (1, 1, 1, 1)

                    MDBoxLayout:
                        md_bg_color: (0.97, 0.97, 0.97, 1) if app.theme_cls.theme_style == "Light" else (0.22, 0.24, 0.28, 1)
                        radius: [10, 10, 10, 10]
                        elevation: 0
                        padding: [12, 0, 8, 0]
                        size_hint_x: 0.48
                        size_hint_y: None
                        height: "42dp"
                        pos_hint: {"center_y": 0.5}

                        MDDropDownItem:
                            id: tamanho_piso_drop
                            text: "Selecione"
                            pos_hint: {"center_y": 0.5}
                            on_release: app.abrir_menu_revest_dimensao(self)

                MDBoxLayout:
                    orientation: "horizontal"
                    size_hint_y: None
                    height: "56dp"
                    spacing: "10dp"

                    MDLabel:
                        text: "Largura da junta (mm):"
                        halign: "left"
                        valign: "center"
                        size_hint_x: 0.52
                        theme_text_color: "Custom"
                        text_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (1, 1, 1, 1)

                    MDBoxLayout:
                        md_bg_color: (0.97, 0.97, 0.97, 1) if app.theme_cls.theme_style == "Light" else (0.22, 0.24, 0.28, 1)
                        radius: [10, 10, 10, 10]
                        elevation: 0
                        padding: [12, 0, 8, 0]
                        size_hint_x: 0.48
                        size_hint_y: None
                        height: "42dp"
                        pos_hint: {"center_y": 0.5}

                        MDDropDownItem:
                            id: junta_piso_drop
                            text: "Selecione"
                            pos_hint: {"center_y": 0.5}
                            on_release: app.abrir_menu_revest_junta(self)

            MDCard:
                id: card_azulejo
                orientation: "vertical"
                padding: "20dp"
                spacing: "14dp"
                elevation: 6
                size_hint_y: None
                height: 0
                opacity: 0
                disabled: True
                md_bg_color: (1, 1, 1, 1) if app.theme_cls.theme_style == "Light" else (0.16, 0.18, 0.21, 1)
                radius: [12, 12, 12, 12]

                MDLabel:
                    text: "[b]Cálculo de Azulejo[/b]"
                    markup: True
                    font_style: "H6"
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (1, 1, 1, 1)

                MDTextField:
                    id: area_azulejo
                    hint_text: "Área da parede em m²"
                    helper_text: "Ex.: 12.5"
                    helper_text_mode: "on_focus"
                    input_filter: None
                    multiline: False

                MDBoxLayout:
                    orientation: "horizontal"
                    size_hint_y: None
                    height: "56dp"
                    spacing: "10dp"

                    MDLabel:
                        text: "Dimensão da peça:"
                        halign: "left"
                        valign: "center"
                        size_hint_x: 0.52
                        theme_text_color: "Custom"
                        text_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (1, 1, 1, 1)

                    MDBoxLayout:
                        md_bg_color: (0.97, 0.97, 0.97, 1) if app.theme_cls.theme_style == "Light" else (0.22, 0.24, 0.28, 1)
                        radius: [10, 10, 10, 10]
                        elevation: 0
                        padding: [12, 0, 8, 0]
                        size_hint_x: 0.48
                        size_hint_y: None
                        height: "42dp"
                        pos_hint: {"center_y": 0.5}

                        MDDropDownItem:
                            id: tamanho_az_drop
                            text: "Selecione"
                            pos_hint: {"center_y": 0.5}
                            on_release: app.abrir_menu_revest_dimensao(self)

                MDBoxLayout:
                    orientation: "horizontal"
                    size_hint_y: None
                    height: "56dp"
                    spacing: "10dp"

                    MDLabel:
                        text: "Largura da junta (mm):"
                        halign: "left"
                        valign: "center"
                        size_hint_x: 0.52
                        theme_text_color: "Custom"
                        text_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (1, 1, 1, 1)

                    MDBoxLayout:
                        md_bg_color: (0.97, 0.97, 0.97, 1) if app.theme_cls.theme_style == "Light" else (0.22, 0.24, 0.28, 1)
                        radius: [10, 10, 10, 10]
                        elevation: 0
                        padding: [12, 0, 8, 0]
                        size_hint_x: 0.48
                        size_hint_y: None
                        height: "42dp"
                        pos_hint: {"center_y": 0.5}

                        MDDropDownItem:
                            id: junta_az_drop
                            text: "Selecione"
                            pos_hint: {"center_y": 0.5}
                            on_release: app.abrir_menu_revest_junta(self)

            BoxLayout:
                spacing: "20dp"
                size_hint_y: None
                height: "48dp"
                size_hint_x: 1

                MDRaisedButton:
                    text: "CALCULAR"
                    md_bg_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (0.22, 0.38, 0.48, 1)
                    text_color: 1, 1, 1, 1
                    on_release: app.calcular_revestimento()

                MDRaisedButton:
                    text: "LIMPAR"
                    md_bg_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (0.22, 0.38, 0.48, 1)
                    text_color: 1, 1, 1, 1
                    on_release: app.limpar_revestimento()

            MDCard:
                orientation: "vertical"
                padding: "16dp"
                spacing: "8dp"
                md_bg_color: (1, 1, 1, 1) if app.theme_cls.theme_style == "Light" else (0.16, 0.18, 0.21, 1)
                elevation: 6
                size_hint_y: None
                height: self.minimum_height
                radius: [12, 12, 12, 12]

                MDLabel:
                    text: "[b]Resumo do cálculo:[/b]"
                    markup: True
                    font_style: "Subtitle1"
                    halign: "left"
                    theme_text_color: "Custom"
                    text_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (1, 1, 1, 1)

                MDLabel:
                    id: resultado_revestimento
                    text: "O resultado aparecerá aqui..."
                    markup: True
                    theme_text_color: "Custom"
                    text_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (1, 1, 1, 1)
                    halign: "left"
                    valign: "top"
                    font_style: "Body2"
                    text_size: self.width, None
                    size_hint_y: None
                    height: self.texture_size[1]

<TabOrcamento>:
    title: "Orçamento"
    orientation: "vertical"
    md_bg_color: (0.96, 0.96, 0.96, 1) if app.theme_cls.theme_style == "Light" else (0.10, 0.12, 0.14, 1)

    ScrollView:
        MDBoxLayout:
            orientation: "vertical"
            padding: [24, 30, 24, 30]
            spacing: "22dp"
            adaptive_height: True
            size_hint_y: None
            height: self.minimum_height
            md_bg_color: (0.96, 0.96, 0.96, 1) if app.theme_cls.theme_style == "Light" else (0.10, 0.12, 0.14, 1)

            MDLabel:
                text: "[b]Orçamento[/b]"
                markup: True
                font_style: "H6"
                halign: "center"
                theme_text_color: "Custom"
                text_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (1, 1, 1, 1)

            MDCard:
                orientation: "vertical"
                padding: "20dp"
                spacing: "14dp"
                elevation: 3
                size_hint_y: None
                height: self.minimum_height
                md_bg_color: (1, 1, 1, 1) if app.theme_cls.theme_style == "Light" else (0.16, 0.18, 0.21, 1)
                radius: [12, 12, 12, 12]

                MDLabel:
                    text: "Insira os valores dos materiais:"
                    font_style: "Subtitle1"
                    halign: "left"
                    theme_text_color: "Custom"
                    text_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (1, 1, 1, 1)

                MDBoxLayout:
                    orientation: "horizontal"
                    size_hint_y: None
                    height: "56dp"
                    spacing: "10dp"

                    MDLabel:
                        text: "Tipo de tijolo:"
                        size_hint_x: 0.5
                        theme_text_color: "Custom"
                        text_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (1, 1, 1, 1)

                    MDBoxLayout:
                        md_bg_color: (0.97, 0.97, 0.97, 1) if app.theme_cls.theme_style == "Light" else (0.22, 0.24, 0.28, 1)
                        radius: [10, 10, 10, 10]
                        elevation: 3
                        padding: [10, 0, 5, 0]
                        size_hint_x: 0.5
                        height: "40dp"
                        pos_hint: {"center_y": 0.5}

                        MDDropDownItem:
                            id: tipo_tijolo_orcamento
                            text: "Tijolo Baiano"
                            pos_hint: {"center_y": 0.5}
                            on_release: app.abrir_menu_tijolo(self)

                MDTextField:
                    id: preco_tijolo
                    hint_text: "Preço do tijolo (unidade)"
                    helper_text: "Valor por unidade"
                    helper_text_mode: "on_focus"
                    input_filter: None
                    multiline: False
                    on_text_validate: app.proximo_campo("abas", "tab_orcamento", "preco_cimento")

                MDSeparator:
                    height: "1dp"

                MDTextField:
                    id: preco_cimento
                    hint_text: "Cimento (50kg) - R$"
                    helper_text: "Preço por saco de 50kg"
                    helper_text_mode: "on_focus"
                    input_filter: None
                    multiline: False
                    on_text_validate: app.proximo_campo("abas", "tab_orcamento", "preco_cal")

                MDTextField:
                    id: preco_cal
                    hint_text: "Cal (20kg) - R$"
                    helper_text: "Preço por saco de 20kg"
                    helper_text_mode: "on_focus"
                    input_filter: None
                    multiline: False
                    on_text_validate: app.proximo_campo("abas", "tab_orcamento", "preco_areia")

                MDTextField:
                    id: preco_areia
                    hint_text: "Areia (m³) - R$"
                    helper_text: "Preço por metro cúbico"
                    helper_text_mode: "on_focus"
                    input_filter: None
                    multiline: False
                    on_text_validate: app.proximo_campo("abas", "tab_orcamento", "preco_pedra")

                MDTextField:
                    id: preco_pedra
                    hint_text: "Pedra (m³) - R$"
                    helper_text: "Preço por metro cúbico"
                    helper_text_mode: "on_focus"
                    input_filter: None
                    multiline: False
                    on_text_validate: app.proximo_campo("abas", "tab_orcamento", "preco_argamassa")

                MDTextField:
                    id: preco_argamassa
                    hint_text: "Argamassa (20kg) - R$"
                    helper_text: "Preço por saco de 20kg"
                    helper_text_mode: "on_focus"
                    input_filter: None
                    multiline: False
                    on_text_validate: app.proximo_campo("abas", "tab_orcamento", "preco_rejunte")

                MDTextField:
                    id: preco_rejunte
                    hint_text: "Rejunte (kg) - R$"
                    helper_text: "Preço por kg"
                    helper_text_mode: "on_focus"
                    input_filter: None
                    multiline: False
                    on_text_validate: app.calcular_orcamento()

            MDBoxLayout:
                spacing: "20dp"
                padding_y: "10dp"
                adaptive_height: True
                size_hint_y: None
                height: self.minimum_height
                pos_hint: {"center_x": 0.5}

                MDRaisedButton:
                    text: "CALCULAR"
                    md_bg_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (0.22, 0.38, 0.48, 1)
                    text_color: 1, 1, 1, 1
                    on_release: app.calcular_orcamento()

                MDRaisedButton:
                    text: "LIMPAR"
                    md_bg_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (0.22, 0.38, 0.48, 1)
                    text_color: 1, 1, 1, 1
                    on_release: app.limpar_orcamento()

            MDCard:
                orientation: "vertical"
                padding: "16dp"
                spacing: "8dp"
                md_bg_color: (1, 1, 1, 1) if app.theme_cls.theme_style == "Light" else (0.16, 0.18, 0.21, 1)
                elevation: 3
                size_hint_y: None
                height: self.minimum_height
                radius: [12, 12, 12, 12]

                MDLabel:
                    text: "[b]Resumo do orçamento:[/b]"
                    markup: True
                    font_style: "Subtitle1"
                    halign: "left"
                    theme_text_color: "Custom"
                    text_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (1, 1, 1, 1)

                MDLabel:
                    id: resultado_orcamento
                    text: "Os valores serão usados no resumo da obra."
                    markup: True
                    theme_text_color: "Custom"
                    text_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (1, 1, 1, 1)
                    halign: "left"
                    valign: "top"
                    font_style: "Body2"
                    text_size: self.width, None
                    size_hint_y: None
                    height: self.texture_size[1]

<TabResumo>:
    title: "Resumo"
    orientation: "vertical"
    md_bg_color: (0.96, 0.96, 0.96, 1) if app.theme_cls.theme_style == "Light" else (0.10, 0.12, 0.14, 1)

    ScrollView:
        MDBoxLayout:
            orientation: "vertical"
            padding: [20, 20, 20, 20]
            spacing: dp(18)
            adaptive_height: True
            size_hint_y: None
            md_bg_color: (0.96, 0.96, 0.96, 1) if app.theme_cls.theme_style == "Light" else (0.10, 0.12, 0.14, 1)

            MDLabel:
                text: "[b]Resumo dos cálculos[/b]"
                markup: True
                font_style: "H6"
                halign: "center"
                size_hint_y: None
                height: dp(30)
                theme_text_color: "Custom"
                text_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (1, 1, 1, 1)

            MDCard:
                orientation: "vertical"
                padding: dp(12)
                size_hint_y: None
                adaptive_height: True
                md_bg_color: (1, 1, 1, 1) if app.theme_cls.theme_style == "Light" else (0.16, 0.18, 0.21, 1)
                elevation: 2
                radius: [12]

                MDLabel:
                    id: resultado_resumo
                    text: "O resumo aparecerá aqui..."
                    markup: True
                    theme_text_color: "Custom"
                    text_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (1, 1, 1, 1)
                    halign: "left"
                    valign: "top"
                    font_style: "Body2"
                    text_size: self.width, None
                    size_hint_y: None
                    height: self.texture_size[1]

            MDBoxLayout:
                size_hint_y: None
                height: dp(56)
                padding: [0, 10, 0, 0]
                spacing: dp(12)
                pos_hint: {"center_x": 0.5}

                MDRaisedButton:
                    text: "Salvar obra"
                    md_bg_color: (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (0.22, 0.38, 0.48, 1)
                    text_color: 1, 1, 1, 1
                    size_hint_x: 1
                    on_release: app.abrir_dialog_salvar_obra()

<ObraCard>:
    orientation: "vertical"
    padding: dp(18)
    spacing: dp(10)
    radius: [20, 20, 20, 20]
    elevation: 3
    md_bg_color: (1,1,1,1) if app.theme_cls.theme_style == "Light" else (0.16, 0.18, 0.21, 1)

    MDBoxLayout:
        orientation: "vertical"
        spacing: dp(4)

        MDBoxLayout:
            orientation: "horizontal"
            spacing: dp(8)
            size_hint_y: None
            height: dp(28)

            MDIcon:
                icon: "home"
                theme_text_color: "Custom"
                text_color: (0.15,0.3,0.39,1)
                size_hint: None, None
                size: dp(22), dp(22)

            MDLabel:
                text: root.nome_obra
                font_style: "H5"
                bold: True
                theme_text_color: "Custom"
                text_color: (0.1,0.1,0.1,1) if app.theme_cls.theme_style == "Light" else (1,1,1,1)
                valign: "middle"

        MDLabel:
            text: root.data_obra
            font_style: "Caption"
            theme_text_color: "Custom"
            text_color: (0.5,0.5,0.5,1) if app.theme_cls.theme_style == "Light" else (0.7,0.7,0.7,1)

    MDBoxLayout:
        size_hint_y: None
        height: dp(30)

        MDLabel:
            text: "[b]BROCAS[/b]"
            markup: True
            size_hint_x: None
            width: dp(90)
            halign: "center"
            valign: "middle"
            theme_text_color: "Custom"
            text_color: (0.15,0.3,0.39,1)

            canvas.before:
                Color:
                    rgba: (0.9,0.95,1,1) if app.theme_cls.theme_style == "Light" else (0.2,0.3,0.4,1)
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [10]

    MDLabel:
        text: root.resumo_obra
        theme_text_color: "Custom"
        text_color: (0.2,0.2,0.2,1) if app.theme_cls.theme_style == "Light" else (0.85,0.85,0.85,1)
        font_style: "Body2"
        text_size: self.width, None
        size_hint_y: None
        height: self.texture_size[1]

    MDSeparator:
        color: (0,0,0,0.1) if app.theme_cls.theme_style == "Light" else (1,1,1,0.08)

    MDBoxLayout:
        size_hint_y: None
        height: dp(40)
        spacing: dp(6)

        MDIconButton:
            icon: "eye-outline"
            theme_text_color: "Custom"
            text_color: (0.2,0.2,0.2,1) if app.theme_cls.theme_style == "Light" else (1,1,1,1)
            on_release: app.abrir_obra(root.index_obra)

        MDIconButton:
            icon: "pencil"
            theme_text_color: "Custom"
            text_color: (0.2,0.2,0.2,1) if app.theme_cls.theme_style == "Light" else (1,1,1,1)
            on_release: app.renomear_obra(root.index_obra)

        MDIconButton:
            icon: "file-edit-outline"
            theme_text_color: "Custom"
            text_color: (0.2,0.2,0.2,1) if app.theme_cls.theme_style == "Light" else (1,1,1,1)
            on_release: app.editar_obra(root.index_obra)

        MDIconButton:
            icon: "content-copy"
            theme_text_color: "Custom"
            text_color: (0.2,0.2,0.2,1) if app.theme_cls.theme_style == "Light" else (1,1,1,1)
            on_release: app.duplicar_obra(root.index_obra)

        MDIconButton:
            icon: "delete-outline"
            theme_text_color: "Custom"
            text_color: (0.85,0.2,0.2,1)
            on_release: app.excluir_obra(root.index_obra)

        Widget:

        MDIconButton:
            icon: "share-variant"
            theme_text_color: "Custom"
            text_color: (0.2,0.2,0.2,1) if app.theme_cls.theme_style == "Light" else (1,1,1,1)
            on_release: app.compartilhar_obra(root.index_obra)
'''

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.tab import MDTabsBase

class TabBrocas(MDBoxLayout, MDTabsBase):
    pass

class TabBaldrame(MDBoxLayout, MDTabsBase):
    pass

class TabParedes(MDBoxLayout, MDTabsBase):
    pass

class TabReboco(MDBoxLayout, MDTabsBase):
    pass

class TabContrapiso(MDBoxLayout, MDTabsBase):
    pass

class TabRevestimento(MDBoxLayout, MDTabsBase):
    pass

class TabOrcamento(MDBoxLayout, MDTabsBase):
    pass

class TabResumo(MDBoxLayout, MDTabsBase):
    pass


class ObraCard(MDCard):
    nome_obra = StringProperty("")
    data_obra = StringProperty("")
    resumo_obra = StringProperty("")
    index_obra = NumericProperty(0)

class BuildCalcApp(MDApp):

#------------------------------------------------------
#   Dados dos materiais para os cálculos
#------------------------------------------------------

    tijolos = {
        "Tijolo Baiano": {"altura": 0.19, "comprimento": 0.19, "massa_por_m2": 15},
        "Tijolo Baiano 9 Furos": {"altura": 0.14, "comprimento": 0.19, "massa_por_m2": 18},
        "Bloco de Concreto": {"altura": 0.39, "comprimento": 0.19, "massa_por_m2": 12},
    }

    massas = {
        "1:0.5:6": {"cimento": 1, "cal": 0.5, "areia": 6},
        "1.5:1:8": {"cimento": 1.5, "cal": 1, "areia": 8},
        "1:0:3": {"cimento": 1, "cal": 0, "areia": 3},
        "1.5:0:4": {"cimento": 1.5, "cal": 0, "areia": 4},
    }

    DENSIDADE_CIMENTO = 1500
    DENSIDADE_CAL = 1100

    consumo_rejunte = {
        "30x30": {1: 3.5, 2: 2.2, 3: 1.7, 4: 1.3, 5: 1.1},
        "40x40": {1: 4.6, 2: 3.0, 3: 2.2, 4: 1.7, 5: 1.4},
        "45x45": {1: 5.2, 2: 3.4, 3: 2.5, 4: 2.0, 5: 1.6},
        "50x50": {1: 5.8, 2: 3.8, 3: 2.8, 4: 2.2, 5: 1.8},
        "60x60": {1: 7.0, 2: 4.6, 3: 3.4, 4: 2.6, 5: 2.2},
        "80x80": {1: 9.2, 2: 6.1, 3: 4.5, 4: 3.6, 5: 3.0},
        "100x100": {1: 11.5, 2: 7.7, 3: 5.8, 4: 4.6, 5: 3.8},
        "120x120": {1: 13.8, 2: 9.2, 3: 6.9, 4: 5.5, 5: 4.6},
        "150x150": {1: 17.3, 2: 11.5, 3: 8.6, 4: 6.9, 5: 5.5},
    }

    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.theme_style = "Light"

        self.carregar_historico_json()

        return Builder.load_string(KV)

#------------------------------------------------------
#   Funções de construção da interface e navegação
#------------------------------------------------------
    def mostrar_snackbar(self, mensagem):
        snackbar = Snackbar(
            duration=2,
            size_hint_x=1,  # 👈 ocupa tudo
            pos_hint={"center_x": 0.5, "y": 0},  # 👈 colado embaixo
            md_bg_color=(0.12, 0.14, 0.17, 1),
            radius=[16, 16, 0, 0],  # 👈 só topo arredondado
        )

        label = MDLabel(
            text=mensagem,
            halign="left",
            valign="middle",
            size_hint_y=None,
            height=dp(24),  # 👈 bem menor
            padding=(dp(12), dp(2)),  # 👈 quase sem espaço vertical
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_style="Caption",  # 👈 fonte menor
        )

        snackbar.add_widget(label)
        snackbar.open()

    def mostrar_snackbar_desfazer(self):

        snackbar = Snackbar(
            duration=3
        )

        label = MDLabel(
            text="🗑️ Obra excluída com sucesso",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1)
        )

        snackbar.add_widget(label)
        snackbar.open()

    def mostrar_resultado_label(self, label, texto):
        if not label:
            return
        label.text = texto
        label.texture_update()
        label.height = max(label.texture_size[1], dp(24))

    def on_start(self):
        self.atualizar_historico()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.texto_brocas = ""
        self.texto_baldrame = ""
        self.texto_paredes = ""
        self.texto_reboco = ""
        self.texto_contrapiso = ""
        self.texto_revestimento = ""
        self.texto_resumo = ""
        self.proporcao_brocas = "Selecione"
        self.proporcao_baldrame = "Selecione"
        self.proporcao_contrapiso_dropdown = "Selecione"
        self.aba_atual = "Brocas"
        self.historico_obras = []
        self.arquivo_historico = "historico_obras.json"
        self.ultima_obra_excluida = None
        self.indice_ultima_exclusao = None

        self.precos_materiais = {
            "tijolo_escolhido": 0.0,
            "cimento_50kg": 0.0,
            "cal_20kg": 0.0,
            "areia_m3": 0.0,
            "pedra_m3": 0.0,
            "argamassa_20kg": 0.0,
            "rejunte_kg": 0.0,
        }

    def voltar_inicio(self):
        self.root.transition = SlideTransition(direction="right", duration=0.35)
        self.root.current = "inicio"

    def abrir_historico(self):
        self.root.transition = SlideTransition(direction="left", duration=0.35)
        self.root.current = "historico"
        tela = self.root.get_screen("historico")
        tela.ids.filtro_obra.text = ""
        self.esconder_feedback_obra_salva()
        self.atualizar_historico()

    def esconder_feedback_obra_salva(self):
        tela = self.root.get_screen("historico")
        card = tela.ids.card_feedback

        card.height = 0
        card.opacity = 0
        card.disabled = True

    def abrir_abas(self):
        self.root.transition = SlideTransition(direction="left", duration=0.35)
        self.root.current = "abas"

    def _tela_abas(self):
        return self.root.get_screen("abas")

    def _tabs(self):
        return self._tela_abas().ids.tabs

    def _ids_brocas(self):
        return self._tela_abas().ids.tab_brocas.ids

    def _ids_baldrame(self):
        return self._tela_abas().ids.tab_baldrame.ids

    def _ids_paredes(self):
        return self._tela_abas().ids.tab_paredes.ids

    def _ids_reboco(self):
        return self._tela_abas().ids.tab_reboco.ids

    def _ids_contrapiso(self):
        return self._tela_abas().ids.tab_contrapiso.ids

    def _ids_revestimento(self):
        return self._tela_abas().ids.tab_revestimento.ids

    def _ids_orcamento(self):
        return self._tela_abas().ids.tab_orcamento.ids

    def _ids_resumo(self):
        return self._tela_abas().ids.tab_resumo.ids

#------------------------------------------------------
#   Funções para abertura dos menus dropdown e definição dos valores
#------------------------------------------------------

    def abrir_menu_proporcao(self, caller):
        proporcoes = ["1:3:3", "1:4:3", "1.5:5:5"]

        items = [{
            "viewclass": "OneLineListItem",
            "text": p,
            "height": dp(48),
            "on_release": lambda x=p: self.definir_proporcao(caller, x),
        } for p in proporcoes]

        if hasattr(self, "menu_proporcao") and self.menu_proporcao:
            self.menu_proporcao.dismiss()

        self.menu_proporcao = MDDropdownMenu(
            caller=caller,
            items=items,
            width_mult=3,
            max_height=dp(180),
            background_color=(1, 1, 1, 1),
            radius=[12, 12, 12, 12],
        )
        self.menu_proporcao.open()

    def definir_proporcao(self, caller, valor):
        caller.set_item(valor)
        caller.text = valor
        caller.current_item = valor

        if hasattr(self, "menu_proporcao") and self.menu_proporcao:
            self.menu_proporcao.dismiss()

    def abrir_menu_tijolo(self, caller):
        itens = [{
            "viewclass": "OneLineListItem",
            "text": t,
            "height": dp(48),
            "on_release": lambda x=t: self.definir_tijolo(caller, x)
        } for t in self.tijolos.keys()]

        if hasattr(self, "menu_tijolo") and self.menu_tijolo:
            self.menu_tijolo.dismiss()

        self.menu_tijolo = MDDropdownMenu(
            caller=caller,
            items=itens,
            width_mult=4
        )
        self.menu_tijolo.open()

    def definir_tijolo(self, caller, valor):
        caller.set_item(valor)
        caller.text = valor
        caller.current_item = valor
        if hasattr(self, "menu_tijolo") and self.menu_tijolo:
            self.menu_tijolo.dismiss()

    def abrir_menu_massa(self, caller):
        itens = [{
            "viewclass": "OneLineListItem",
            "text": p,
            "height": dp(48),
            "on_release": lambda x=p: self.definir_massa(caller, x)
        } for p in self.massas.keys()]

        if hasattr(self, "menu_massa") and self.menu_massa:
            self.menu_massa.dismiss()

        self.menu_massa = MDDropdownMenu(
            caller=caller,
            items=itens,
            width_mult=4
        )
        self.menu_massa.open()

    def definir_massa(self, caller, valor):
        caller.set_item(valor)
        caller.text = valor
        caller.current_item = valor
        if hasattr(self, "menu_massa") and self.menu_massa:
            self.menu_massa.dismiss()

    def abrir_menu_massa_reboco(self, caller):
        itens = [{
            "viewclass": "OneLineListItem",
            "text": p,
            "height": dp(48),
            "on_release": lambda x=p: self.definir_massa_reboco(caller, x)
        } for p in self.massas.keys()]

        if hasattr(self, "menu_massa_reboco") and self.menu_massa_reboco:
            self.menu_massa_reboco.dismiss()

        self.menu_massa_reboco = MDDropdownMenu(
            caller=caller,
            items=itens,
            width_mult=4
        )
        self.menu_massa_reboco.open()

    def definir_massa_reboco(self, caller, valor):
        caller.set_item(valor)
        caller.text = valor
        caller.current_item = valor
        if hasattr(self, "menu_massa_reboco") and self.menu_massa_reboco:
            self.menu_massa_reboco.dismiss()

    def abrir_menu_revest_dimensao(self, caller):
        tamanhos = [
            "30x30", "40x40", "45x45", "50x50",
            "60x60", "80x80", "100x100", "120x120", "150x150"
        ]

        itens = [{
            "viewclass": "OneLineListItem",
            "text": t,
            "height": dp(48),
            "on_release": lambda x=t: self.definir_dimensao(caller, x),
        } for t in tamanhos]

        if hasattr(self, "menu_dim") and self.menu_dim:
            self.menu_dim.dismiss()

        self.menu_dim = MDDropdownMenu(
            caller=caller,
            items=itens,
            width_mult=4
        )
        self.menu_dim.open()

    def definir_dimensao(self, caller, valor):
        caller.set_item(valor)
        caller.text = valor
        caller.current_item = valor
        if hasattr(self, "menu_dim") and self.menu_dim:
            self.menu_dim.dismiss()

    def abrir_menu_revest_junta(self, caller):
        juntas = ["1", "2", "3", "4", "5"]

        itens = [{
            "viewclass": "OneLineListItem",
            "text": j,
            "height": dp(48),
            "on_release": lambda x=j: self.definir_junta(caller, x),
        } for j in juntas]

        if hasattr(self, "menu_junta") and self.menu_junta:
            self.menu_junta.dismiss()

        self.menu_junta = MDDropdownMenu(
            caller=caller,
            items=itens,
            width_mult=3
        )
        self.menu_junta.open()

    def definir_junta(self, caller, valor):
        caller.set_item(valor)
        caller.text = valor
        caller.current_item = valor
        if hasattr(self, "menu_junta") and self.menu_junta:
            self.menu_junta.dismiss()

    def abrir_menu_margem(self, caller):
        opcoes = ["Sem margem", "5%", "10%", "15%"]

        itens = [{
            "viewclass": "OneLineListItem",
            "text": opcao,
            "height": dp(48),
            "on_release": lambda x=opcao: self.definir_margem(caller, x)
        } for opcao in opcoes]

        if hasattr(self, "menu_margem") and self.menu_margem:
            self.menu_margem.dismiss()

        self.menu_margem = MDDropdownMenu(
            caller=caller,
            items=itens,
            width_mult=4
        )
        self.menu_margem.open()


    def definir_margem(self, caller, valor):
        caller.set_item(valor)
        caller.text = valor
        caller.current_item = valor

        if hasattr(self, "menu_margem") and self.menu_margem:
            self.menu_margem.dismiss()


    def obter_percentual_margem(self, valor_margem):
        mapa = {
            "Sem margem": 0.0,
            "5%": 0.05,
            "10%": 0.10,
            "15%": 0.15,
        }
        return mapa.get(valor_margem, 0.0)

    def limpar_markup(self, texto):
        return (
            texto.replace("[b]", "")
                .replace("[/b]", "")
                .replace("[i]", "")
                .replace("[/i]", "")
                .strip()
        )

    def escolher_caminho_pdf(self):
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)

        nome_arquivo = f"resumo_obra_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

        caminho = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Arquivo PDF", "*.pdf")],
            initialfile=nome_arquivo,
            title="Salvar PDF como"
        )

        root.destroy()
        return caminho

    def proximo_campo(self, tela, aba, proximo_id):
        try:
            ids = getattr(self._tela_abas().ids, aba).ids
            campo = ids.get(proximo_id)
            if campo:
                campo.focus = True
        except Exception as e:
            print("ERRO AO MUDAR FOCO:", e)

    def abrir_ajuda_inicial(self):
        self.dialog = MDDialog(
            title="Como usar",
            text=(
                "• Toque em Iniciar para abrir os cálculos.\n\n"
                "• Toque em Histórico para visualizar os registros salvos."
            ),
            radius=[20, 20, 20, 20],
            buttons=[
                MDRaisedButton(
                    text="Fechar",
                    md_bg_color=(0.15, 0.30, 0.39, 1),
                    text_color=(1, 1, 1, 1),
                    on_release=lambda x: self.dialog.dismiss()
                )
            ],
        )
        self.dialog.open()

    def alternar_tema(self):
        if self.theme_cls.theme_style == "Light":
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"

        Clock.schedule_once(lambda dt: self.atualizar_tema_revestimento(), 0.1)

    def atualizar_tema_revestimento(self):
        try:
            tela = self.root.get_screen("abas")
            tab_revest = tela.ids.tab_revestimento

            card_piso = tab_revest.ids.card_piso
            card_azulejo = tab_revest.ids.card_azulejo

            self._aplicar_tema_card_revestimento(card_piso)
            self._aplicar_tema_card_revestimento(card_azulejo)
            self._atualizar_altura_revestimento(tab_revest)

        except Exception as e:
            print("ERRO AO ATUALIZAR TEMA DO REVESTIMENTO:", e)

    def atualizar_aba_atual(self, *args):
        try:
            tab = args[1]
            self.aba_atual = tab.title
        except Exception as e:
            print("ERRO AO ATUALIZAR ABA ATUAL:", e)

    def abrir_ajuda_abas(self):
        textos = {
            "Brocas": (
                "• Informe a quantidade total de brocas da obra.\n\n"
                "• Depois insira o diâmetro e a profundidade de cada broca em metros.\n\n"
                "• Selecione a proporção do concreto para calcular os materiais necessários."
            ),

            "Baldrame": (
                "• Some todo o comprimento da vala ou sapata da obra e insira o valor total.\n\n"
                "• Depois informe a largura e a altura em metros.\n\n"
                "• Selecione a proporção do concreto para calcular os materiais necessários."
            ),

            "Paredes": (
                "• Some as áreas de cada parede de todos os cômodos e insira o valor total em m².\n\n"
                "• Se houver portas e janelas, some essas áreas e informe no campo de espaço perdido.\n\n"
                "• Depois selecione o tipo de tijolo, a margem para perdas e a proporção da massa."
            ),

            "Reboco": (
                "• Some as áreas de todas as paredes que receberão reboco e informe o total em m².\n\n"
                "• Se houver portas e janelas, some essas áreas e informe como espaço perdido.\n\n"
                "• Depois informe a espessura do reboco em metros e selecione a proporção da massa."
            ),

            "Contrapiso": (
                "• Some as áreas de todos os cômodos que receberão contrapiso e informe o total em m².\n\n"
                "• Depois informe a espessura do contrapiso em metros.\n\n"
                "• Selecione a proporção do concreto para calcular os materiais necessários."
            ),

            "Revestimento": (
                "• Escolha se deseja calcular piso, azulejo ou ambos.\n\n"
                "• Some as áreas de todos os ambientes que receberão revestimento e informe o total em m².\n\n"
                "• Depois selecione a dimensão da peça e a largura da junta para calcular a quantidade de peças, argamassa e rejunte."
            ),

            "Orçamento": (
                "• Informe os preços unitários dos materiais utilizados na obra.\n\n"
                "• Esses valores serão usados para estimar o custo total no resumo final.\n\n"
                "• Preencha com atenção para obter um orçamento mais próximo do real."
            ),

            "Resumo": (
                "• Aqui você visualiza o resumo geral dos cálculos realizados nas abas anteriores.\n\n"
                "• Também é nesta aba que você pode salvar o resultado final em PDF."
            ),
        }

        titulo = f"Como usar: {self.aba_atual}"
        texto = textos.get(
            self.aba_atual,
            "Preencha os dados da aba atual e toque em calcular para ver o resultado."
        )

        self.dialog = MDDialog(
            title=titulo,
            text=texto,
            radius=[20, 20, 20, 20],
            buttons=[
                MDRaisedButton(
                    text="Fechar",
                    md_bg_color=(0.15, 0.30, 0.39, 1),
                    text_color=(1, 1, 1, 1),
                    on_release=lambda x: self.dialog.dismiss()
                )
            ],
        )
        self.dialog.open()

    def coletar_campos_obra(self):
        ids_brocas = self._ids_brocas()
        ids_baldrame = self._ids_baldrame()
        ids_paredes = self._ids_paredes()
        ids_reboco = self._ids_reboco()
        ids_contrapiso = self._ids_contrapiso()
        ids_revest = self._ids_revestimento()
        ids_orc = self._ids_orcamento()

        return {
            "brocas": {
                "qtd_brocas": ids_brocas.qtd_brocas.text,
                "diametro_broca": ids_brocas.diametro_broca.text,
                "profundidade_broca": ids_brocas.profundidade_broca.text,
                "proporcao": getattr(ids_brocas.proporcao_dropdown, "current_item", ids_brocas.proporcao_dropdown.text),
            },
            "baldrame": {
                "comprimento_baldrame": ids_baldrame.comprimento_baldrame.text,
                "largura_baldrame": ids_baldrame.largura_baldrame.text,
                "altura_baldrame": ids_baldrame.altura_baldrame.text,
                "proporcao": getattr(ids_baldrame.proporcao_concreto_baldrame, "current_item", ids_baldrame.proporcao_concreto_baldrame.text),
            },
            "paredes": {
                "area_parede": ids_paredes.area_parede.text,
                "espaco_perdido_parede": ids_paredes.espaco_perdido_parede.text,
                "tijolo": getattr(ids_paredes.tijolo_dropdown, "current_item", ids_paredes.tijolo_dropdown.text),
                "margem": getattr(ids_paredes.margem_paredes_dropdown, "current_item", ids_paredes.margem_paredes_dropdown.text),
                "massa": getattr(ids_paredes.massa_dropdown, "current_item", ids_paredes.massa_dropdown.text),
            },
            "reboco": {
                "area_reboco": ids_reboco.area_reboco.text,
                "espaco_perdido_reboco": ids_reboco.espaco_perdido_reboco.text,
                "espessura_reboco": ids_reboco.espessura_reboco.text,
                "massa": getattr(ids_reboco.massa_reboco_dropdown, "current_item", ids_reboco.massa_reboco_dropdown.text),
            },
            "contrapiso": {
                "area_contrapiso": ids_contrapiso.area_contrapiso.text,
                "espessura_contrapiso": ids_contrapiso.espessura_contrapiso.text,
                "proporcao": getattr(ids_contrapiso.proporcao_contrapiso_dropdown, "current_item", ids_contrapiso.proporcao_contrapiso_dropdown.text),
            },
            "revestimento": {
                "tipo": (
                    "piso" if ids_revest.cb_piso.active else
                    "azulejo" if ids_revest.cb_azulejo.active else
                    "ambos" if ids_revest.cb_ambos.active else ""
                ),
                "area_piso": ids_revest.area_piso.text,
                "tamanho_piso": getattr(ids_revest.tamanho_piso_drop, "current_item", ids_revest.tamanho_piso_drop.text),
                "junta_piso": getattr(ids_revest.junta_piso_drop, "current_item", ids_revest.junta_piso_drop.text),
                "area_azulejo": ids_revest.area_azulejo.text,
                "tamanho_azulejo": getattr(ids_revest.tamanho_az_drop, "current_item", ids_revest.tamanho_az_drop.text),
                "junta_azulejo": getattr(ids_revest.junta_az_drop, "current_item", ids_revest.junta_az_drop.text),
            },
            "orcamento": {
                "tipo_tijolo": getattr(ids_orc.tipo_tijolo_orcamento, "current_item", ids_orc.tipo_tijolo_orcamento.text),
                "preco_tijolo": ids_orc.preco_tijolo.text,
                "preco_cimento": ids_orc.preco_cimento.text,
                "preco_cal": ids_orc.preco_cal.text,
                "preco_areia": ids_orc.preco_areia.text,
                "preco_pedra": ids_orc.preco_pedra.text,
                "preco_argamassa": ids_orc.preco_argamassa.text,
                "preco_rejunte": ids_orc.preco_rejunte.text,
            }
        }

    def preencher_campos_obra(self, obra):
        campos = obra.get("campos", {})

        brocas = campos.get("brocas", {})
        ids = self._ids_brocas()
        ids.qtd_brocas.text = brocas.get("qtd_brocas", "")
        ids.diametro_broca.text = brocas.get("diametro_broca", "")
        ids.profundidade_broca.text = brocas.get("profundidade_broca", "")
        if brocas.get("proporcao"):
            ids.proporcao_dropdown.text = brocas["proporcao"]
            ids.proporcao_dropdown.current_item = brocas["proporcao"]

        baldrame = campos.get("baldrame", {})
        ids = self._ids_baldrame()
        ids.comprimento_baldrame.text = baldrame.get("comprimento_baldrame", "")
        ids.largura_baldrame.text = baldrame.get("largura_baldrame", "")
        ids.altura_baldrame.text = baldrame.get("altura_baldrame", "")
        if baldrame.get("proporcao"):
            ids.proporcao_concreto_baldrame.text = baldrame["proporcao"]
            ids.proporcao_concreto_baldrame.current_item = baldrame["proporcao"]

        paredes = campos.get("paredes", {})
        ids = self._ids_paredes()
        ids.area_parede.text = paredes.get("area_parede", "")
        ids.espaco_perdido_parede.text = paredes.get("espaco_perdido_parede", "")
        for key, widget_id in [
            ("tijolo", "tijolo_dropdown"),
            ("margem", "margem_paredes_dropdown"),
            ("massa", "massa_dropdown"),
        ]:
            valor = paredes.get(key, "")
            if valor:
                widget = getattr(ids, widget_id)
                widget.text = valor
                widget.current_item = valor

        reboco = campos.get("reboco", {})
        ids = self._ids_reboco()
        ids.area_reboco.text = reboco.get("area_reboco", "")
        ids.espaco_perdido_reboco.text = reboco.get("espaco_perdido_reboco", "")
        ids.espessura_reboco.text = reboco.get("espessura_reboco", "")
        if reboco.get("massa"):
            ids.massa_reboco_dropdown.text = reboco["massa"]
            ids.massa_reboco_dropdown.current_item = reboco["massa"]

        contrapiso = campos.get("contrapiso", {})
        ids = self._ids_contrapiso()
        ids.area_contrapiso.text = contrapiso.get("area_contrapiso", "")
        ids.espessura_contrapiso.text = contrapiso.get("espessura_contrapiso", "")
        if contrapiso.get("proporcao"):
            ids.proporcao_contrapiso_dropdown.text = contrapiso["proporcao"]
            ids.proporcao_contrapiso_dropdown.current_item = contrapiso["proporcao"]

        revest = campos.get("revestimento", {})
        ids = self._ids_revestimento()
        tipo = revest.get("tipo", "")
        ids.cb_piso.active = tipo == "piso"
        ids.cb_azulejo.active = tipo == "azulejo"
        ids.cb_ambos.active = tipo == "ambos"
        ids.area_piso.text = revest.get("area_piso", "")
        ids.area_azulejo.text = revest.get("area_azulejo", "")

        for key, widget_id in [
            ("tamanho_piso", "tamanho_piso_drop"),
            ("junta_piso", "junta_piso_drop"),
            ("tamanho_azulejo", "tamanho_az_drop"),
            ("junta_azulejo", "junta_az_drop"),
        ]:
            valor = revest.get(key, "")
            if valor:
                widget = getattr(ids, widget_id)
                widget.text = valor
                widget.current_item = valor

        orc = campos.get("orcamento", {})
        ids = self._ids_orcamento()
        if orc.get("tipo_tijolo"):
            ids.tipo_tijolo_orcamento.text = orc["tipo_tijolo"]
            ids.tipo_tijolo_orcamento.current_item = orc["tipo_tijolo"]
        ids.preco_tijolo.text = orc.get("preco_tijolo", "")
        ids.preco_cimento.text = orc.get("preco_cimento", "")
        ids.preco_cal.text = orc.get("preco_cal", "")
        ids.preco_areia.text = orc.get("preco_areia", "")
        ids.preco_pedra.text = orc.get("preco_pedra", "")
        ids.preco_argamassa.text = orc.get("preco_argamassa", "")
        ids.preco_rejunte.text = orc.get("preco_rejunte", "")

    def salvar_obra_app(self):
        try:
            resumo = self.texto_resumo.strip()

            if not resumo:
                self.mostrar_snackbar("⚠️ Gere o resumo antes de salvar a obra.")
                return

            nome_obra = f"Obra {len(self.historico_obras) + 1}"
            data_salva = self.obter_data_hora_atual()

            dados_obra = {
                "nome": nome_obra,
                "data": data_salva,
                "resumo": resumo,
                "campos": self.coletar_campos_obra(),
            }

            self.historico_obras.append(dados_obra)
            self.salvar_historico_json()
            self.atualizar_historico()
            self.mostrar_snackbar("✅ Obra salva no histórico com sucesso!")

        except Exception as e:
            print("ERRO AO SALVAR OBRA:", e)
            self.mostrar_snackbar("⚠️ Erro ao salvar a obra.")

    def divider_vertical(self):
        d = MDWidget(
            size_hint_x=None,
            width=dp(1),
            size_hint_y=None,
            height=dp(16),
            pos_hint={"center_y": 0.5}
        )

        with d.canvas.before:

            if self.theme_cls.theme_style == "Light":
                Color(0, 0, 0, 0.10)
            else:
                Color(1, 1, 1, 0.10)

            rect = Rectangle(pos=d.pos, size=d.size)

        def update_rect(*args):
            rect.pos = d.pos
            rect.size = d.size

        d.bind(pos=update_rect, size=update_rect)
        return d

    def atualizar_historico(self, obras_filtradas=None):

        container = self.root.get_screen("historico").ids.container_historico
        container.clear_widgets()

        lista_base = obras_filtradas if obras_filtradas is not None else self.historico_obras

        if self.theme_cls.theme_style == "Light":
            bg_card = (1, 1, 1, 1)
            cor_nome = (0.1, 0.1, 0.1, 1)
            cor_data = (0.42, 0.45, 0.5, 1)
            cor_preview = (0.25, 0.28, 0.32, 1)
            cor_div = (0.88, 0.9, 0.92, 1)
            cor_icon = (0.2, 0.25, 0.3, 1)
            cor_share = (0.25, 0.25, 0.25, 1)
        else:
            bg_card = (0.12, 0.14, 0.17, 1)
            cor_nome = (1, 1, 1, 1)
            cor_data = (0.72, 0.76, 0.82, 1)
            cor_preview = (0.88, 0.90, 0.94, 1)
            cor_div = (0.22, 0.25, 0.29, 1)
            cor_icon = (0.75, 0.82, 0.9, 1)
            cor_share = (1, 1, 1, 1)

        if not lista_base:
            card_vazio = MDCard(
                orientation="vertical",
                padding=dp(18),
                size_hint_y=None,
                height=dp(90),
                radius=[16, 16, 16, 16],
                elevation=2,
                md_bg_color=bg_card,
            )
            card_vazio.add_widget(
                MDLabel(
                    text="Nenhuma obra salva ainda.",
                    halign="center",
                    theme_text_color="Secondary",
                )
            )
            container.add_widget(card_vazio)
            return

        lista_exibicao = list(reversed(lista_base))

        for obra in lista_exibicao:
            indice_real = next((i for i, o in enumerate(self.historico_obras) if o == obra), None)
            if indice_real is None:
                continue

            card = MDCard(
                orientation="vertical",
                padding=dp(16),
                spacing=dp(10),
                size_hint_y=None,
                height=dp(230),
                radius=[18, 18, 18, 18],
                elevation=4,
                md_bg_color=bg_card,
            )

            topo = MDBoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height=dp(30),
                spacing=dp(6),
                padding=[0, dp(2), 0, 0]
            )

            icone_obra = MDIcon(
                icon="home-outline",
                theme_text_color="Custom",
                text_color=(0,0,0,1) if self.theme_cls.theme_style == "Light" else (1,1,1,1),
                font_size="20sp",
                size_hint=(None, None),
                size=(dp(20), dp(20)),
                pos_hint={"center_y": 0.5},
            )

            nome = MDLabel(
                text=obra.get("nome", "Sem nome"),
                bold=True,
                theme_text_color="Custom",
                text_color=cor_nome,
                font_size="19sp",
                valign="middle",
            )

            topo.add_widget(icone_obra)
            topo.add_widget(nome)

            linha_data = MDBoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height=dp(24),
                spacing=dp(6),
                padding=(0, 0, 0, 0),
            )

            icone_data = MDIcon(
                icon="calendar-outline",
                theme_text_color="Custom",
                text_color=(0,0,0,1) if self.theme_cls.theme_style == "Light" else (1,1,1,1),
                font_size="18sp",
                size_hint=(None, None),
                size=(dp(18), dp(18)),
                pos_hint={"center_y": 0.5},
            )

            data_label = MDLabel(
                text=f"Salva em: {obra.get('data', '')}",
                theme_text_color="Custom",
                text_color=cor_data,
                font_size="14sp",
                valign="middle",
            )

            linha_data.add_widget(icone_data)
            linha_data.add_widget(data_label)

            # --- PRIMEIRA LINHA ---
            div_1 = MDBoxLayout(
                size_hint_y=None,
                height=dp(0.8),
                md_bg_color=cor_div
            )

            linha1_wrap = MDBoxLayout(
                size_hint_y=None,
                height=dp(1),
                padding=(dp(6), 0, dp(6), 0),
            )
            linha1_wrap.add_widget(div_1)

            resumo_box = MDBoxLayout(
                orientation="vertical",
                size_hint_y=None,
                height=dp(56),
                spacing=dp(4),
                padding=(dp(4), 0, 0, 0),
            )

            tipo_texto, preview = self.gerar_preview_obra(obra.get("resumo", ""))

            linha_principal = "-"

            if preview:
                primeira = self.limpar_markup(preview[0]).strip()

                if ":" in primeira:
                    titulo, valor = primeira.split(":", 1)
                    linha_principal = f"[b]{titulo.strip()}:[/b] {valor.strip()}"
                else:
                    linha_principal = primeira

            tipo_label = MDLabel(
                text=tipo_texto,
                font_size="15sp",
                bold=True,
                theme_text_color="Custom",
                text_color=(0, 0, 0, 1) if self.theme_cls.theme_style == "Light" else (1, 1, 1, 1),
                size_hint_y=None,
                height=dp(20),
            )

            volume_label = MDLabel(
                text=linha_principal,
                markup=True,
                theme_text_color="Custom",
                text_color=cor_preview,
                font_size="14sp",
                size_hint_y=None,
                height=dp(22),
                shorten=True,
                shorten_from="right",
            )

            resumo_box.add_widget(tipo_label)
            resumo_box.add_widget(volume_label)

            # --- SEGUNDA LINHA ---
            div_2 = MDBoxLayout(
                size_hint_y=None,
                height=dp(0.8),
                md_bg_color=cor_div
            )

            linha2_wrap = MDBoxLayout(
                size_hint_y=None,
                height=dp(1),
                padding=(dp(6), 0, dp(6), 0),
            )
            linha2_wrap.add_widget(div_2)

            acoes = MDBoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height=dp(20),
                spacing=dp(9),
                padding=[0, 0, 0, 0],
            )

            btn_ver = MDIconButton(
                icon="eye-outline",
                theme_text_color="Custom",
                icon_size="15sp",
                pos_hint={"center_y": 0.5},
                text_color=cor_icon,
                on_release=lambda x, i=indice_real: self.abrir_obra(i),
            )

            btn_renomear = MDIconButton(
                icon="pencil",
                theme_text_color="Custom",
                icon_size="15sp",
                pos_hint={"center_y": 0.5},
                text_color=cor_icon,
                on_release=lambda x, i=indice_real: self.renomear_obra(i),
            )

            btn_editar = MDIconButton(
                icon="file-edit-outline",
                theme_text_color="Custom",
                icon_size="15sp",
                pos_hint={"center_y": 0.5},
                text_color=cor_icon,
                on_release=lambda x, i=indice_real: self.editar_obra(i),
            )

            btn_duplicar = MDIconButton(
                icon="content-copy",
                theme_text_color="Custom",
                icon_size="15sp",
                pos_hint={"center_y": 0.5},
                text_color=cor_icon,
                on_release=lambda x, i=indice_real: self.duplicar_obra(i),
            )

            btn_excluir = MDIconButton(
                icon="delete-outline",
                theme_text_color="Custom",
                icon_size="15sp",
                pos_hint={"center_y": 0.5},
                text_color=(0.85, 0.2, 0.2, 1),
                on_release=lambda x, i=indice_real: self.excluir_obra(i),
            )

            btn_compartilhar = MDIconButton(
                icon="share-variant",
                theme_text_color="Custom",
                icon_size="15sp",
                pos_hint={"center_y": 0.5},
                text_color=cor_share,
                on_release=lambda x, i=indice_real: self.compartilhar_obra(i),
            )

            acoes.add_widget(btn_ver)
            acoes.add_widget(self.divider_vertical())
            acoes.add_widget(btn_renomear)
            acoes.add_widget(self.divider_vertical())
            acoes.add_widget(btn_editar)
            acoes.add_widget(self.divider_vertical())
            acoes.add_widget(btn_duplicar)
            acoes.add_widget(self.divider_vertical())
            acoes.add_widget(btn_excluir)
            acoes.add_widget(self.divider_vertical())
            acoes.add_widget(btn_compartilhar)

            card.add_widget(topo)
            card.add_widget(linha_data)
            card.add_widget(linha1_wrap)
            card.add_widget(resumo_box)
            card.add_widget(MDWidget(size_hint_y=None, height=dp(1)))
            linha = MDWidget(
                size_hint=(1, None),
                height=dp(1)
            )

            with linha.canvas.before:
                from kivy.graphics import Color, Rectangle

                if self.theme_cls.theme_style == "Light":
                    Color(0, 0, 0, 0.08)
                else:
                    Color(1, 1, 1, 0.08)

                rect_linha = Rectangle(pos=linha.pos, size=linha.size)

            def update_linha(*args):
                rect_linha.pos = linha.pos
                rect_linha.size = linha.size

            linha.bind(pos=update_linha, size=update_linha)

            card.add_widget(linha)
            card.add_widget(MDWidget(size_hint_y=None, height=dp(1)))
            card.add_widget(acoes)

            container.add_widget(card)

    def abrir_dialog_salvar_obra(self):
        self.campo_nome_obra = MDTextField(
            hint_text="Digite o nome da obra",
            helper_text="Ex: Casa da Maria",
            helper_text_mode="on_focus",
            multiline=False,
            size_hint_x=1,
        )

        self.dialog_salvar_obra = MDDialog(
            title="Salvar obra",
            type="custom",
            content_cls=self.campo_nome_obra,
            radius=[20, 20, 20, 20],
            buttons=[
                MDFlatButton(
                    text="Cancelar",
                    on_release=lambda x: self.dialog_salvar_obra.dismiss()
                ),
                MDRaisedButton(
                    text="Salvar",
                    md_bg_color=(0.15, 0.30, 0.39, 1),
                    text_color=(1, 1, 1, 1),
                    on_release=lambda x: self.confirmar_salvar_obra()
                ),
            ],
        )
        self.dialog_salvar_obra.open()

    def confirmar_salvar_obra(self):
        try:
            resumo = self.texto_resumo.strip()

            if not resumo:
                self.mostrar_snackbar("⚠️ Gere o resumo antes de salvar a obra.")
                return

            nome_digitado = self.campo_nome_obra.text.strip()

            if not nome_digitado:
                nome_digitado = f"Obra {len(self.historico_obras) + 1}"

            data_salva = self.obter_data_hora_atual()

            dados_obra = {
                "nome": nome_digitado,
                "data": data_salva,
                "resumo": resumo,
                "campos": self.coletar_campos_obra(),
            }

            self.historico_obras.append(dados_obra)
            self.salvar_historico_json()

            self.root.current = "historico"
            self.atualizar_historico()
            self.mostrar_feedback_obra_salva()

            self.dialog_salvar_obra.dismiss()
            self.mostrar_snackbar("✅ Obra salva com sucesso!")

        except Exception as e:
            print("ERRO AO CONFIRMAR SALVAMENTO:", e)
            self.mostrar_snackbar("⚠️ Erro ao salvar a obra.")

    def salvar_historico_json(self):
        try:
            with open(self.arquivo_historico, "w", encoding="utf-8") as f:
                json.dump(self.historico_obras, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print("ERRO AO SALVAR JSON:", e)

    def carregar_historico_json(self):
        try:
            if os.path.exists(self.arquivo_historico):
                with open(self.arquivo_historico, "r", encoding="utf-8") as f:
                    self.historico_obras = json.load(f)
            else:
                self.historico_obras = []

        except Exception as e:
            print("ERRO AO CARREGAR JSON:", e)
            self.historico_obras = []

    def abrir_obra(self, index):
        obra = self.historico_obras[index]
        self.texto_resumo = obra["resumo"]

        ids = self._ids_resumo()
        self.mostrar_resultado_label(ids.resultado_resumo, obra["resumo"])

        self.root.current = "abas"
        Clock.schedule_once(lambda dt: self._tabs().switch_tab("Resumo"), 0.1)

    def editar_obra(self, index):
        obra = self.historico_obras[index]
        self.root.current = "abas"

        def abrir_e_preencher(dt):
            try:
                self.preencher_campos_obra(obra)
                self._tabs().switch_tab("Brocas")
            except Exception as e:
                print("ERRO AO EDITAR OBRA:", e)
                self.mostrar_snackbar("⚠️ Erro ao abrir a obra para edição.")

        Clock.schedule_once(abrir_e_preencher, 0.3)

    def excluir_obra(self, index):
        self.dialog_confirmar_exclusao = MDDialog(
            title="Excluir obra",
            text="Deseja mesmo excluir esta obra?",
            buttons=[
                MDFlatButton(
                    text="Cancelar",
                    theme_text_color="Custom",
                    text_color=(0.25, 0.25, 0.25, 1) if self.theme_cls.theme_style == "Light" else (1, 1, 1, 1),
                    on_release=lambda x: self.dialog_confirmar_exclusao.dismiss()
                ),
                MDRaisedButton(
                    text="Excluir",
                    md_bg_color=(0.9, 0.2, 0.2, 1),
                    text_color=(1, 1, 1, 1),
                    on_release=lambda x, i=index: self.confirmar_exclusao_obra(i)
                ),
            ],
        )
        self.dialog_confirmar_exclusao.open()


    def confirmar_exclusao_obra(self, index):
        if hasattr(self, "dialog_confirmar_exclusao") and self.dialog_confirmar_exclusao:
            self.dialog_confirmar_exclusao.dismiss()

        if index < 0 or index >= len(self.historico_obras):
            self.mostrar_snackbar("⚠️ Não foi possível excluir a obra.")
            return

        del self.historico_obras[index]
        self.salvar_historico_json()
        self.atualizar_historico()

        self.mostrar_snackbar_desfazer()

    def desfazer_exclusao_obra(self, *args):
        if not hasattr(self, "ultima_obra_excluida") or self.ultima_obra_excluida is None:
            self.mostrar_snackbar("⚠️ Nada para desfazer.")
            return

        indice = getattr(self, "ultimo_indice_excluido", len(self.historico_obras))

        if indice < 0 or indice > len(self.historico_obras):
            indice = len(self.historico_obras)

        self.historico_obras.insert(indice, self.ultima_obra_excluida)
        self.salvar_historico_json()
        self.atualizar_historico()

        self.ultima_obra_excluida = None
        self.ultimo_indice_excluido = None

        self.mostrar_snackbar("↩️ Exclusão desfeita com sucesso!")

    def desfazer_exclusao(self):
        if self.ultima_obra_excluida is not None:
            self.historico_obras.insert(
                self.indice_ultima_exclusao,
                self.ultima_obra_excluida
            )

            self.salvar_historico_json()
            self.atualizar_historico()

            self.mostrar_snackbar("↩️ Exclusão desfeita")

            # limpa
            self.ultima_obra_excluida = None
            self.indice_ultima_exclusao = None

    def duplicar_obra(self, index):

        obra = self.historico_obras[index]
        nova = copy.deepcopy(obra)
        nova["nome"] = obra["nome"] + " (cópia)"
        nova["data"] = self.obter_data_hora_atual()

        self.historico_obras.append(nova)
        self.salvar_historico_json()
        self.atualizar_historico()

        self.mostrar_snackbar("📋 Obra duplicada")

    def renomear_obra(self, index):
        self.index_renomear = index

        self.campo_nome = MDTextField(
            text=self.historico_obras[index]["nome"]
        )

        self.dialog = MDDialog(
            title="Renomear obra",
            type="custom",
            content_cls=self.campo_nome,
            buttons=[
                MDFlatButton(
                    text="Cancelar",
                    on_release=lambda x: self.dialog.dismiss()
                ),
                MDRaisedButton(
                    text="Salvar",
                    on_release=lambda x: self.confirmar_renomear()
                ),
            ],
        )
        self.dialog.open()

    def confirmar_renomear(self):
        novo_nome = self.campo_nome.text.strip()

        if novo_nome:
            self.historico_obras[self.index_renomear]["nome"] = novo_nome
            self.salvar_historico_json()
            self.atualizar_historico()
            self.mostrar_snackbar("✏️ Nome atualizado")

        self.dialog.dismiss()
        self.mostrar_snackbar("✏️ Nome da obra atualizado")

    def filtrar_obras(self, texto):
        texto = texto.strip().lower()

        if not texto:
            self.atualizar_historico()
            return

        filtradas = []
        for obra in self.historico_obras:
            if (
                texto in obra.get("nome", "").lower()
                or texto in obra.get("data", "").lower()
                or texto in obra.get("resumo", "").lower()
            ):
                filtradas.append(obra)

        self.atualizar_historico(filtradas)

    def obter_data_hora_atual(self):
        return datetime.now().strftime("%d/%m/%Y %H:%M")

    def compartilhar_obra(self, index):
        try:
            obra = self.historico_obras[index]

            nome = str(obra.get("nome", "Obra"))
            data = str(obra.get("data", "Sem data"))
            resumo = str(obra.get("resumo_obra") or obra.get("resumo") or "")
            precos = obra.get("precos", {}) or {}

            # =========================
            # CORES
            # =========================
            COR_PRIMARIA = colors.HexColor("#16324F")
            COR_PRIMARIA_2 = colors.HexColor("#214B72")
            COR_SECUNDARIA = colors.HexColor("#F5F7FA")
            COR_DESTAQUE = colors.HexColor("#2A5673")
            COR_BOX_TOTAL = colors.HexColor("#EDF4FB")
            COR_BOX_BORDA = colors.HexColor("#D4DAE2")
            COR_TEXTO = colors.HexColor("#1F2937")
            COR_TEXTO_SUAVE = colors.HexColor("#6B7280")
            COR_BORDA = colors.HexColor("#D4DAE2")
            COR_BRANCO = colors.white
            COR_SUBDESTAQUE = colors.HexColor("#DCEAF8")
            COR_BOX_INFO = colors.HexColor("#EEF1F4")

            # =========================
            # FUNÇÕES AUXILIARES
            # =========================
            def limpar(txt):
                txt = str(txt)
                txt = re.sub(r"\[/?[^\]]+\]", "", txt)
                txt = re.sub(
                    r"[^\w\s\-\:\.\,\/\(\)%R\$áàâãéêíóôõúçÁÀÂÃÉÊÍÓÔÕÚÇªº]",
                    "",
                    txt
                )
                return txt.strip()

            def nome_seguro(txt):
                txt = re.sub(r'[\\/*?:"<>|]', "", str(txt))
                return txt.replace(" ", "_").strip() or "obra"

            def formatar_moeda(valor):
                try:
                    valor = float(valor)
                    texto = f"R$ {valor:,.2f}"
                    return texto.replace(",", "X").replace(".", ",").replace("X", ".")
                except Exception:
                    return str(valor)

            def extrair_numero_moeda(texto):
                if not texto:
                    return 0.0
                t = str(texto).replace("R$", "").strip()
                t = t.replace(".", "").replace(",", ".")
                try:
                    return float(t)
                except Exception:
                    return 0.0

            def eh_titulo_etapa(txt):
                t = limpar(txt).strip().upper().rstrip(":")
                titulos_validos = {
                    "BROCAS",
                    "BALDRAME",
                    "PAREDES",
                    "REBOCO",
                    "CONTRAPISO",
                    "REVESTIMENTO",
                    "REVESTIMENTOS",
                    "PISO",
                    "AZULEJO",
                    "AZULEJOS",
                    "ORÇAMENTO",
                    "ORCAMENTO",
                    "RESUMO",
                }
                return t in titulos_validos

            def criar_linha_info(label, valor, largura_total=520):
                tabela = Table(
                    [[label, valor]],
                    colWidths=[125, largura_total - 125],
                    hAlign="LEFT",
                )
                tabela.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, -1), COR_BOX_INFO),
                    ("TEXTCOLOR", (0, 0), (-1, -1), COR_TEXTO),
                    ("FONTNAME", (0, 0), (0, 0), "Helvetica-Bold"),
                    ("FONTNAME", (1, 0), (1, 0), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 10.8),
                    ("BOX", (0, 0), (-1, -1), 0.6, COR_BORDA),
                    ("INNERGRID", (0, 0), (-1, -1), 0.6, COR_BORDA),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 12),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                    ("TOPPADDING", (0, 0), (-1, -1), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ]))
                return tabela

            def criar_tabela(dados, col_widths, alinhar_segunda_coluna_direita=False):
                tabela = Table(
                    dados,
                    colWidths=col_widths,
                    hAlign="LEFT",
                    repeatRows=1
                )

                estilo = [
                    ("BOX", (0, 0), (-1, -1), 0.6, COR_BORDA),
                    ("INNERGRID", (0, 0), (-1, -1), 0.25, COR_BORDA),
                    ("BACKGROUND", (0, 0), (-1, 0), COR_PRIMARIA),
                    ("TEXTCOLOR", (0, 0), (-1, 0), COR_BRANCO),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 9.8),
                    ("TEXTCOLOR", (0, 1), (-1, -1), COR_TEXTO),
                    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, COR_SECUNDARIA]),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 8),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]

                if alinhar_segunda_coluna_direita:
                    estilo += [
                        ("ALIGN", (1, 1), (1, -1), "RIGHT"),
                        ("ALIGN", (1, 0), (1, 0), "CENTER"),
                    ]

                tabela.setStyle(TableStyle(estilo))
                return tabela

            def criar_box_total(total_formatado, largura_total=520):
                tabela = Table(
                    [[
                        Paragraph("Total geral", estilo_box_titulo),
                        Paragraph(total_formatado, estilo_box_valor)
                    ]],
                    colWidths=[220, largura_total - 220],
                    hAlign="LEFT",
                )
                tabela.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, -1), COR_BOX_TOTAL),
                    ("BOX", (0, 0), (-1, -1), 0.8, COR_BOX_BORDA),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 12),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ]))
                return tabela

            def desenhar_rodape(canvas, doc):
                canvas.saveState()
                largura, _ = A4

                canvas.setStrokeColor(COR_BORDA)
                canvas.setLineWidth(0.5)
                canvas.line(doc.leftMargin, 14 * mm, largura - doc.rightMargin, 14 * mm)

                canvas.setFont("Helvetica", 8.5)
                canvas.setFillColor(COR_TEXTO_SUAVE)
                canvas.drawRightString(
                    largura - doc.rightMargin,
                    9 * mm,
                    f"Página {doc.page}"
                )
                canvas.restoreState()

            def parsear_resumo(texto):
                linhas = [limpar(l) for l in texto.splitlines()]
                linhas = [l for l in linhas if l and set(l) != {"-"}]

                blocos = []
                custos = []
                secao_atual = None
                linhas_secao = []

                ignorar = {
                    "RESUMO DA OBRA - BUILDCALC",
                    "CUSTOS POR ETAPA",
                    "TOTAL GERAL DA OBRA",
                    "ORAMENTO E CUSTOS POR ETAPA",
                    "ORÇAMENTO E CUSTOS POR ETAPA",
                    "RESUMO FINANCEIRO POR ETAPA",
                    "RELATÓRIO GERADO AUTOMATICAMENTE PELO SISTEMA BUILDCALC",
                    "RELATORIO GERADO AUTOMATICAMENTE PELO SISTEMA BUILDCALC",
                    "GERADO PELO BUILDCALC",
                }

                def salvar_secao():
                    nonlocal secao_atual, linhas_secao
                    if secao_atual and linhas_secao:
                        blocos.append({
                            "titulo": secao_atual,
                            "linhas": linhas_secao[:]
                        })

                for linha in linhas:
                    if linha.upper() in ignorar:
                        continue

                    if "R$" in linha:
                        m = re.search(r"^(.*?)(R\$\s*[\d\.\,]+)", linha)
                        if m:
                            nome_etapa = limpar(m.group(1)).strip(" .-:")
                            valor = m.group(2).strip()
                            if nome_etapa:
                                custos.append([nome_etapa.title(), valor])
                        continue

                    if eh_titulo_etapa(linha):
                        salvar_secao()
                        secao_atual = linha.rstrip(":").title()
                        linhas_secao = []
                        continue

                    if secao_atual:
                        linhas_secao.append(linha)

                salvar_secao()
                return blocos, custos

            def extrair_linhas_aba(linhas):
                saida = []

                for linha in linhas:
                    txt = limpar(linha)
                    if not txt:
                        continue

                    if txt.lower() in {"campo valor"}:
                        continue

                    if txt.startswith("-"):
                        txt = "• " + txt[1:].strip()

                    if len(saida) < 9:
                        saida.append(txt)

                return saida[:9]

            # =========================
            # ARQUIVO PDF
            # =========================
            caminho = os.path.join(tempfile.gettempdir(), f"{nome_seguro(nome)}.pdf")

            doc = SimpleDocTemplate(
                caminho,
                pagesize=A4,
                rightMargin=36,
                leftMargin=36,
                topMargin=38,
                bottomMargin=50,
            )

            styles = getSampleStyleSheet()

            estilo_marca = ParagraphStyle(
                name="Marca",
                parent=styles["Normal"],
                fontName="Helvetica-Bold",
                fontSize=10.5,
                leading=12,
                textColor=COR_PRIMARIA,
                alignment=TA_LEFT,
                spaceAfter=2,
            )

            estilo_submarca = ParagraphStyle(
                name="Submarca",
                parent=styles["Normal"],
                fontName="Helvetica",
                fontSize=8.8,
                leading=11,
                textColor=COR_TEXTO_SUAVE,
                alignment=TA_LEFT,
                spaceAfter=8,
            )

            estilo_titulo = ParagraphStyle(
                name="Titulo",
                parent=styles["Title"],
                fontName="Helvetica-Bold",
                fontSize=20,
                leading=24,
                textColor=COR_TEXTO,
                alignment=TA_CENTER,
                spaceAfter=4,
            )

            estilo_subtitulo = ParagraphStyle(
                name="Subtitulo",
                parent=styles["Normal"],
                fontName="Helvetica",
                fontSize=10,
                leading=13,
                textColor=COR_TEXTO_SUAVE,
                alignment=TA_CENTER,
                spaceAfter=12,
            )

            estilo_secao = ParagraphStyle(
                name="Secao",
                parent=styles["Heading2"],
                fontName="Helvetica-Bold",
                fontSize=17,
                leading=16,
                textColor=COR_DESTAQUE,
                spaceBefore=10,
                spaceAfter=7,
            )

            estilo_texto = ParagraphStyle(
                name="Texto",
                parent=styles["BodyText"],
                fontName="Helvetica",
                fontSize=10,
                leading=13.5,
                textColor=COR_TEXTO,
                spaceAfter=3,
            )

            estilo_label_aba = ParagraphStyle(
                name="LabelAba",
                parent=styles["BodyText"],
                fontName="Helvetica-Bold",
                fontSize=13,
                leading=13,
                textColor=COR_PRIMARIA,
                spaceAfter=2,
            )

            estilo_subdestaque = ParagraphStyle(
                name="Subdestaque",
                parent=styles["BodyText"],
                fontName="Helvetica-Bold",
                fontSize=10,
                leading=13,
                textColor=COR_PRIMARIA,
                backColor=COR_SUBDESTAQUE,
                borderPadding=(2, 4, 2, 4),
                spaceBefore=4,
                spaceAfter=4,
            )

            estilo_box_titulo = ParagraphStyle(
                name="BoxTitulo",
                parent=styles["Normal"],
                fontName="Helvetica-Bold",
                fontSize=10,
                leading=12,
                textColor=COR_DESTAQUE,
                alignment=TA_LEFT,
            )

            estilo_box_valor = ParagraphStyle(
                name="BoxValor",
                parent=styles["Normal"],
                fontName="Helvetica-Bold",
                fontSize=14,
                leading=16,
                textColor=COR_PRIMARIA,
                alignment=TA_RIGHT,
            )

            estilo_rodape_final = ParagraphStyle(
                name="RodapeFinal",
                parent=styles["Italic"],
                fontName="Helvetica-Oblique",
                fontSize=8.6,
                leading=11,
                textColor=COR_TEXTO_SUAVE,
                alignment=TA_CENTER,
            )

            elementos = []

            # =========================
            # CABEÇALHO
            # =========================
            elementos.append(Paragraph("BUILDCALC", estilo_marca))
            elementos.append(Paragraph("Relatório técnico de materiais e custos", estilo_submarca))
            elementos.append(Spacer(1, 4))

            elementos.append(Paragraph(nome, estilo_titulo))
            elementos.append(Paragraph(
                "Planejamento consolidado de materiais, quantitativos e custos da obra",
                estilo_subtitulo
            ))

            elementos.append(HRFlowable(
                width="100%",
                thickness=1,
                color=COR_PRIMARIA,
                spaceBefore=4,
                spaceAfter=12
            ))

            # Boxes do jeito que você pediu
            elementos.append(criar_linha_info("Obra", nome))
            elementos.append(Spacer(1, 6))
            elementos.append(criar_linha_info("Gerado em:", data))
            elementos.append(Spacer(1, 12))

            # =========================
            # CONTEÚDO
            # =========================
            blocos, custos = parsear_resumo(resumo)

            total_geral = sum(extrair_numero_moeda(valor) for _, valor in custos)
            if total_geral > 0:
                elementos.append(criar_box_total(formatar_moeda(total_geral)))
                elementos.append(Spacer(1, 12))

            # =========================
            # DADOS POR ABA
            # =========================
            if blocos:
                elementos.append(Paragraph("Dados inseridos por aba", estilo_secao))
                elementos.append(Spacer(1, 2))

                for bloco in blocos:
                    linhas_aba = extrair_linhas_aba(bloco["linhas"])
                    if not linhas_aba:
                        continue

                    elementos.append(Paragraph(bloco["titulo"], estilo_label_aba))

                    for item in linhas_aba:
                        item_limpo = limpar(item).lower().rstrip(":")

                        if item_limpo in {"materiais necessários", "materiais necessarios"}:
                            elementos.append(
                                Paragraph("Materiais necessários:", estilo_subdestaque)
                            )
                        else:
                            elementos.append(Paragraph(item, estilo_texto))

                    elementos.append(Spacer(1, 8))

            # =========================
            # RESUMO FINANCEIRO
            # =========================
            if custos:
                elementos.append(Spacer(1, 4))
                elementos.append(Paragraph("Resumo financeiro por etapa", estilo_secao))
                elementos.append(Spacer(1, 2))

                dados_custos = [["Etapa", "Custo"]]
                dados_custos.extend(custos)

                tabela_custos = criar_tabela(
                    dados=dados_custos,
                    col_widths=[320, 140],
                    alinhar_segunda_coluna_direita=True,
                )

                elementos.append(KeepTogether([tabela_custos]))
                elementos.append(Spacer(1, 12))

            # =========================
            # PREÇOS DOS MATERIAIS
            # =========================
            if precos:
                elementos.append(Paragraph("Tabela de preços dos materiais", estilo_secao))
                elementos.append(Spacer(1, 2))

                dados_precos = [["Material", "Valor"]]
                for chave, valor in precos.items():
                    nome_material = str(chave).replace("_", " ").title()
                    valor_material = (
                        formatar_moeda(valor)
                        if isinstance(valor, (int, float))
                        else f"R$ {valor}"
                    )
                    dados_precos.append([nome_material, valor_material])

                tabela_precos = criar_tabela(
                    dados=dados_precos,
                    col_widths=[320, 140],
                    alinhar_segunda_coluna_direita=True,
                )

                elementos.append(KeepTogether([tabela_precos]))
                elementos.append(Spacer(1, 12))

            # =========================
            # RODAPÉ FINAL DO CONTEÚDO
            # =========================
            elementos.append(Spacer(1, 6))
            elementos.append(HRFlowable(
                width="100%",
                thickness=0.6,
                color=COR_BORDA,
                spaceBefore=2,
                spaceAfter=8
            ))
            elementos.append(
                Paragraph(
                    "Relatório gerado automaticamente pelo sistema BuildCalc",
                    estilo_rodape_final
                )
            )

            # =========================
            # GERAR PDF
            # =========================
            doc.build(
                elementos,
                onFirstPage=desenhar_rodape,
                onLaterPages=desenhar_rodape
            )

            webbrowser.open(caminho)
            self.mostrar_snackbar("PDF profissional gerado com sucesso!")

        except Exception as e:
            print("Erro ao compartilhar:", e)
            self.mostrar_snackbar("Erro ao gerar PDF")

    def gerar_pdf_direto(self, caminho):
        pdf = SimpleDocTemplate(caminho, pagesize=A4)
        estilos = getSampleStyleSheet()

        estilo_titulo = ParagraphStyle(
            "Titulo",
            parent=estilos["Heading1"],
            alignment=1,
            fontSize=22,
            leading=26,
            spaceAfter=10,
            fontName="Helvetica-Bold",
        )

        estilo_info = ParagraphStyle(
            "Info",
            parent=estilos["BodyText"],
            alignment=1,
            fontSize=10,
            leading=12,
            spaceAfter=18,
            textColor=colors.grey,
        )

        estilo_texto = estilos["BodyText"]

        elementos = []

        data_pdf = self.obter_data_hora_atual()

        elementos.append(Paragraph("RESUMO DA OBRA - BuildCalc", estilo_titulo))
        elementos.append(Paragraph(f"Gerado em: {data_pdf}", estilo_info))
        elementos.append(Spacer(1, 10))

        for linha in self.texto_resumo.split("\n"):
            if linha.strip():
                elementos.append(Paragraph(linha, estilo_texto))

        pdf.build(elementos)

    def gerar_preview_obra(self, resumo):
        secoes = {
            "BROCAS",
            "BALDRAME",
            "PAREDES",
            "REBOCO",
            "CONTRAPISO",
            "REVESTIMENTO",
            "ORÇAMENTO",
            "RESUMO DA OBRA - BUILDCALC",
        }

        prefixos_ignorar = (
            "☑ ",
            "☒ ",
            "✓ ",
            "✔ ",
            "• ",
            "📋 ",
            "🕳️ ",
            "🧱 ",
            "🪵 ",
            "🧩 ",
            "📦 ",
            "💰 ",
        )

        linhas_validas = []
        tipo_texto = "RESUMO"

        for linha in resumo.splitlines():
            linha_limpa = self.limpar_markup(linha).strip()

            if not linha_limpa:
                continue

            linha_sem_prefixo = linha_limpa
            mudou = True
            while mudou:
                mudou = False
                for p in prefixos_ignorar:
                    if linha_sem_prefixo.startswith(p):
                        linha_sem_prefixo = linha_sem_prefixo[len(p):].strip()
                        mudou = True

            linha_upper = linha_limpa.upper()
            linha_sem_prefixo_upper = linha_sem_prefixo.upper()

            if linha_sem_prefixo_upper in secoes:
                if linha_sem_prefixo_upper != "RESUMO DA OBRA - BUILDCALC":
                    tipo_texto = linha_sem_prefixo_upper
                continue

            if "RESUMO DA OBRA - BUILDCALC" in linha_sem_prefixo_upper:
                continue

            if "MATERIAIS NECESSÁRIOS" in linha_sem_prefixo_upper:
                continue

            if set(linha_sem_prefixo) == {"-"}:
                continue

            linhas_validas.append(linha_sem_prefixo)

        return tipo_texto, linhas_validas[:2]

    def ir_para_resumo_ultima_obra(self):
        if not self.historico_obras:
            self.mostrar_snackbar("⚠️ Nenhuma obra salva ainda.")
            return

        self.abrir_obra(len(self.historico_obras) - 1)

    def mostrar_feedback_obra_salva(self):
        tela = self.root.get_screen("historico")
        card = tela.ids.card_feedback

        card.height = dp(82)
        card.opacity = 1
        card.disabled = False

    def _ajustar_card_revestimento(self, card):
        try:
            card.do_layout()
            Clock.schedule_once(lambda dt: setattr(card, "height", card.minimum_height), 0)
        except Exception as e:
            print("ERRO AO AJUSTAR CARD DE REVESTIMENTO:", e)

    def _aplicar_tema_card_revestimento(self, card):
        try:
            tema_dark = self.theme_cls.theme_style == "Dark"
            card.md_bg_color = (1, 1, 1, 1) if not tema_dark else (0.16, 0.18, 0.21, 1)
        except Exception as e:
            print("ERRO AO APLICAR TEMA NO CARD DE REVESTIMENTO:", e)

    def to_float(self, valor):
        if not valor:
            return 0
        return float(valor.replace(",", "."))

    def formatar(self, valor):
        return f"{valor:.2f}".replace(".", ",")

#------------------------------------------------------
#   BROCAS - Cálculo e limpeza dos campos
#------------------------------------------------------

    def calcular_brocas(self):
        print("CLICOU NO BOTÃO CALCULAR")

        try:
            ids = self._ids_brocas()

            qtd = int(ids.qtd_brocas.text) if ids.qtd_brocas.text else 0
            diametro = self.to_float(ids.diametro_broca.text)
            profundidade = self.to_float(ids.profundidade_broca.text)

            proporcao = getattr(ids.proporcao_dropdown, "current_item", ids.proporcao_dropdown.text).strip()

            if not proporcao or proporcao == "Selecione":
                self.mostrar_snackbar("⚠️ Selecione a proporção do concreto")
                return

            # guarda a proporção para usar no custo depois
            self.proporcao_brocas = proporcao

            # cálculo do volume total
            volume_total = qtd * pi * (diametro / 2) ** 2 * profundidade

            # traços do concreto
            proporcoes = {
                "1:3:3": {"cimento": 1, "areia": 3, "pedra": 3},
                "1:4:3": {"cimento": 1, "areia": 4, "pedra": 3},
                "1.5:5:5": {"cimento": 1.5, "areia": 5, "pedra": 5}
            }

            prop = proporcoes.get(proporcao)
            if not prop:
                self.mostrar_snackbar("⚠️ Proporção inválida")
                return
            total_partes = sum(prop.values())

            # divisão dos materiais
            vol_cimento = volume_total * (prop["cimento"] / total_partes)
            vol_areia = volume_total * (prop["areia"] / total_partes)
            vol_pedra = volume_total * (prop["pedra"] / total_partes)

            # cimento em kg -> sacos
            cimento_kg = vol_cimento * 2500
            sacos_cimento = ceil(cimento_kg / 50)

            # texto do resultado
            texto = (
                f"[b]Volume total das brocas:[/b] {self.formatar(volume_total)} m³\n\n"
                f"[b]Materiais necessários:[/b]\n"
                f"- Cimento: {sacos_cimento} saco(s) de 50kg\n"
                f"- Areia: {self.formatar(vol_areia)} m³\n"
                f"- Pedra: {self.formatar(vol_pedra)} m³\n"
            )

            ids.resultado_brocas.text = texto
            self.texto_brocas = texto

            print("RESULTADO CALCULADO:", texto)

            # atualiza o resumo geral
            self.gerar_resumo()

        except Exception as e:
            print("ERRO NO CALCULO:", e)
            self.mostrar_snackbar("⚠️ Verifique os valores informados")

    def limpar_brocas(self):
        ids = self._ids_brocas()
        ids.qtd_brocas.text = ""
        ids.diametro_broca.text = ""
        ids.profundidade_broca.text = ""
        ids.proporcao_dropdown.set_item("Selecione")
        ids.proporcao_dropdown.text = "Selecione"
        ids.proporcao_dropdown.current_item = "Selecione"
        self.mostrar_resultado_label(ids.resultado_brocas, "O resultado aparecerá aqui...")
        self.texto_brocas = ""
        self.proporcao_brocas = "Selecione"

#------------------------------------------------------
#   BALDRAME - Cálculo e limpeza dos campos
#------------------------------------------------------

    def calcular_baldrame(self):
        try:
            ids = self._ids_baldrame()

            comp = self.to_float(ids.comprimento_baldrame.text)
            larg = self.to_float(ids.largura_baldrame.text)
            alt = self.to_float(ids.altura_baldrame.text)

            proporcao = getattr(
                ids.proporcao_concreto_baldrame,
                "current_item",
                ids.proporcao_concreto_baldrame.text
            ).strip()

            if not proporcao or proporcao == "Selecione":
                self.mostrar_snackbar("⚠️ Selecione a proporção do concreto")
                return

            self.proporcao_baldrame = proporcao

            volume_total = comp * larg * alt

            proporcoes = {
                "1:3:3": {"cimento": 1, "areia": 3, "pedra": 3},
                "1:4:3": {"cimento": 1, "areia": 4, "pedra": 3},
                "1.5:5:5": {"cimento": 1.5, "areia": 5, "pedra": 5}
            }

            prop = proporcoes.get(proporcao)
            if not prop:
                self.mostrar_snackbar("⚠️ Proporção inválida")
                return
            total_partes = sum(prop.values())

            vol_cimento = volume_total * (prop["cimento"] / total_partes)
            vol_areia = volume_total * (prop["areia"] / total_partes)
            vol_pedra = volume_total * (prop["pedra"] / total_partes)

            cimento_kg = vol_cimento * 2500
            sacos_cimento = ceil(cimento_kg / 50)

            texto = (
                f"[b]Volume total do baldrame:[/b] {self.formatar(volume_total)} m³\n\n"
                f"[b]Materiais Necessários:[/b]\n"
                f"- Cimento: {sacos_cimento} saco(s) de 50kg\n"
                f"- Areia: {self.formatar(vol_areia)} m³\n"
                f"- Pedra: {self.formatar(vol_pedra)} m³\n"
            )

            ids.resultado_baldrame.text = texto
            self.texto_baldrame = texto
            self.gerar_resumo()

        except Exception as e:
            print("ERRO BALDRAME:", e)
            self.mostrar_snackbar("⚠️ Preencha todos os campos corretamente!")

    def limpar_baldrame(self):
        ids = self._ids_baldrame()

        ids.comprimento_baldrame.text = ""
        ids.largura_baldrame.text = ""
        ids.altura_baldrame.text = ""

        ids.proporcao_concreto_baldrame.set_item("Selecione")
        ids.proporcao_concreto_baldrame.text = "Selecione"
        ids.proporcao_concreto_baldrame.current_item = "Selecione"

        ids.resultado_baldrame.text = "O resultado aparecerá aqui..."
        self.texto_baldrame = ""
        self.proporcao_baldrame = "Selecione"

#------------------------------------------------------
#   PAREDES - Cálculo e limpeza dos campos
#------------------------------------------------------

    def calcular_paredes(self):
        print("\n===== DEBUG PAREDES =====")

        try:
            ids = self._ids_paredes()
            print("ids paredes:", ids)

            print("area raw =", ids.area_parede.text)
            print("espaco perdido raw =", ids.espaco_perdido_parede.text)
            print("tijolo raw =", ids.tijolo_dropdown.text)
            print("massa raw =", ids.massa_dropdown.text)
            print("margem raw =", ids.margem_paredes_dropdown.text)

            area_total = self.to_float(ids.area_parede.text)

            espaco_perdido_str = ids.espaco_perdido_parede.text.strip()
            espaco_perdido = self.to_float(espaco_perdido_str) if espaco_perdido_str else 0.0

            tipo_tijolo = ids.tijolo_dropdown.text.strip()
            tipo_massa = ids.massa_dropdown.text.strip()
            margem_txt = ids.margem_paredes_dropdown.text.strip()

            print("tipo_tijolo =", tipo_tijolo)
            print("tipo_massa =", tipo_massa)
            print("margem_txt =", margem_txt)

            margem = self.obter_percentual_margem(margem_txt)

            area_liquida = area_total - espaco_perdido

            print("area_total =", area_total)
            print("espaco_perdido =", espaco_perdido)
            print("area_liquida =", area_liquida)

            if area_liquida <= 0:
                self.mostrar_snackbar("⚠️ O espaço perdido não pode ser maior que a área da parede")
                print("DEBUG: área líquida inválida")
                return

            dados_tijolo = self.tijolos.get(tipo_tijolo)
            massa = self.massas.get(tipo_massa)

            print("dados_tijolo =", dados_tijolo)
            print("massa =", massa)

            if not dados_tijolo or not massa:
                self.mostrar_snackbar("⚠️ Tipo de tijolo ou massa inválido!")
                print("DEBUG: tijolo ou massa inválido")
                return

            area_tijolos = area_liquida * (1 + margem)

            altura_tijolo = dados_tijolo["altura"]
            comprimento_tijolo = dados_tijolo["comprimento"]
            area_tijolo = altura_tijolo * comprimento_tijolo

            qtd_tijolos = ceil(area_tijolos / area_tijolo)

            massa_m2 = dados_tijolo["massa_por_m2"]
            volume_massa = (massa_m2 * area_liquida) / self.DENSIDADE_CIMENTO

            total_partes = sum(massa.values())

            vol_cimento = volume_massa * (massa["cimento"] / total_partes)
            vol_cal = volume_massa * (massa["cal"] / total_partes)
            vol_areia = volume_massa * (massa["areia"] / total_partes)

            cimento_kg = vol_cimento * self.DENSIDADE_CIMENTO
            sacos_cimento = ceil(cimento_kg / 50)

            cal_kg = vol_cal * self.DENSIDADE_CAL
            sacos_cal = ceil(cal_kg / 20)

            texto = (
                f"[b]Área total da parede:[/b] {self.formatar(area_total)} m²\n"
                f"[b]Espaço perdido (portas e janelas):[/b] {self.formatar(espaco_perdido)} m²\n"
                f"[b]Área líquida da parede:[/b] {self.formatar(area_liquida)} m²\n\n"
                f"[b]Margem para tijolos:[/b] {margem * 100:.0f}%\n"
                f"[b]Tijolos necessários:[/b] {qtd_tijolos}\n\n"
                f"[b]Materiais necessários:[/b]\n"
                f"- Cimento: {sacos_cimento} saco(s) de 50kg\n"
                f"- Cal: {sacos_cal} saco(s) de 20kg\n"
                f"- Areia: {self.formatar(vol_areia)} m³\n"
            )

            print("texto final:")
            print(texto)

            self.mostrar_resultado_label(ids.resultado_paredes, texto)
            self.texto_paredes = texto
            self.gerar_resumo()

            print("===== FIM DEBUG PAREDES =====\n")

        except Exception as e:
            print("ERRO PAREDES:", e)
            print("TIPO DO ERRO:", type(e))
            self.mostrar_snackbar("⚠️ Erro no cálculo. Verifique os valores!")

    def limpar_paredes(self):
        ids = self._ids_paredes()

        ids.area_parede.text = ""
        ids.espaco_perdido_parede.text = ""

        ids.tijolo_dropdown.set_item("Selecione")
        ids.tijolo_dropdown.text = "Selecione"
        ids.tijolo_dropdown.current_item = "Selecione"

        ids.margem_paredes_dropdown.set_item("Selecione")
        ids.margem_paredes_dropdown.text = "Selecione"
        ids.margem_paredes_dropdown.current_item = "Selecione"

        ids.massa_dropdown.set_item("Selecione")
        ids.massa_dropdown.text = "Selecione"
        ids.massa_dropdown.current_item = "Selecione"

        ids.resultado_paredes.text = "O resultado aparecerá aqui..."
        self.texto_paredes = ""


#------------------------------------------------------
#   REBOCO - Cálculo e limpeza dos campos
#------------------------------------------------------

    def calcular_reboco(self):
        try:
            ids = self._ids_reboco()

            area_total = self.to_float(ids.area_reboco.text)

            espaco_str = ids.espaco_perdido_reboco.text.strip()
            espaco_perdido = self.to_float(espaco_str) if espaco_str else 0.0

            espessura = self.to_float(ids.espessura_reboco.text)

            proporcao = ids.massa_reboco_dropdown.text.strip()

            if not proporcao:
                self.mostrar_snackbar("⚠️ Selecione a proporção da massa")
                return

            area_liquida = area_total - espaco_perdido

            if area_liquida <= 0:
                self.mostrar_snackbar("⚠️ O espaço perdido não pode ser maior que a área")
                return

            volume = area_liquida * espessura

            massa = self.massas.get(proporcao)

            if not massa:
                self.mostrar_snackbar("⚠️ Proporção inválida")
                return

            total_partes = sum(massa.values())

            vol_cimento = volume * (massa["cimento"] / total_partes)
            vol_cal = volume * (massa["cal"] / total_partes)
            vol_areia = volume * (massa["areia"] / total_partes)

            cimento_kg = vol_cimento * self.DENSIDADE_CIMENTO
            sacos_cimento = ceil(cimento_kg / 50)

            cal_kg = vol_cal * self.DENSIDADE_CAL
            sacos_cal = ceil(cal_kg / 20)

            texto = (
                f"[b]Área total das paredes:[/b] {self.formatar(area_total)} m²\n"
                f"[b]Espaço perdido:[/b] {self.formatar(espaco_perdido)} m²\n"
                f"[b]Área líquida:[/b] {self.formatar(area_liquida)} m²\n\n"
                f"[b]Volume de reboco:[/b] {self.formatar(volume)} m³\n\n"
                f"[b]Materiais Necessários:[/b]\n"
                f"- Cimento: {sacos_cimento} saco(s) de 50kg\n"
                f"- Cal: {sacos_cal} saco(s) de 20kg\n"
                f"- Areia: {self.formatar(vol_areia)} m³\n"
            )

            ids.resultado_reboco.text = texto
            self.texto_reboco = texto
            self.gerar_resumo()

        except Exception as e:
            print("ERRO REBOCO:", e)
            self.mostrar_snackbar("⚠️ Verifique os valores informados")

    def limpar_reboco(self):
        ids = self._ids_reboco()

        ids.area_reboco.text = ""
        ids.espaco_perdido_reboco.text = ""
        ids.espessura_reboco.text = ""

        ids.massa_reboco_dropdown.set_item("Selecione")
        ids.massa_reboco_dropdown.text = "Selecione"
        ids.massa_reboco_dropdown.current_item = "Selecione"

        self.mostrar_resultado_label(ids.resultado_reboco, "O resultado aparecerá aqui...")
        self.texto_reboco = ""

#------------------------------------------------------
#   CONTRAPISO - Cálculo e limpeza dos campos
#------------------------------------------------------

    def calcular_contrapiso(self):
        try:
            ids = self._ids_contrapiso()

            area = self.to_float(ids.area_contrapiso.text)
            esp = self.to_float(ids.espessura_contrapiso.text)
            proporcao = ids.proporcao_contrapiso_dropdown.text.strip()

            if not proporcao or proporcao == "Selecione":
                self.mostrar_snackbar("⚠️ Selecione a proporção do concreto")
                return

            volume_total = area * esp

            proporcoes = {
                "1:3:3": {"cimento": 1, "areia": 3, "pedra": 3},
                "1:4:3": {"cimento": 1, "areia": 4, "pedra": 3},
                "1.5:5:5": {"cimento": 1.5, "areia": 5, "pedra": 5}
            }

            self.proporcao_contrapiso_dropdown = proporcao

            prop = proporcoes.get(proporcao)
            if not prop:
                self.mostrar_snackbar("⚠️ Proporção inválida")
                return

            total_partes = sum(prop.values())

            vol_cimento = volume_total * (prop["cimento"] / total_partes)
            vol_areia = volume_total * (prop["areia"] / total_partes)
            vol_pedra = volume_total * (prop["pedra"] / total_partes)

            cimento_kg = vol_cimento * 2500
            sacos_cimento = ceil(cimento_kg / 50)

            texto = (
                f"[b]Área do contrapiso:[/b] {self.formatar(area)} m²\n"
                f"[b]Volume total do contrapiso:[/b] {self.formatar(volume_total)} m³\n\n"
                f"[b]Materiais Necessários:[/b]\n"
                f"- Cimento: {sacos_cimento} saco(s) de 50kg\n"
                f"- Areia: {self.formatar(vol_areia)} m³\n"
                f"- Pedra: {self.formatar(vol_pedra)} m³\n"
            )

            self.mostrar_resultado_label(ids.resultado_contrapiso, texto)
            self.texto_contrapiso = texto
            self.gerar_resumo()

        except Exception as e:
            print("ERRO CONTRAPISO:", e)
            self.mostrar_snackbar("⚠️ Verifique os valores informados")

    def limpar_contrapiso(self):
        ids = self._ids_contrapiso()

        ids.area_contrapiso.text = ""
        ids.espessura_contrapiso.text = ""

        ids.proporcao_contrapiso_dropdown.set_item("Selecione")
        ids.proporcao_contrapiso_dropdown.text = "Selecione"
        ids.proporcao_contrapiso_dropdown.current_item = "Selecione"

        self.mostrar_resultado_label(ids.resultado_contrapiso, "O resultado aparecerá aqui...")
        self.texto_contrapiso = ""
        self.proporcao_contrapiso_dropdown = "Selecione"

#------------------------------------------------------
#   REVESTIMENTO - Cálculo e limpeza dos campos
#------------------------------------------------------

    def mostrar_revestimento(self, tipo, active, tab_revest):
        if not active:
            return

        card_piso = tab_revest.ids.card_piso
        card_azulejo = tab_revest.ids.card_azulejo
        resultado = tab_revest.ids.resultado_revestimento
        scroll = tab_revest.ids.scroll_revestimento

        def mostrar(card):
            card.disabled = False
            card.opacity = 1
            card.size_hint_y = None
            self._aplicar_tema_card_revestimento(card)
            Clock.schedule_once(lambda dt: self._ajustar_card_revestimento(card), 0)

        def esconder(card):
            card.disabled = True
            card.opacity = 0
            card.size_hint_y = None
            card.height = 0

        if tipo == "piso":
            mostrar(card_piso)
            esconder(card_azulejo)

        elif tipo == "azulejo":
            esconder(card_piso)
            mostrar(card_azulejo)

        elif tipo == "ambos":
            mostrar(card_piso)
            mostrar(card_azulejo)

        self.mostrar_resultado_label(resultado, "O resultado aparecerá aqui.")
        self.texto_revestimento = ""

        Clock.schedule_once(lambda dt: self._atualizar_altura_revestimento(tab_revest), 0.05)
        Clock.schedule_once(lambda dt: setattr(scroll, "scroll_y", 1), 0.12)

    def _atualizar_altura_revestimento(self, tab_revest):
        try:
            card_piso = tab_revest.ids.card_piso
            card_azulejo = tab_revest.ids.card_azulejo

            if card_piso.opacity == 1 and not card_piso.disabled:
                card_piso.do_layout()
                card_piso.height = card_piso.minimum_height
            else:
                card_piso.height = 0
                card_piso.size_hint_y = None

            if card_azulejo.opacity == 1 and not card_azulejo.disabled:
                card_azulejo.do_layout()
                card_azulejo.height = card_azulejo.minimum_height
            else:
                card_azulejo.height = 0
                card_azulejo.size_hint_y = None

            tab_revest.do_layout()

        except Exception as e:
            print("ERRO AO ATUALIZAR ALTURA DO REVESTIMENTO:", e)

    def calcular_revestimento(self):
        try:
            ids = self._ids_revestimento()

            resultado = ""

            piso_ativo = ids.card_piso.opacity == 1 and not ids.card_piso.disabled
            az_ativo = ids.card_azulejo.opacity == 1 and not ids.card_azulejo.disabled

            if piso_ativo:
                area_texto = ids.area_piso.text.strip()
                tamanho = ids.tamanho_piso_drop.text.strip()
                junta_texto = ids.junta_piso_drop.text.strip()

                if not area_texto:
                    self.mostrar_snackbar("⚠️ Informe a área do piso")
                    return

                if not tamanho or tamanho == "Selecione":
                    self.mostrar_snackbar("⚠️ Selecione o tamanho do piso")
                    return

                if not junta_texto or junta_texto == "Selecione":
                    self.mostrar_snackbar("⚠️ Selecione a junta do piso")
                    return

                area = self.to_float(area_texto)
                junta = int(junta_texto)

                area_margem = area * 1.10

                consumo = self.consumo_rejunte[tamanho][junta]
                kg_rej = round((area / consumo) * 1.10, 2)

                largura_cm, altura_cm = map(int, tamanho.split("x"))
                area_peca = (largura_cm / 100) * (altura_cm / 100)
                kgm2 = 5 if area_peca <= 0.9 else 8

                kg_arg = round(area * kgm2 * 1.10, 2)
                sacos_20 = math.ceil(kg_arg / 20)
                qtd_pecas = math.ceil(area_margem / area_peca)

                resultado += (
                    "[b]Piso:[/b]\n"
                    f"[b]Área total:[/b] {self.formatar(area)} m²\n"
                    f"[b]Área com margem (10%):[/b] {self.formatar(area_margem)} m²\n\n"
                    f"[b]Peças necessárias:[/b] {qtd_pecas}\n\n"
                    f"[b]Materiais Necessários:[/b]\n"
                    f"- Rejunte necessário: {self.formatar(kg_rej)} kg\n"
                    f"- Argamassa: {self.formatar(kg_arg)} kg\n"
                    f"- Sacos de 20 kg: {sacos_20}\n"
                )

            if az_ativo:
                area_texto = ids.area_azulejo.text.strip()
                tamanho = ids.tamanho_az_drop.text.strip()
                junta_texto = ids.junta_az_drop.text.strip()

                if not area_texto:
                    self.mostrar_snackbar("⚠️ Informe a área do azulejo")
                    return

                if not tamanho or tamanho == "Selecione":
                    self.mostrar_snackbar("⚠️ Selecione o tamanho do azulejo")
                    return

                if not junta_texto or junta_texto == "Selecione":
                    self.mostrar_snackbar("⚠️ Selecione a junta do azulejo")
                    return

                area = self.to_float(area_texto)
                junta = int(junta_texto)

                area_margem = area * 1.10

                consumo = self.consumo_rejunte[tamanho][junta]
                kg_rej = round((area / consumo) * 1.10, 2)

                largura_cm, altura_cm = map(int, tamanho.split("x"))
                area_peca = (largura_cm / 100) * (altura_cm / 100)
                kgm2 = 5 if area_peca <= 0.9 else 8

                kg_arg = round(area * kgm2 * 1.10, 2)
                sacos_20 = math.ceil(kg_arg / 20)
                qtd_pecas = math.ceil(area_margem / area_peca)

                resultado += (
                    "[b]Azulejos:[/b]\n"
                    f"[b]Área total:[/b] {self.formatar(area)} m²\n"
                    f"[b]Área com margem (10%):[/b] {self.formatar(area_margem)} m²\n\n"
                    f"[b]Peças necessárias:[/b] {qtd_pecas}\n\n"
                    f"[b]Materiais Necessários:[/b]\n"
                    f"- Rejunte necessário: {self.formatar(kg_rej)} kg\n"
                    f"- Argamassa: {self.formatar(kg_arg)} kg\n"
                    f"- Sacos de 20 kg: {sacos_20}\n"
                )

            self.mostrar_resultado_label(
                ids.resultado_revestimento,
                resultado or "Selecione um tipo de cálculo."
            )

            self.texto_revestimento = resultado
            self.gerar_resumo()

        except Exception as e:
            print("ERRO REVESTIMENTO:", e)
            self.mostrar_snackbar("⚠️ Erro no cálculo. Verifique os valores!")

    def limpar_revestimento(self):
        ids = self._ids_revestimento()

        # Campos de texto
        ids.area_piso.text = ""
        ids.area_azulejo.text = ""

        # Dropdowns (SEM valor fixo)
        ids.tamanho_piso_drop.set_item("Selecione")
        ids.junta_piso_drop.set_item("Selecione")

        ids.tamanho_az_drop.set_item("Selecione")
        ids.junta_az_drop.set_item("Selecione")

        # Resultado
        ids.resultado_revestimento.text = "O resultado aparecerá aqui..."
        self.texto_revestimento = ""

        # (Opcional) esconder cards novamente se você usa isso
        try:
            self.esconder(ids.card_piso)
            self.esconder(ids.card_azulejo)
        except:
            pass

#------------------------------------------------------
#   ORÇAMENTO - Cálculo e limpeza dos campos
#------------------------------------------------------

    def calcular_orcamento(self):
        try:
            ids = self._ids_orcamento()

            self.precos_materiais = {
                "tipo_tijolo": ids.tipo_tijolo_orcamento.text,
                "tijolo_preco": self.to_float(ids.preco_tijolo.text),
                "cimento_50kg": self.to_float(ids.preco_cimento.text),
                "cal_20kg": self.to_float(ids.preco_cal.text),
                "areia_m3": self.to_float(ids.preco_areia.text),
                "pedra_m3": self.to_float(ids.preco_pedra.text),
                "argamassa_20kg": self.to_float(ids.preco_argamassa.text),
                "rejunte_kg": self.to_float(ids.preco_rejunte.text),
            }

            self.mostrar_resultado_label(
                ids.resultado_orcamento,
                "[b]Valores salvos com sucesso![/b]\nEles serão usados no resumo da obra."
            )

            self.mostrar_snackbar("✅ Valores de orçamento salvos!")
            self.gerar_resumo()

            try:
                self._tabs().switch_tab("Resumo")
            except:
                pass

        except Exception as e:
            print("ERRO ORÇAMENTO:", e)
            self.mostrar_snackbar("⚠️ Erro no cálculo. Verifique os valores!")

    def limpar_orcamento(self):
        ids = self._ids_orcamento()

        ids.tipo_tijolo_orcamento.set_item("Tijolo Baiano")
        ids.tipo_tijolo_orcamento.text = "Tijolo Baiano"
        ids.tipo_tijolo_orcamento.current_item = "Tijolo Baiano"

        ids.preco_tijolo.text = ""
        ids.preco_cimento.text = ""
        ids.preco_cal.text = ""
        ids.preco_areia.text = ""
        ids.preco_pedra.text = ""
        ids.preco_argamassa.text = ""
        ids.preco_rejunte.text = ""

        self.mostrar_resultado_label(
            ids.resultado_orcamento,
            "Os valores serão usados no resumo da obra."
        )

    def extrair_valor(self, texto, chave):
        try:
            inicio = texto.index(chave) + len(chave)
            fim = texto.index("\n", inicio)
            valor = texto[inicio:fim].strip().split()[0]
            return valor.replace(",", ".")
        except Exception:
            return "0"

#------------------------------------------------------
#   CALCULAR CUSTOS POR ETAPA
#------------------------------------------------------

    def calcular_custos(self):
        custos = {}

        # --------------------------------------
        # BROCAS
        # --------------------------------------
        conteudo = self.texto_brocas
        if conteudo.strip():
            try:
                sacos_cimento = 0
                vol_areia = 0
                vol_pedra = 0

                for linha in conteudo.splitlines():
                    linha_limpa = self.limpar_markup(linha)

                    if "Cimento:" in linha_limpa:
                        sacos_cimento = self.to_float(linha_limpa.split(":")[1].split()[0])
                    elif "Areia:" in linha_limpa:
                        vol_areia = self.to_float(linha_limpa.split(":")[1].replace("m³", "").strip())
                    elif "Pedra:" in linha_limpa:
                        vol_pedra = self.to_float(linha_limpa.split(":")[1].replace("m³", "").strip())

                custo = (
                    sacos_cimento * self.precos_materiais["cimento_50kg"] +
                    vol_areia * self.precos_materiais["areia_m3"] +
                    vol_pedra * self.precos_materiais["pedra_m3"]
                )

                custos["Brocas"] = custo

            except Exception as e:
                print("ERRO CUSTO BROCAS:", e)
                custos["Brocas"] = 0

        # --------------------------------------
        # BALDRAME
        # --------------------------------------
        conteudo = self.texto_baldrame
        if conteudo.strip():
            try:
                sacos_cimento = 0
                vol_areia = 0
                vol_pedra = 0

                for linha in conteudo.splitlines():
                    linha_limpa = self.limpar_markup(linha)

                    if "Cimento:" in linha_limpa:
                        sacos_cimento = self.to_float(linha_limpa.split(":")[1].split()[0])
                    elif "Areia:" in linha_limpa:
                        vol_areia = self.to_float(linha_limpa.split(":")[1].replace("m³", "").strip())
                    elif "Pedra:" in linha_limpa:
                        vol_pedra = self.to_float(linha_limpa.split(":")[1].replace("m³", "").strip())

                custo = (
                    sacos_cimento * self.precos_materiais["cimento_50kg"] +
                    vol_areia * self.precos_materiais["areia_m3"] +
                    vol_pedra * self.precos_materiais["pedra_m3"]
                )

                custos["Baldrame"] = custo

            except Exception as e:
                print("ERRO CUSTO BALDRAME:", e)
                custos["Baldrame"] = 0

        # --------------------------------------
        # PAREDES
        # --------------------------------------
        conteudo = self.texto_paredes
        if conteudo.strip():
            try:
                qtd_tijolos = 0
                sacos_cimento = 0
                sacos_cal = 0
                vol_areia = 0

                for linha in conteudo.splitlines():
                    linha_limpa = self.limpar_markup(linha)

                    if "Tijolos necessários:" in linha_limpa:
                        qtd_tijolos = self.to_float(linha_limpa.split(":")[1].strip())

                    elif "Cimento:" in linha_limpa:
                        sacos_cimento = self.to_float(linha_limpa.split(":")[1].split()[0])

                    elif "Cal:" in linha_limpa:
                        sacos_cal = self.to_float(linha_limpa.split(":")[1].split()[0])

                    elif "Areia:" in linha_limpa:
                        vol_areia = self.to_float(linha_limpa.split(":")[1].replace("m³", "").strip())

                custo_tijolos = qtd_tijolos * self.precos_materiais.get("tijolo_preco", 0.0)

                custo_massa = (
                    sacos_cimento * self.precos_materiais["cimento_50kg"] +
                    sacos_cal * self.precos_materiais["cal_20kg"] +
                    vol_areia * self.precos_materiais["areia_m3"]
                )

                custos["Paredes"] = custo_tijolos + custo_massa

            except Exception as e:
                print("ERRO CUSTO PAREDES:", e)
                custos["Paredes"] = 0

        # --------------------------------------
        # REBOCO
        # --------------------------------------
        conteudo = self.texto_reboco
        if conteudo.strip():
            try:
                sacos_cimento = 0
                sacos_cal = 0
                vol_areia = 0

                for linha in conteudo.splitlines():
                    linha_limpa = self.limpar_markup(linha)

                    if "Cimento:" in linha_limpa:
                        sacos_cimento = self.to_float(linha_limpa.split(":")[1].split()[0])
                    elif "Cal:" in linha_limpa:
                        sacos_cal = self.to_float(linha_limpa.split(":")[1].split()[0])
                    elif "Areia:" in linha_limpa:
                        vol_areia = self.to_float(linha_limpa.split(":")[1].replace("m³", "").strip())

                custo_reb = (
                    sacos_cimento * self.precos_materiais["cimento_50kg"] +
                    sacos_cal * self.precos_materiais["cal_20kg"] +
                    vol_areia * self.precos_materiais["areia_m3"]
                )

                custos["Reboco"] = custo_reb

            except Exception as e:
                print("ERRO CUSTO REBOCO:", e)
                custos["Reboco"] = 0

        # --------------------------------------
        # CONTRAPISO
        # --------------------------------------
        conteudo = self.texto_contrapiso
        if conteudo.strip():
            try:
                sacos_cimento = 0
                vol_areia = 0
                vol_pedra = 0

                for linha in conteudo.splitlines():
                    linha_limpa = self.limpar_markup(linha)

                    if "Cimento:" in linha_limpa:
                        sacos_cimento = self.to_float(linha_limpa.split(":")[1].split()[0])

                    elif "Areia:" in linha_limpa:
                        vol_areia = self.to_float(linha_limpa.split(":")[1].replace("m³", "").strip())

                    elif "Pedra:" in linha_limpa:
                        vol_pedra = self.to_float(linha_limpa.split(":")[1].replace("m³", "").strip())

                custo_contra = (
                    sacos_cimento * self.precos_materiais["cimento_50kg"] +
                    vol_areia * self.precos_materiais["areia_m3"] +
                    vol_pedra * self.precos_materiais["pedra_m3"]
                )

                custos["Contrapiso"] = custo_contra

            except Exception as e:
                print("ERRO CUSTO CONTRAPISO:", e)
                custos["Contrapiso"] = 0

        # --------------------------------------
        # REVESTIMENTO
        # --------------------------------------
        conteudo = self.texto_revestimento
        if conteudo.strip():
            try:
                kg_rej = 0
                sacos_arg = 0

                for linha in conteudo.splitlines():
                    linha_limpa = self.limpar_markup(linha)

                    if "Rejunte necessário" in linha_limpa:
                        kg_rej += self.to_float(linha_limpa.split(":")[1].replace("kg", "").strip())

                    elif "Sacos de 20 kg" in linha_limpa:
                        sacos_arg += self.to_float(linha_limpa.split(":")[1].replace("un", "").strip())

                custo_rev = (
                    kg_rej * self.precos_materiais["rejunte_kg"] +
                    sacos_arg * self.precos_materiais["argamassa_20kg"]
                )

                custos["Revestimentos"] = custo_rev

            except Exception as e:
                print("ERRO CUSTO REVESTIMENTO:", e)
                custos["Revestimentos"] = 0

        return custos

#------------------------------------------------------
#   GERAR RESUMO DA OBRA
#------------------------------------------------------

    def gerar_resumo(self):
        secoes = [
            ("BROCAS", self.texto_brocas),
            ("BALDRAME", self.texto_baldrame),
            ("PAREDES", self.texto_paredes),
            ("REBOCO", self.texto_reboco),
            ("CONTRAPISO", self.texto_contrapiso),
            ("REVESTIMENTO", self.texto_revestimento),
        ]

        emojis_secao = {
            "BROCAS": "🕳️",
            "BALDRAME": "🧱",
            "PAREDES": "🧱",
            "REBOCO": "🪵",
            "CONTRAPISO": "🧱",
            "REVESTIMENTO": "🧩",
        }

        linhas = []

        linhas.append("[b]📋 RESUMO DA OBRA - BuildCalc[/b]")
        linhas.append("")

        for nome, texto in secoes:

            if texto.strip():

                emoji = emojis_secao.get(nome, "📦")

                linhas.append(f"[b]{emoji} {nome}[/b]")
                linhas.append("------------------------------")

                texto_limpo = texto.strip()

                # reforça negrito em palavras importantes
                texto_limpo = texto_limpo.replace("[b]Materiais necessários:[/b]", "[b]Materiais necessários:[/b]")
                texto_limpo = texto_limpo.replace("[b]Materiais:[/b]", "[b]Materiais:[/b]")
                texto_limpo = texto_limpo.replace("[b]Peças necessárias: [/b]", "[b]Peças necessárias:[/b] ")
                texto_limpo = texto_limpo.replace("[b]Área total: [/b]", "[b]Área total:[/b] ")
                texto_limpo = texto_limpo.replace("[b]Área com margem (10%): [/b]", "[b]Área com margem (10%):[/b] ")
                texto_limpo = texto_limpo.replace("[b]Volume total das brocas:[/b]", "[b]Volume total das brocas:[/b]")
                texto_limpo = texto_limpo.replace("[b]Volume total do baldrame:[/b]", "[b]Volume total do baldrame:[/b]")
                texto_limpo = texto_limpo.replace("[b]Volume total do contrapiso:[/b]", "[b]Volume total do contrapiso:[/b]")
                texto_limpo = texto_limpo.replace("[b]Volume de reboco:[/b]", "[b]Volume de reboco:[/b]")
                texto_limpo = texto_limpo.replace("[b]Tijolos necessários:[/b]", "[b]Tijolos necessários:[/b]")
                texto_limpo = texto_limpo.replace("[b]Margem para tijolos:[/b]", "[b]Margem para tijolos:[/b]")
                texto_limpo = texto_limpo.replace("[b]Espaço perdido(Portas e Janelas):[/b]", "[b]Espaço perdido (portas e janelas):[/b]")

                linhas.append(texto_limpo)
                linhas.append("")

        custos = self.calcular_custos()
        total_geral = sum(custos.values())

        linhas.append("")
        linhas.append("[b]CUSTOS POR ETAPA[/b]")
        linhas.append("------------------------------------------------")
        linhas.append("")

        for nome, valor in custos.items():

            emojis = {
                "Brocas": "🕳️",
                "Baldrame": "🧱",
                "Paredes": "🧱",
                "Reboco": "🪵",
                "Contrapiso": "🧱",
                "Revestimentos": "🧩"
            }

            emoji = emojis.get(nome, "📦")

            valor_formatado = f"{valor:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")

            nome_formatado = f"[b]{emoji} {nome}:[/b]"

            largura_total = 35
            qtd_pontos = largura_total - len(nome)

            if qtd_pontos < 3:
                qtd_pontos = 3

            pontinhos = "." * qtd_pontos

            linhas.append(f"{nome_formatado}{pontinhos}R$ {valor_formatado}")

        linhas.append("")
        linhas.append("------------------------------------------------")
        linhas.append("[b]TOTAL GERAL DA OBRA[/b]")

        total_formatado = f"{total_geral:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
        linhas.append(f"[b]R$ {total_formatado}[/b]")

        resumo_final = "\n".join(linhas)
        self.texto_resumo = resumo_final

        ids_resumo = self._ids_resumo()
        self.mostrar_resultado_label(ids_resumo.resultado_resumo, resumo_final)

if __name__ == "__main__":
    BuildCalcApp().run()