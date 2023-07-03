from imports.UE import *
print("STARTING")
from direct.stdpy import thread
import threading
from playsound import playsound
import time
print("Finished Imports")

app = Ursina(size=(1280,720))
app.loaded = False

field = InputField(name='name_field')
button2 = Button(text='Submit', color=color.azure)


def play():
    print("PLAYING")
    print(field.text)
button2.on_click = play
descr="hi"
test = Text(text=descr, wordwrap=30)
icon = Text()
icon.images = ["Evanescent-Clear.png"]

wp = WindowPanel(
        title='Custom Window',
        content=(
            Text('Name:'),
            field,
            button2,
            Slider(),
            Slider(),
            ButtonGroup(('test', 'eslk', 'skffk'))
            ),
        )

wp.y = wp.panel.scale_y / 2 * wp.scale_y

icon.y = wp.panel.scale_y / 2 * wp.scale_y

app.run()