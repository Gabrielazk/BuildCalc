from kivy.config import Config

# Size fixo para mobile (400x700)
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '700')
Config.set('graphics', 'resizable', False)

from kivy.core.window import Window
from kivymd.app import MDApp
from src.views.main_screen import MainScreenManager
from src.models.database import init_db

Window.size = (400, 700)

class BuildCalcApp(MDApp):
    def build(self):
        init_db()  # Inicializa o SQLite
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"  # Palette em tons de Azul
        return MainScreenManager()

if __name__ == "__main__":
    BuildCalcApp().run()