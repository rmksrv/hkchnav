from api import Navigator
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView


class hkchnavApp(App):

    def __init__(self):
        super().__init__()
        self.nav = Navigator()


    def build(self):
        gist_json = self.nav.goto('/').get()
        main_layout = GridLayout(
            cols=1,
            padding=10,
            spacing=10,
            size_hint=(None, None),
            width=Window.width,
        )
        main_layout.bind(minimum_height=main_layout.setter('height'))

        for category in gist_json:
            # adding category labels
            label = Label(
                text=category,
                size=(0.97 * Window.width, 40),
                size_hint=(None, None),
            )
            main_layout.add_widget(label)
            for board in gist_json[category]:
                # adding board buttons
                button_name = '/{} - {}'.format(board['id'], board['name'])
                button = Button(
                    text=button_name,
                    size=(0.97 * Window.width, 40),
                    size_hint=(None, None),
                )
                main_layout.add_widget(button)

        root = ScrollView(
            size_hint=(None, None),
            size=(Window.width ,Window.height),
            pos_hint={'center_x': .5, 'center_y': .5},
            do_scroll_x=False
        )
        root.add_widget(main_layout)

        return root


if __name__ == '__main__':
    hkchnavApp().run()
