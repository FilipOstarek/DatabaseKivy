from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.button import MDFlatButton, MDFillRoundFlatIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList, ThreeLineAvatarIconListItem, ImageLeftWidget, IconRightWidget
from kivymd.uix.menu import MDDropdownMenu
from cats.database import Popis, Fotka, Database, Druh

class DruhContent(BoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

class VyberDruhu(MDDialog):
    def __init__(self, *args, **kwargs):
        super(VyberDruhu, self).__init__(
            type="custom",
            content_cls=DruhContent(),
            title='Nový druh',
            size_hint=(1, 1),
            buttons=[
                MDFlatButton(text='Uložit', on_release=self.save_dialog),
                MDFlatButton(text='Zrušit', on_release=self.cancel_dialog)
            ]
        )

    def save_dialog(self, *args):
        druh = Druh()
        druh.jmeno_druhu = self.content_cls.ids.druh_kocky.text
        app.kocky.database.create_druh(druh)
        self.dismiss()

    def cancel_dialog(self, *args):
        self.dismiss()


class KockaContent(BoxLayout):
    def __init__(self, id, *args, **kwargs):
        super().__init__(**kwargs)
        if id:
            kocka = vars(app.kocky.database.read_popisy_by_id(id))
        else:
            kocka = {"id":"", "jmeno":"Jméno", "druh": "Druh", "vek": "Vek", "vaha": "Vaha", "samotny_popis":"popis"}

        self.ids.jmeno_kocky.text = kocka['jmeno']
        self.ids.vek_kocky.text = kocka['vek']
        self.ids.vaha_kocky.text = kocka['vaha']
        self.ids.popis_kocky.text = kocka['samotny_popis']
        druhy = app.kocky.database.read_druhy()
        #print("tohle")
        #print(druhy)
        #for druh in druhy:
            #prep = str(vars(druh)).split(': ')
            #print(str(vars(druh)))
            #print(prep)
            #print(f"{druh.id}")
            #print(druh.__dict__.id())
            #print(f"{druhy.id}")
        menu_items = [{"viewclass": "OneLineListItem", "text": f"{druh.jmeno_druhu}", "on_release": lambda x=f"{druh.jmeno_druhu}": self.set_item(x)} for druh in druhy]
        self.menu_kocek = MDDropdownMenu(
            caller=self.ids.druh_kocky,
            items=menu_items,
            position="center",
            width_mult=5,
        )
        self.ids.druh_kocky.set_item(kocka['druh'])
        self.ids.druh_kocky.text = kocka['druh']

    def set_item(self, text_item):
        self.ids.druh_kocky.set_item(text_item)
        self.ids.druh_kocky.text = text_item
        self.menu_kocek.dismiss()

class KockaDialog(MDDialog):
    def __init__(self, id, *args, **kwargs):
        super(KockaDialog, self).__init__(
            type="custom",
            content_cls=KockaContent(id=id),
            title='Záznam nové kočky/předělání',
            size_hint=(1, 1),
            buttons=[
                MDFlatButton(text='Uložit', on_release=self.save_dialog),
                MDFlatButton(text='Zrušit', on_release=self.cancel_dialog)
            ]
        )
        self.id = id

    def save_dialog(self, *args):
        kocka = {}
        kocka['jmeno'] = self.content_cls.ids.jmeno_kocky.text
        kocka['vek'] = self.content_cls.ids.vek_kocky.text
        kocka['vaha'] = self.content_cls.ids.vaha_kocky.text
        kocka['druh'] = self.content_cls.ids.druh_kocky.text
        kocka['samotny_popis'] = self.content_cls.ids.popis_kocky.text
        if self.id:
            kocka["id"] = self.id
            app.kocky.update(kocka)
        else:
            app.kocky.create(kocka)
        self.dismiss()

    def cancel_dialog(self, *args):
        self.dismiss()

class MyItem(ThreeLineAvatarIconListItem):
    def __init__(self, item, *args, **kwargs):
        super(MyItem, self).__init__()
        self.id = item['id']
        self.text = item['jmeno']
        self.secondary_text = str(item['druh'])
        self.tertiary_text = str(item['samotny_popis'])
        self._no_ripple_effect = True
        self.image = ImageLeftWidget()
        self.image.source = f"images/{item['id']}.png"
        self.add_widget(self.image)
        self.icon = IconRightWidget(icon="delete", on_release=self.on_delete)
        self.add_widget(self.icon)

    def on_press(self):
        self.dialog = KockaDialog(id=self.id)
        self.dialog.open()

    def on_delete(self, *args):
        yes_button = MDFlatButton(text='Ano', on_release=self.yes_button_release)
        no_button = MDFlatButton(text='Ne', on_release=self.no_button_release)
        self.dialog_confirm = MDDialog(type="confirmation", title='Smazání záznamu', text="Chcete opravdu smazat tento záznam?", buttons=[yes_button, no_button])
        self.dialog_confirm.open()

    def yes_button_release(self, *args):
        app.kocky.delete(self.id)
        self.dialog_confirm.dismiss()

    def no_button_release(self, *args):
        self.dialog_confirm.dismiss()

class Kocky(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(Kocky, self).__init__(orientation="vertical")
        global app
        app = App.get_running_app()
        scrollview = ScrollView()
        self.list = MDList()
        self.database = Database(dbtype='sqlite', dbname='data.db')
        self.rewrite_list()
        scrollview.add_widget(self.list)
        self.add_widget(scrollview)
        button_box = BoxLayout(orientation='horizontal', size_hint_y=0.1)
        new_kocka_btn = MDFillRoundFlatIconButton()
        new_kocka_btn.text = "Nový záznam"
        new_kocka_btn.icon = "plus"
        new_kocka_btn.icon_color = [1, 1, 1, 1]
        new_kocka_btn.text_color = [0.999, 0.999, 0.999, 1]
        new_kocka_btn.md_bg_color = [0.22, 0.627, 0.58, 1]
        new_kocka_btn.font_style = "Button"
        new_kocka_btn.pos_hint = {"center_x": .5}
        new_kocka_btn.on_release = self.on_create_kocka
        button_box.add_widget(new_kocka_btn)

        new_druh_btn = MDFillRoundFlatIconButton()
        new_druh_btn.text = "Nový druh"
        new_druh_btn.icon = "plus"
        new_druh_btn.icon_color = [1, 1, 1, 1]
        new_druh_btn.text_color = [0.999, 0.999, 0.999, 1]
        new_druh_btn.md_bg_color = [0.22, 0.627, 0.58, 1]
        new_druh_btn.font_style = "Button"
        new_druh_btn.pos_hint = {"center_x": .6}
        new_druh_btn.on_release = self.on_create_druh
        button_box.add_widget(new_druh_btn)
        self.add_widget(button_box)


    def rewrite_list(self):
        self.list.clear_widgets()
        kocky = self.database.read_popisy()
        for kocka in kocky:
            print("owo")
            print(vars(kocka))
            self.list.add_widget(MyItem(item=vars(kocka)))

    def on_create_kocka(self, *args):
        self.dialog = KockaDialog(id=None)
        self.dialog.open()

    def on_create_druh(self, *args):
        self.dialog = VyberDruhu()
        self.dialog.open()

    def create(self, kocka):
        create_kocka = Popis()
        create_kocka.jmeno = kocka['jmeno']
        create_kocka.druh = kocka['druh']
        create_kocka.vek = kocka['vek']
        create_kocka.vaha = kocka['vaha']
        create_kocka.samotny_popis = kocka['samotny_popis']
        self.database.create_popis(create_kocka)
        self.rewrite_list()


    def update(self, kocka):
        update_kocka = self.database.read_popisy_by_id(kocka['id'])
        update_kocka.jmeno = kocka['jmeno']
        update_kocka.druh = kocka['druh']
        update_kocka.vek = kocka['vek']
        update_kocka.vaha = kocka['vaha']
        update_kocka.samotny_popis = kocka['samotny_popis']
        self.database.update()
        self.rewrite_list()

    def delete(self, id):
        self.database.delete_popis(id)
        self.rewrite_list()