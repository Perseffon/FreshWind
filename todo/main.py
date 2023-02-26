from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.base import runTouchApp
from additional_classes import Selfs,Images, red, blue, green,yellow
from kivy.config import Config

Config.set('graphics', 'width', '540')
Config.set('graphics', 'height', '960')
Config.set('graphics', 'resizable', True)
Config.write()

selfs = Selfs()
images = Images()

class MainApp(App):
    def build(self):
        sm.add_widget(MainScreen())
        sm.add_widget(ProfileScreen())
        sm.add_widget(OptionsScreen())
        sm.add_widget(NoteScreen())
        return sm

class MainScreen(Screen):
    def __init__(self):
        super().__init__()

        self.name = 'Main'

        main_layout = FloatLayout()

        self.add_widget(main_layout)
        Background = Image(
            source=images.backimg,
            size=(540,960),
            size_hint=(None, None),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        Plank = Image(
            source='images/1.jpg',
            pos_hint={'center_x': 0.5, 'center_y': 0},
        )
        Go_Screen2 = Button(text='',
                            background_normal="images/test1.png",
                            size=(100, 100),
                            size_hint=(None, None),
                            pos_hint={'center_x': .9, 'center_y': .1},
                            )
        Go_Note = Button(text='',
                            background_normal="images/test1.png",
                            size=(100, 100),
                            size_hint=(None, None),
                            pos_hint={'center_x': .5, 'center_y': .1},
                            )
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        for i in range(6):
            lbl = Button(text=str(i),
                        size_hint_y=None,
                        height=50,
                        color=red)
            layout.add_widget(lbl)
        root = ScrollView(size_hint=(1, None),
                          size=(400, 300),
                          pos_hint = {'center_x': .5, 'center_y': .35}
                          )
        root.add_widget(layout)
        Go_Screen2.bind(on_press=self.to_second_scrn)
        Go_Note.bind(on_press=self.to_note_scrn)
        selfs.self1=self
        main_layout.add_widget(Background)
        main_layout.add_widget(Plank)
        main_layout.add_widget(Go_Screen2)
        main_layout.add_widget(Go_Note)
        main_layout.add_widget(root)
    def redraw(self):
        self.__init__()
    def to_second_scrn(self, *args):
        self.manager.current = 'Profile'
        self.manager.transition.direction = 'up'
    def to_note_scrn(self, *args):
        self.manager.current = 'Note'
        self.manager.transition.direction = 'up'


class NoteScreen(Screen):
    def __init__(self):
        super().__init__()

        self.name = 'Note'

        note_layout = FloatLayout()

        self.add_widget(note_layout)
        Background = Image(
            source=images.backimg,
            size=(540,960),
            size_hint=(None, None),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        Go_Back = Button(text='Back',
                         size_hint=(.1, .05),
                         pos_hint={'center_x': .1, 'center_y': .1},
                         )
        Save_Note = Button(text='Save',
                         size_hint=(.7, .05),
                         pos_hint={'center_x': .5, 'center_y': .6},
                         )
        textinput = TextInput(text='Hello world',
                              multiline=True,
                              pos_hint = {'center_x': .5, 'center_y': .8},
                              size_hint = (.7, .3)
                        )

        Go_Back.bind(on_press=self.to_main_scrn)
        Save_Note.bind(on_press=self.save_note)
        selfs.self3=self
        note_layout.add_widget(Background)
        note_layout.add_widget(Go_Back)
        note_layout.add_widget(textinput)
        note_layout.add_widget(Save_Note)

    def redraw(self):
        self.__init__()
    def to_main_scrn(self, *args):
        self.manager.current = 'Main'
        self.manager.transition.direction = 'up'
    def save_note(self, *args):
        print("note succesfully saved!")


class ProfileScreen(Screen):
    def __init__(self):
        super().__init__()
        self.name = 'Profile'
        second_layout = FloatLayout()
        self.add_widget(second_layout)
        Background = Image(
            source=images.backimg,
            size=(540, 960),
            size_hint=(None, None),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        # Button
        Go_Back = Button(text='Back',
                         size_hint=(.1, .05),
                         pos_hint={'center_x': .1, 'center_y': .1},
                         )
        Go_Options = Button(text='',
                            background_normal="images/test1.png",
                            size=(100, 100),
                            size_hint=(None, None),
                            pos_hint={'center_x': .3, 'center_y': .1},
                            )
        Go_Back.bind(on_press=self.to_main_scrn)
        Go_Options.bind(on_press=self.to_option_scrn)
        selfs.self2=self
        second_layout.add_widget(Background)
        second_layout.add_widget(Go_Back)
        second_layout.add_widget(Go_Options)

    def redraw(self):
        self.__init__()
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
        Background = Image(
            source=images.backimg,
            size=(540, 960),
            size_hint=(None, None),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        # Button
        Go_Back = Button(text='Back',
                         size_hint=(.1, .05),
                         pos_hint={'center_x': .1, 'center_y': .1},
                         color=green)

        Go_Back.bind(on_press=self.to_profile_scrn)
        label = Label(text='Choose', font_size=32, pos_hint={'center_x': .5, 'center_y': .9})
        Red = Button(text='Green',
                     size_hint=(.1, .05),
                     pos_hint={'center_x': .2, 'center_y': .8},
                     color=green)

        Red.bind(on_press=self.choose_red)
        Green = Button(text='Blue',
                       size_hint=(.1, .05),
                       pos_hint={'center_x': .4, 'center_y': .8},
                       color=blue)

        Green.bind(on_press=self.choose_green)
        Blue = Button(text='Yellow',
                      size_hint=(.1, .05),
                      pos_hint={'center_x': .6, 'center_y': .8},
                      color=yellow)

        Blue.bind(on_press=self.choose_blue)
        Yellow = Button(text='Red',
                        size_hint=(.1, .05),
                        pos_hint={'center_x': .8, 'center_y': .8},
                        color=red)

        Yellow.bind(on_press=self.choose_yellow)
        options_layout.add_widget(Background)
        options_layout.add_widget(Go_Back)
        options_layout.add_widget(label)
        options_layout.add_widget(Red)
        options_layout.add_widget(Green)
        options_layout.add_widget(Blue)
        options_layout.add_widget(Yellow)
    def redraw(self):
        self.__init__()
    def to_profile_scrn(self, *args):
        self.manager.current = 'Profile'
        self.manager.transition.direction = 'down'
        return 0

    def choose_red(self, *args):
        images.backimg='images/back1.png'
        OptionsScreen.redraw(self)
        ProfileScreen.redraw(selfs.self2)
        MainScreen.redraw(selfs.self1)
        NoteScreen.redraw(selfs.self3)
        return 0

    def choose_green(self, *args):
        images.backimg='images/back2.png'
        OptionsScreen.redraw(self)
        ProfileScreen.redraw(selfs.self2)
        MainScreen.redraw(selfs.self1)
        NoteScreen.redraw(selfs.self3)
        return 0

    def choose_blue(self, *args):
        images.backimg = 'images/back3.png'
        OptionsScreen.redraw(self)
        ProfileScreen.redraw(selfs.self2)
        MainScreen.redraw(selfs.self1)
        NoteScreen.redraw(selfs.self3)
        return 0

    def choose_yellow(self, *args):
        images.backimg = 'images/back4.jpg'
        OptionsScreen.redraw(self)
        ProfileScreen.redraw(selfs.self2)
        MainScreen.redraw(selfs.self1)
        NoteScreen.redraw(selfs.self3)
        return 0


sm = ScreenManager()

if __name__ == '__main__':
    MainApp().run()