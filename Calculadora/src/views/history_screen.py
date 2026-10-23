"""Tela de Histórico de orçamentos."""
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogHeadlineText,
    MDDialogSupportingText,
    MDDialogButtonContainer,
    MDDialogContentContainer,
)
from src.models.database import (
    listar_orcamentos,
    atualizar_nome_orcamento,
    excluir_orcamento,
    duplicar_orcamento,
)
from kivymd.uix.card import MDCard
from kivymd.uix.divider import MDDivider
from src.views.comum import CONFIG_APP, txt, fmt_moeda
from src.views import comum


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
        
        user_id = comum.USUARIO_LOGADO.get("id") if comum.USUARIO_LOGADO else None
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

    def _abrir_no_calculo(self, item, modo_leitura):
        dados = item["dados_json"]
        if not dados:
            return
        calc_screen = self.manager.get_screen("calculator")
        calc_screen.reiniciar(montar=False)
        calc_screen.origem = "history"
        # carrega do último para o primeiro: assim a primeira aba é a que fica aberta
        for etapa in reversed(dados):
            calc_screen.preencher_campos(etapa.get("inputs", {}), modo_leitura=modo_leitura, tipo=etapa.get("tipo", "brocas"))
            calc_screen.executar_calculo(None)
        self.manager.current = "calculator"

    def visualizar_orcamento(self, item):
        self._abrir_no_calculo(item, modo_leitura=True)

    def editar_orcamento(self, item):
        self._abrir_no_calculo(item, modo_leitura=False)

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
        user_id = comum.USUARIO_LOGADO.get("id") if comum.USUARIO_LOGADO else None
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