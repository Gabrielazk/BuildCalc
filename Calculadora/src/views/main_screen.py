"""Junta todas as telas do app. Cada tela fica no seu próprio arquivo, nesta mesma pasta."""
from kivymd.uix.screenmanager import MDScreenManager

from src.views.login_screen import LoginScreen
from src.views.home_screen import HomeScreen
from src.views.calculator_screen import CalculatorScreen
from src.views.summary_screen import SummaryScreen
from src.views.history_screen import HistoryScreen
from src.views.settings_screen import SettingsScreen


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