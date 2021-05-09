from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivy.lang import Builder
from cats.kocky import Kocky


class BMIScreen(Screen):
    pass


class DatabaseScreen(Screen):
    pass


class Test(MDApp):

    def build(self):
        self.theme_cls.primary_palette = "Gray"
        self.title = 'Veterinárna Adély Pavlincové xd'
        self.icon = f"images/1.png"
        builder = Builder.load_file('main.kv')
        self.kocky = Kocky()
        builder.ids.navigation.ids.tab_manager.screens[0].add_widget(self.kocky)
        return builder


Test().run()