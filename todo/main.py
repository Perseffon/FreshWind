from kivy.graphics import Color, Ellipse, Rectangle
from kivy.uix.progressbar import ProgressBar
from kivy.core.text import Label as CoreLabel
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from additional_classes import Selfs,Images, red, blue, green,yellow,Labels,Backs,extras
from kivy.config import Config
from kivy.clock import Clock
import plyer
import sqlite3
import os

Config.set('graphics', 'width', '540')
Config.set('graphics', 'height', '800')
Config.set('graphics', 'resizable', False)
Config.write()

con=sqlite3.connect("tutorial.db")
cur = con.cursor()
# cur.execute("""
#     INSERT INTO notes VALUES
#         (?)
# """,(data,))
# con.commit()
for row in cur.execute("SELECT note FROM notes"):
    print(row)
    extras.countnote+=1
print("count="+str(extras.countnote))
# data='test'
# cur.execute("DELETE FROM notes WHERE note=(?)",(data,))
# con.commit()
# print("----------------------------------------------")
# for row in cur.execute("SELECT note FROM notes"):
#     print(row)
# con.close()
selfs = Selfs()
images = Images()
labels = Labels()
back=Backs()
extra=extras()
f=open('profile.txt','r')
labels.name=f.readline()
labels.age=f.readline()
back.typeback=f.readline()
if (back.typeback=="1"):
    images.backimg='images/back1.png'
elif(back.typeback=="2"):
    images.backimg = 'images/back2.png'
elif (back.typeback == "3"):
    images.backimg = 'images/back3.png'
elif(back.typeback=="4"):
    images.backimg = 'images/back4.jpg'

f.close()

class CircularProgressBar(ProgressBar):

    def __init__(self, **kwargs):
        super(CircularProgressBar, self).__init__(**kwargs)

        # Set constant for the bar thickness
        self.thickness = 40

        # Create a direct text representation
        self.label = CoreLabel(text="", font_size=self.thickness)

        # Initialise the texture_size variable
        self.texture_size = None

        # Refresh the text
        self.refresh_text()


        selfs.self5=self
        # Redraw on innit
        self.draw()

    def draw(self):
        with self.canvas:
            self.canvas.clear()
            Color(0.26, 0.26, 0.26)
            Ellipse(pos=self.pos, size=self.size)
            Color(0.5, 0, 0.5)
            Ellipse(pos=self.pos, size=self.size,
                    angle_end=(0.001 if self.value_normalized == 0 else self.value_normalized * 360))
            Color(0, 0, 0)
            Ellipse(pos=(self.pos[0] + self.thickness / 2, self.pos[1] + self.thickness / 2),
                    size=(self.size[0] - self.thickness, self.size[1] - self.thickness))
            Color(1, 1, 1, 1)
            Rectangle(texture=self.label.texture, size=self.texture_size,
                      pos=(self.size[0] / 2 - self.texture_size[0] / 2 + self.pos[0],
                           self.size[1] / 2 - self.texture_size[1] / 2 + self.pos[1]))

    def refresh_text(self):
        self.label.refresh()
        self.texture_size = list(self.label.texture.size)

    def set_value(self, value):
        self.value = value
        self.label.text = str(int(self.value_normalized * 100)) + "%"
        self.refresh_text()
        self.draw()


class MainApp(App):
    global sm
    sm = ScreenManager()
    a=0
    def build(self):
        sm.add_widget(SplashScreen())
        sm.add_widget(MainScreen())
        sm.add_widget(ProfileScreen())
        sm.add_widget(OptionsScreen())
        sm.add_widget(NoteScreen())
        return sm

    def on_start(self):
        Clock.schedule_once(self.change_screen,1)
    def change_screen(self, dt):
        sm.current="Main"

class SplashScreen(Screen):
    def __init__(self):
        super().__init__()

        self.name = 'Splash'

        splash_layout = FloatLayout()

        self.add_widget(splash_layout)
        gif = Image(source='images/test.gif',
                    pos_hint={'center_x': 0.5, 'center_y': 0.2},
                    size_hint=(None,None),
                    size=(130, 130),
                    )
        splash_layout.add_widget(gif)

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
            source='images/plank.png',
            size=(540,200),
            pos_hint={'center_x': 0.5, 'center_y': 0.07},
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
        for row in cur.execute("SELECT note FROM notes"):
            print(row)
            lbl = Button(text=str(row)[2:-3],
                            size_hint_y=None,
                            height=50,
                            color=red)
            lbl.bind(on_press=self.to_editnote_scrn)
            layout.add_widget(lbl)
        root = ScrollView(size_hint=(1, None),
                          size=(400, 200),
                          pos_hint = {'center_x': .5, 'center_y': .3}
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
    def to_editnote_scrn(self,instance, *args):
        plyer.notification.notify(title='test',message='hi user')
        extras.notetext = instance.text
        print(extras.notetext)
        cur.execute("DELETE FROM notes WHERE note=(?)", (extras.notetext,))
        con.commit()
        instance.disabled=True
        extras.completenote+=1
        ProfileScreen.redraw(selfs.self2)

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

        def on_text(instance, value):
            labels.note = value
        textinput.bind(text=on_text)
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
        print(labels.note)
        if(labels.note!='') :
            cur.execute("""
                INSERT INTO notes VALUES
                    (?)
            """,(labels.note,))
            con.commit()
            MainScreen.redraw(selfs.self1)

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
        Name=Label(text="Имя пользователя",
                   font_size=32,
                   pos_hint={'center_x': .3, 'center_y': .9},
                   color=(0 / 255, 0 / 255, 0 / 255)
                   )
        Nameinput = TextInput(text=labels.name,
                              multiline=False,
                              pos_hint={'center_x': .3, 'center_y': .85},
                              size_hint=(.5, .05)
                              )
        Age = Label(text="Возраст",
                     font_size=32,
                     pos_hint={'center_x': .3, 'center_y': .8},
                     color=(0 / 255, 0 / 255, 0 / 255)
                     )
        Ageinput = TextInput(text=labels.age,
                              multiline=False,
                              pos_hint={'center_x': .3, 'center_y': .75},
                              size_hint=(.5, .05)
                              )
        Save = Button(text='Изменить и Сохранить',
                            size=(200, 50),
                            size_hint=(None, None),
                            pos_hint={'center_x': .3, 'center_y': .68},
                            )
        progress=CircularProgressBar(max=extra.countnote,
                                     value=extra.completenote,
                                     pos=(400,590)
                                    )
        progress.refresh_text()
        Go_Back.bind(on_press=self.to_main_scrn)
        Go_Options.bind(on_press=self.to_option_scrn)
        Save.bind(on_press=self.save_changes)
        def on_text(instance, value):
            labels.name=value

        def on_text1(instance, value):
            labels.age = value
        Nameinput.bind(text=on_text)
        Ageinput.bind(text=on_text1)

        selfs.self2=self
        second_layout.add_widget(Background)
        second_layout.add_widget(Go_Back)
        second_layout.add_widget(Go_Options)
        second_layout.add_widget(Name)
        second_layout.add_widget(Nameinput)
        second_layout.add_widget(Age)
        second_layout.add_widget(Ageinput)
        second_layout.add_widget(Save)
        second_layout.add_widget(progress)
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
    def save_changes(self, *args):
        print("saved")
        if os.path.isfile('profile.txt'):
            os.remove('profile.txt')
        file = open('profile.txt','w+')
        print(labels.name)
        print(labels.age)
        file.write(labels.name)
        file.write(labels.age)
        file.write(back.typeback)
        file.close()


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
        back.typeback="1"
        OptionsScreen.redraw(self)
        ProfileScreen.redraw(selfs.self2)
        MainScreen.redraw(selfs.self1)
        NoteScreen.redraw(selfs.self3)
        return 0

    def choose_green(self, *args):
        images.backimg='images/back2.png'
        back.typeback = "2"
        OptionsScreen.redraw(self)
        ProfileScreen.redraw(selfs.self2)
        MainScreen.redraw(selfs.self1)
        NoteScreen.redraw(selfs.self3)
        return 0

    def choose_blue(self, *args):
        images.backimg = 'images/back3.png'
        back.typeback = "3"
        OptionsScreen.redraw(self)
        ProfileScreen.redraw(selfs.self2)
        MainScreen.redraw(selfs.self1)
        NoteScreen.redraw(selfs.self3)
        return 0

    def choose_yellow(self, *args):
        images.backimg = 'images/back4.jpg'
        back.typeback = "4"
        OptionsScreen.redraw(self)
        ProfileScreen.redraw(selfs.self2)
        MainScreen.redraw(selfs.self1)
        NoteScreen.redraw(selfs.self3)
        return 0


if __name__ == '__main__':
    MainApp().run()
con.close()