"""Tela de Resumo (orçamento consolidado da obra)."""
import math
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
from src.calculators.baldrame import LITROS_POR_LATA
from src.calculators.hidraulica import BARRA_TUBO_M
from src.models.database import salvar_orcamento, quantidade_orcamentos_salvos
from src.views.comum import CONFIG_APP, ORCAMENTO_FINAL, txt, fmt_moeda, fmt_num
from src.views.calculator_screen import CalculatorScreen
from src.views import comum


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
            
        user_id = comum.USUARIO_LOGADO.get("id") if comum.USUARIO_LOGADO else None
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
        
        user_id = comum.USUARIO_LOGADO.get("id") if comum.USUARIO_LOGADO else None
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
            total_imperm = sum(item.get("imperm_litros", 0) for item in ORCAMENTO_FINAL)
            total_cal = sum(item.get("cal", 0) for item in ORCAMENTO_FINAL)
            total_tijolos = sum(item.get("tijolos", 0) for item in ORCAMENTO_FINAL)
            total_argamassa = sum(item.get("argamassa_sacos", 0) for item in ORCAMENTO_FINAL)
            total_rodape = sum(item.get("rodape_m", 0) for item in ORCAMENTO_FINAL)
            itens_piso = [i for i in ORCAMENTO_FINAL if i.get("tipo") == "piso"]
            itens_azulejo = [i for i in ORCAMENTO_FINAL if i.get("tipo") == "azulejo"]
            
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
            if total_tijolos > 0:
                texto += f"• {txt('label_tijolos_resumo')}: {total_tijolos} {txt('un_unidades')}\n"
            texto += f"• Cimento 50kg: {total_cimento} sacos\n"
            if total_cal > 0:
                texto += f"• Cal 20kg: {total_cal} sacos\n"
            texto += f"• Areia: {fmt_num(total_areia, 2)} m³\n"
            if total_pedra > 0:
                texto += f"• Brita: {fmt_num(total_pedra, 2)} m³\n"
            if total_aco > 0:
                texto += f"• Aço: {fmt_num(total_aco, 1)} kg ({total_barras} barras de 12m)\n"
            for rotulo, itens_c in (("label_piso_resumo", itens_piso), ("label_azulejo_resumo", itens_azulejo)):
                if itens_c:
                    caixas_c = sum(i.get("caixas", 0) for i in itens_c)
                    pecas_c = sum(i.get("pecas", 0) for i in itens_c)
                    if caixas_c > 0:
                        texto += f"• {txt(rotulo)}: {caixas_c} {txt('un_caixas')} ({pecas_c} {txt('un_pecas')})\n"
                    else:
                        texto += f"• {txt(rotulo)}: {pecas_c} {txt('un_pecas')}\n"
            if total_argamassa > 0:
                texto += f"• {txt('label_argamassa_resumo')}: {total_argamassa} {txt('un_sacos_cal').replace(' de 20 kg', '').replace(' of 20 kg', '')}\n"
            if total_rodape > 0:
                texto += f"• {txt('label_rodape')}: {fmt_num(total_rodape, 2)} m\n"
            total_laje_pm = sum(item.get("laje_premoldada_m2", 0) for item in ORCAMENTO_FINAL)
            if total_laje_pm > 0:
                total_lajotas = sum(item.get("lajotas", 0) for item in ORCAMENTO_FINAL)
                linha = f"• {txt('label_laje_pm_resumo')}: {fmt_num(total_laje_pm, 2)} m²"
                if total_lajotas > 0:
                    linha += f" ({txt('label_lajotas')}: {total_lajotas} {txt('un_unidades')})"
                texto += linha + "\n"
            for item in ORCAMENTO_FINAL:
                if item.get("tipo") != "telhado":
                    continue
                linha = f"• {txt('label_telhas_resumo')} ({CalculatorScreen._rotulo_telha(item['tipo_telha'])}): {item['telhas']} {txt('un_unidades')}"
                if item.get("cumeeiras", 0) > 0:
                    linha += f" + {item['cumeeiras']} {txt('un_pecas')} {txt('un_de')} {txt('label_cumeeira').lower()}"
                texto += linha + "\n"
                pecas_madeira = [
                    f"{txt('label_' + chave).lower()} {fmt_num(item.get(chave + '_m', 0), 1)} m"
                    for chave in ("ripas", "caibros", "tercas") if item.get(chave + "_m", 0) > 0
                ]
                if pecas_madeira:
                    texto += f"• {txt('label_madeira_resumo')}: {', '.join(pecas_madeira)}\n"
            for item in ORCAMENTO_FINAL:
                if item.get("tipo") != "eletrica":
                    continue
                if item.get("rolos_conduite", 0) > 0:
                    qtd = item['rolos_conduite']
                    texto += f"• {txt('label_conduite')}: {qtd} {txt('un_rolo_conduite') if qtd == 1 else txt('un_rolos_conduite')}\n"
                for bitola, qtd in item.get("fios", {}).items():
                    texto += f"• {txt('label_fio').format(b=CalculatorScreen._rotulo_bitola_fio(float(bitola)))}: {qtd} {txt('un_rolo_fio') if qtd == 1 else txt('un_rolos_fio')}\n"
                for chave, rotulo in (("caixas_4x2", "label_caixa_4x2"), ("caixas_octogonais", "label_caixa_oct"),
                                      ("tomadas", "label_tomadas"), ("interruptores", "label_interruptores")):
                    if item.get(chave, 0) > 0:
                        texto += f"• {txt(rotulo)}: {item[chave]} {txt('un_unidades')}\n"
            for item in ORCAMENTO_FINAL:
                if item.get("tipo") != "hidraulica":
                    continue
                for tubo, barras in item.get("tubos", {}).items():
                    texto += f"• {txt('label_tubo_' + tubo)}: {CalculatorScreen._texto_barras(barras, BARRA_TUBO_M[tubo])}\n"
                for tipo, qtd in item.get("conexoes", {}).items():
                    texto += f"• {txt('label_conexoes_' + tipo)}: {qtd} {txt('un_unidades')}\n"
                if item.get("registros", 0) > 0:
                    texto += f"• {txt('label_registros')}: {item['registros']} {txt('un_unidades')}\n"
            for item in ORCAMENTO_FINAL:
                if item.get("tipo") != "pintura":
                    continue
                for produto, (latas, galoes) in item.get("pintura", {}).items():
                    texto += f"• {txt('label_pint_' + produto)}: {CalculatorScreen._texto_latas_galoes(latas, galoes)}\n"
                if item.get("baldes_massa", 0) > 0:
                    qtd = item["baldes_massa"]
                    texto += f"• {CalculatorScreen._rotulo_massa(item['massa_tipo'])}: {qtd} {txt('un_balde_25') if qtd == 1 else txt('un_baldes_25')}\n"
            for item in ORCAMENTO_FINAL:
                if item.get("tipo") != "esquadrias":
                    continue
                for esq in item.get("esquadrias", []):
                    texto += f"• {CalculatorScreen._texto_item_esquadria(esq)}\n"
                if item.get("tubos_espuma", 0) > 0:
                    qtd = item["tubos_espuma"]
                    texto += f"• {txt('label_res_espuma')}: {qtd} {txt('un_tubo_500') if qtd == 1 else txt('un_tubos_500')}\n"
                if item.get("parafusos", 0) > 0:
                    texto += f"• {txt('label_res_parafusos')}: {item['parafusos']} {txt('un_unidades')}\n"
                if item.get("sacos_argamassa_fix", 0) > 0:
                    qtd = item["sacos_argamassa_fix"]
                    texto += f"• {txt('label_res_argamassa_fix')}: {qtd} {txt('un_saco_20') if qtd == 1 else txt('un_sacos_20')}\n"
            total_rejunte = sum(item.get("rejunte_kg", 0) for item in ORCAMENTO_FINAL)
            if total_rejunte > 0:
                latas_1 = sum(item.get("rejunte_latas_1kg", 0) for item in ORCAMENTO_FINAL)
                latas_2 = sum(item.get("rejunte_latas_2kg", 0) for item in ORCAMENTO_FINAL)
                texto += f"• {txt('label_rejunte_resumo')}: {fmt_num(total_rejunte, 2)} kg ({CalculatorScreen._texto_latas(latas_1, latas_2)})\n"
            if total_imperm > 0:
                latas = math.ceil(total_imperm / LITROS_POR_LATA)
                un_lata = txt('un_lata') if latas == 1 else txt('un_latas')
                texto += f"• {txt('label_imperm_item')}: {fmt_num(total_imperm, 1)} L ({latas} {un_lata})\n"
                
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