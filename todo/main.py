from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image

from kivy.config import Config
Config.set('graphics', 'width', '540')
Config.set('graphics', 'height', '960')

red = (255 / 255, 67 / 255, 67 / 255)
green = (0 / 255, 158 / 255, 60 / 255)


class MainApp(App):
    def build(self):
        sm.add_widget(MainScreen())
        sm.add_widget(ProfileScreen())
        sm.add_widget(OptionsScreen())
        return sm


class MainScreen(Screen):
    def __init__(self):
        super().__init__()

        self.name = 'Main'

        main_layout = FloatLayout()

        self.add_widget(main_layout)
        Background = Image(
            source='2.jpg',
            size_hint=(self.width,self.height),
            pos_hint = {'center_x': 0.3, 'center_y': 0.5}
        )
        Plank = Image(
            source='1.jpg',
            pos_hint={'center_x': 0.5, 'center_y': 0},
        )
        # Button
        Go_Screen2 = Button(text='',
                            background_normal='test.png',
                            size_hint=(0.1,0.05),
                            pos_hint={'center_x': .9, 'center_y': .1},
)

        Go_Screen2.bind(on_press=self.to_second_scrn)
        main_layout.add_widget(Background)
        main_layout.add_widget(Plank)
        main_layout.add_widget(Go_Screen2)


    def to_second_scrn(self, *args):
        self.manager.current = 'Profile'
        self.manager.transition.direction = 'up'


class ProfileScreen(Screen):
    def __init__(self):
        super().__init__()
        self.name = 'Profile'
        second_layout = FloatLayout()
        self.add_widget(second_layout)

        # Button
        Go_Back = Button(text='Back',
                         size_hint=(.1, .05),
                         pos_hint={'center_x': .1, 'center_y': .1},
                         color=green)
        Go_Options = Button(text='OPT',
                         size_hint=(.1, .05),
                         pos_hint={'center_x': .3, 'center_y': .1},
                         color=green)
        Go_Back.bind(on_press=self.to_main_scrn)
        Go_Options.bind(on_press=self.to_option_scrn)
        second_layout.add_widget(Go_Back)
        second_layout.add_widget(Go_Options)

    def to_main_scrn(self, *args):
        self.manager.current = 'Main'
        self.manager.transition.direction = 'down'
        return 0
    def to_option_scrn(self, *args):
        self.manager.current = 'Options'
        self.manager.transition.direction = 'down'
        return 0

class OptionsScreen(Screen):
    def __init__(self):
        super().__init__()
        self.name = 'Options'
        options_layout = FloatLayout()
        self.add_widget(options_layout)

        # Button
        Go_Back = Button(text='Back',
                         size_hint=(.1, .05),
                         pos_hint={'center_x': .1, 'center_y': .1},
                         color=green)

        Go_Back.bind(on_press=self.to_profile_scrn)

        options_layout.add_widget(Go_Back)

    def to_profile_scrn(self, *args):
        self.manager.current = 'Profile'
        self.manager.transition.direction = 'down'
        return 0

sm = ScreenManager()

if __name__ == '__main__':
    MainApp().run()