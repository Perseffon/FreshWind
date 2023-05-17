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
from additional_classes import Selfs, Images, red, blue, green, yellow, Labels, Backs, extras
from kivy.config import Config
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
import datetime
import plyer
import sqlite3
import random
from kivy.core.window import Window

Config.set('graphics', 'width', '540')
Config.set('graphics', 'height', '800')
Config.set('graphics', 'resizable', False)
Config.write()
now = datetime.datetime.now()

# создание потоков в доступные бд
con = sqlite3.connect("tutorial.db")
con1 = sqlite3.connect("prof.db")
con2 = sqlite3.connect("date.db")
con3 = sqlite3.connect("progress.db")
con4 = sqlite3.connect("advice.db")
cur = con.cursor()
cur1 = con1.cursor()
cur2 = con2.cursor()
cur3 = con3.cursor()
cur4 = con4.cursor()

# new_column = "ALTER TABLE prof ADD COLUMN soundtype INT"

for row in cur4.execute("""SELECT id,advice from advice"""):
    print(row)
# cur4.execute("""INSERT INTO advice VALUES 3,'Это не у тебя нет девчонки,/nэто ни у одной девчонки нет тебя.')""")

# объявление объектов дополнительных классов
selfs = Selfs()
images = Images()
labels = Labels()
back = Backs()
extra = extras()

# проверка даты

res1 = cur2.execute("SELECT month,day FROM date ")
if res1 is not None:
    month, day = res1.fetchone()
else:
    month = now.month
    day = now.day

if month == now.month and day == now.day:
    print("true")
    res2 = cur3.execute("SELECT value,maxvalue FROM progress ")
    if res2 is not None:
        value, maxvalue = res2.fetchone()
        extras.completenote = value
        extras.countnote = maxvalue
    else:
        data = (1, 1, 1)
        cur3.execute("""
                        INSERT INTO progress VALUES
                            (?,?,?)
                    """, data)
        con3.commit()
        res2 = cur3.execute("SELECT value,maxvalue FROM progress ")
        value, maxvalue = res2.fetchone()
        extras.completenote = value
        extras.countnote = maxvalue
else:
    print("false")
    cur3.execute('UPDATE progress SET value=? WHERE id=?',
                 (0, 1))
    con3.commit()
    res2 = cur3.execute("SELECT value,maxvalue FROM progress ")
    value, maxvalue = res2.fetchone()
    extras.completenote = value
    extras.countnote = 0
    for row in cur.execute("SELECT note FROM notes"):
        # print(row)
        extras.countnote += 1
    cur3.execute('UPDATE progress SET maxvalue=? WHERE id=?',
                 (extras.countnote, 1))
    con3.commit()
    cur2.execute('UPDATE date SET month=?,day=? WHERE id=?',
                 (now.month, now.day, 1))
    con2.commit()
# for row in cur3.execute("SELECT value,maxvalue FROM progress"):
#     print(row)

# восстановление сохраненных настроек пользователя
res = cur1.execute("SELECT name,age,typeback,soundtype FROM prof ")
name, age, typeback, soundtype = res.fetchone()
print("soundtype = " + str(soundtype))
labels.name = name
labels.age = age
back.typeback = typeback
extras.soundtype = soundtype
if back.typeback == "1":
    images.backimg = 'images/back1.png'
elif back.typeback == "2":
    images.backimg = 'images/back2.png'
elif back.typeback == "3":
    images.backimg = 'images/back3.png'
elif back.typeback == "4":
    images.backimg = 'images/back4.jpg'


class CircularProgressBar(ProgressBar):

    def __init__(self, **kwargs):
        super(CircularProgressBar, self).__init__(**kwargs)

        # Set constant for the bar thickness
        self.thickness = 40
        self.max = extras.countnote
        # Create a direct text representation
        self.label = CoreLabel(text="", font_size=self.thickness)

        # Initialise the texture_size variable
        self.texture_size = None

        # Refresh the text
        self.refresh_text()

        selfs.self5 = self
        # Redraw on innit
        self.draw()

    def draw(self):
        with self.canvas:
            self.canvas.clear()
            Color(0.5, 0.5, 0.5)
            Ellipse(pos=self.pos, size=self.size)
            Color(1, 0, 0)

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
        self.value += value
        self.label.text = str(int(self.value_normalized * 100)) + "%"
        self.refresh_text()
        self.draw()


class MainApp(App):
    sm = ScreenManager()
    a = 0

    def build(self):
        self.sm.add_widget(SplashScreen())
        self.sm.add_widget(MainScreen())
        self.sm.add_widget(ProfileScreen())
        self.sm.add_widget(OptionsScreen())
        self.sm.add_widget(NoteScreen())
        Window.bind(on_request_close=self.on_request_close)
        return self.sm

    def on_start(self):
        Clock.schedule_once(self.change_screen, 5)

    def change_screen(self, dt):
        self.sm.current = "Main"

    def on_request_close(self, pp):
        con.close()
        con1.close()
        con2.close()
        con3.close()
        print("closed")


class SplashScreen(Screen):
    def __init__(self):
        super().__init__()

        self.name = 'Splash'

        splash_layout = FloatLayout()
        self.add_widget(splash_layout)
        selfs.self6 = self
        Background = Image(
            source=images.backimg,
            size=(540, 960),
            size_hint=(None, None),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        label = Label(text='Приложение-ежедневник', font_size=40, pos_hint={'center_x': .5, 'center_y': .9},
                      color=(255 / 255, 69 / 255, 0 / 255))
        gif = Image(source='images/test.gif',
                    pos_hint={'center_x': 0.5, 'center_y': 0.2},
                    size_hint=(None, None),
                    size=(130, 130),
                    )
        splash_layout.add_widget(Background)
        splash_layout.add_widget(label)
        splash_layout.add_widget(gif)


class MainScreen(Screen):
    def __init__(self):
        super().__init__()

        self.name = 'Main'

        main_layout = FloatLayout()

        self.add_widget(main_layout)
        Background = Image(
            source=images.backimg,
            size=(540, 960),
            size_hint=(None, None),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        Plank = Image(
            source='images/plank.png',
            size=(540, 200),
            pos_hint={'center_x': 0.5, 'center_y': 0.07},
        )
        Go_advice = Button(
            background_normal="images/advice.png",
            size=(100, 100),
            size_hint=(None, None),
            pos_hint={'center_x': .15, 'center_y': .1}
        )
        Go_advice.bind(on_press=self.advice)
        Go_Screen2 = Button(text='',
                            background_normal="images/button_person.png",
                            size=(100, 100),
                            size_hint=(None, None),
                            pos_hint={'center_x': .85, 'center_y': .1},
                            )
        Go_Note = Button(text='',
                         background_normal="images/+.png",
                         size=(100, 100),
                         size_hint=(None, None),
                         pos_hint={'center_x': .5, 'center_y': .1},
                         )
        box = BoxLayout(orientation='vertical')

        res3 = cur4.execute("SELECT id,advice FROM advice WHERE id = {}".format(extras.rand))
        id, advice = res3.fetchone()
        box.add_widget(Label(text=advice))
        btn_ex = Button(
            size=(380, 40),
            background_normal="images/neutral1-1.png",
            size_hint=(None, None))
        box.add_widget(btn_ex)
        popup = Popup(title="Ваш совет на сегодня",
                      title_size=26,
                      separator_height=7,
                      background='images/popup.jpg',
                      content=box,
                      size=(400, 300),
                      size_hint=(None, None),
                      auto_dismiss=False)
        btn_ex.bind(on_press=popup.dismiss)
        Selfs.popups1 = popup
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        for row in cur.execute("SELECT note FROM notes"):
            lbl = Button(text=str(row)[2:-3],
                         background_normal="images/neutral.png",
                         size=(500, 50),
                         size_hint_y=None,

                         )
            lbl.bind(on_press=self.to_editnote_scrn)
            layout.add_widget(lbl)
        root = ScrollView(size_hint=(1, None),
                          size=(400, 200),
                          pos_hint={'center_x': .5, 'center_y': .3}
                          )
        root.add_widget(layout)
        Go_Screen2.bind(on_press=self.to_second_scrn)
        Go_Note.bind(on_press=self.to_note_scrn)
        selfs.self1 = self
        main_layout.add_widget(Background)
        main_layout.add_widget(Plank)
        main_layout.add_widget(Go_Screen2)
        main_layout.add_widget(Go_Note)
        main_layout.add_widget(root)
        main_layout.add_widget(Go_advice)

    def redraw(self):
        self.__init__()

    def advice(self, *args):
        extras.rand = random.randint(1, extras.countadv)
        self.redraw()
        Selfs.popups1.open()

    def to_second_scrn(self, *args):
        self.manager.current = 'Profile'
        self.manager.transition.direction = 'up'

    def to_note_scrn(self, *args):
        self.manager.current = 'Note'
        self.manager.transition.direction = 'up'

    def to_editnote_scrn(self, instance, *args):
        if extras.soundtype == 0:
            plyer.notification.notify(title='Поздравляем!', message='Вы успешно выполнили еще одну задачу!')
        extras.notetext = instance.text
        cur.execute("DELETE FROM notes WHERE note=(?)", (extras.notetext,))
        con.commit()
        instance.disabled = True
        extras.completenote += 1
        cur3.execute('UPDATE progress SET value=? WHERE id=?',
                     (extras.completenote, 1))
        con3.commit()
        ProfileScreen.redraw(selfs.self2)


class NoteScreen(Screen):
    def __init__(self):
        super().__init__()

        self.name = 'Note'

        note_layout = FloatLayout()

        self.add_widget(note_layout)
        Background = Image(
            source=images.backimg,
            size=(540, 960),
            size_hint=(None, None),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        Go_Back = Button(
            background_normal="images/button_notes.png",
            size=(100, 100),
            size_hint=(None, None),
            pos_hint={'center_x': .1, 'center_y': .1},
        )
        Save_Note = Button(background_normal="images/Save.png",
                           size=(200, 50),
                           size_hint=(None, None),
                           pos_hint={'center_x': .5, 'center_y': .6},
                           )
        textinput = TextInput(text='',
                              multiline=True,
                              pos_hint={'center_x': .5, 'center_y': .8},
                              size_hint=(.7, .3)
                              )

        def on_text(instance, value):
            labels.note = value

        textinput.bind(text=on_text)
        Go_Back.bind(on_press=self.to_main_scrn)
        Save_Note.bind(on_press=self.save_note)
        selfs.self3 = self
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
        extras.countnote += 1
        if labels.note != '':
            cur.execute("""
                INSERT INTO notes VALUES
                    (?)
            """, (labels.note,))
            con.commit()
            MainScreen.redraw(selfs.self1)
        ProfileScreen.redraw(selfs.self2)

        print(str(now.month) + '.' + str(now.day))
        cur2.execute('UPDATE date SET month=?,day=? WHERE id=?',
                     (now.month, now.day, 1))
        con2.commit()

        cur3.execute('UPDATE progress SET maxvalue=? WHERE id=?',
                     (extras.countnote, 1))
        con3.commit()
        for row in cur2.execute("SELECT id,month,day FROM date"):
            print(row)
        labels.note = ''
        self.redraw()
        self.manager.current = 'Main'
        self.manager.transition.direction = 'up'


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
        Go_Back = Button(background_normal="images/button_notes.png",
                         size=(100, 100),
                         size_hint=(None, None),
                         pos_hint={'center_x': .15, 'center_y': .1},
                         )
        Go_Options = Button(text='',
                            background_normal="images/setting.png",
                            size=(100, 100),
                            size_hint=(None, None),
                            pos_hint={'center_x': .85, 'center_y': .1},
                            )
        Name = Label(text="Имя пользователя",
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
        Save = Button(background_normal="images/Saveandchange.png",
                      size=(300, 100),
                      size_hint=(None, None),
                      pos_hint={'center_x': .3, 'center_y': .64},
                      )
        progress = CircularProgressBar(max=extra.countnote,
                                       value=extra.completenote,
                                       pos=(400, 590)
                                       )
        content = Button(
            size=(280, 40),
            background_normal="images/neutral1-2.png",
            size_hint=(None, None)
        )
        popup = Popup(title="Вы неверно ввели возраст",
                      background='images/popup.jpg',
                      content=content,
                      size=(300, 100),
                      size_hint=(None, None),
                      auto_dismiss=False)
        content.bind(on_press=popup.dismiss)
        Selfs.popups = popup
        progress.refresh_text()
        Go_Back.bind(on_press=self.to_main_scrn)
        Go_Options.bind(on_press=self.to_option_scrn)
        Save.bind(on_press=self.save_changes)

        def on_text(instance, value):
            labels.name = value

        def on_text1(instance, value):
            labels.age = value

        Nameinput.bind(text=on_text)
        Ageinput.bind(text=on_text1)

        selfs.self2 = self
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
        if labels.age.isdigit():
            if 99 > int(labels.age) >= 6:
                count = 0
                for row in cur1.execute("SELECT id,name,age,typeback FROM prof"):
                    count += 1
                if count == 0:
                    data = ("1", labels.name, labels.age, back.typeback, extras.soundtype)
                    cur1.execute("""
                    INSERT INTO prof VALUES
                        (?,?,?,?,?)
                    """, data)
                else:
                    cur1.execute('UPDATE prof SET name=?,age=?,typeback=? WHERE id=?',
                                 (labels.name, labels.age, back.typeback, "1"))
                con1.commit()
            else:
                labels.age = ''
                Selfs.popups.open()
                self.redraw()
        else:
            labels.age = ''
            Selfs.popups.open()
            self.redraw()


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
        Go_Back = Button(background_normal="images/back.png",
                         size=(100, 100),
                         size_hint=(None, None),
                         pos_hint={'center_x': .1, 'center_y': .1},
                         color=green)
        Go_Back.bind(on_press=self.to_profile_scrn)
        if extras.soundtype == 1:
            images.soundback = 'images/soundoff.png'
        elif extras.soundtype == 0:
            images.soundback = 'images/soundon.png'
        Sound = Button(background_normal=images.soundback,
                       size=(50, 50),
                       size_hint=(None, None),
                       pos_hint={'center_x': .9, 'center_y': .92},
                       )
        Sound.bind(on_press=self.sound_change)
        label = Label(text='Выберите тему', font_size=32, pos_hint={'center_x': .5, 'center_y': .9})
        Red = Button(background_normal="images/Field2.png",
                     size=(100, 50),
                     size_hint=(None, None),
                     pos_hint={'center_x': .2, 'center_y': .8},
                     color=green)

        Red.bind(on_press=self.choose_red)
        Green = Button(background_normal="images/Castle2.png",
                       size=(100, 50),
                       size_hint=(None, None),
                       pos_hint={'center_x': .4, 'center_y': .8},
                       color=blue)

        Green.bind(on_press=self.choose_green)
        Blue = Button(background_normal="images/Desert2.png",
                      size=(100, 50),
                      size_hint=(None, None),
                      pos_hint={'center_x': .6, 'center_y': .8},
                      color=yellow)

        Blue.bind(on_press=self.choose_blue)
        Yellow = Button(background_normal="images/Sea2.png",
                        size=(100, 50),
                        size_hint=(None, None),
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
        options_layout.add_widget(Sound)

    def redraw(self):
        self.__init__()

    def sound_change(self, *args):
        if extras.soundtype is None:
            extras.soundtype = 0
            print("None")
        else:
            print("Not none")
            if extras.soundtype == 1:
                extras.soundtype = 0
                images.soundback = 'images/soundoff.png'
            elif extras.soundtype == 0:
                extras.soundtype = 1
                images.soundback = 'images/soundon.png'
        cur1.execute('UPDATE prof SET soundtype=? WHERE id=?',
                     (extras.soundtype, "1"))
        con1.commit()
        print(extras.soundtype)
        self.redraw()

    def to_profile_scrn(self, *args):
        self.manager.current = 'Profile'
        self.manager.transition.direction = 'down'
        return 0

    def choose_red(self, *args):
        images.backimg = 'images/back1.png'
        back.typeback = "1"
        OptionsScreen.redraw(self)
        ProfileScreen.redraw(selfs.self2)
        MainScreen.redraw(selfs.self1)
        NoteScreen.redraw(selfs.self3)
        return 0

    def choose_green(self, *args):
        images.backimg = 'images/back2.png'
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
