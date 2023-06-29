
from imports.UE import *

from direct.stdpy import thread
import threading
from playsound import playsound
import time

GameRunning = True
app = Ursina(size=(1280,720))
app.loaded = False
editor_camera = EditorCamera(enabled=False, ignore_paused=True)
physics_entities = []
class PhysicsEntity(Entity):
    def __init__(self, model='cube', collider='box', **kwargs):
        super().__init__(model=model, collider=collider, **kwargs)
        physics_entities.append(self)

    def update(self):
        if self.intersects():
            self.stop()
            return

        self.velocity = lerp(self.velocity, Vec3(0), time.dt)
        self.velocity += Vec3(0,-1,0) * time.dt * 5
        self.position += (self.velocity + Vec3(0,-4,0)) * time.dt


    def stop(self):
        self.velocity = Vec3(0,0,0)
        if self in physics_entities:
            physics_entities.remove(self)

    def on_destroy(self):
        self.stop()


    def throw(self, direction, force):
        pass



class Panel(Entity):

    def __init__(self, **kwargs):
        super().__init__()
        self.parent = camera.ui
        self.model = Quad()
        self.color = Button.color

        for key, value in kwargs.items():
            setattr(self, key, value)



from imports.UE.shaders import lit_with_shadows_shader
Entity.default_shader = lit_with_shadows_shader
DirectionalLight().look_at(Vec3(1,-1,-1))

ground = Entity(model='plane', scale=32, texture='white_cube', texture_scale=Vec2(32), collider='box')

from imports.UE.prefabs.first_person_controller import FirstPersonController
player = FirstPersonController()


def pause_input(key):
    if key == 'tab':    # press tab to toggle edit/play mode
        editor_camera.enabled = not editor_camera.enabled

        player.visible_self = editor_camera.enabled
        player.cursor.enabled = not editor_camera.enabled
        mouse.locked = not editor_camera.enabled
        editor_camera.position = player.position

        application.paused = editor_camera.enabled

pause_handler = Entity(ignore_paused=True, input=pause_input)

HeaderText = Text(f'''''', origin=(0,-13), color=color.white, font='Orbitron-Bold.ttf')
MessageText = Text(f'''''', origin=(0,-15), color=color.white, font='Orbitron-Bold.ttf')

def AlertFunction():
    while True:
        if GameRunning == True:
            time.sleep(0.1)
            for alert in alerts:
                if alert["Sound"] == True:
                    playsound('alert_sound.wav') 

def NoticeText():
    while True:
        if GameRunning == True:
            time.sleep(0.1)
            try:
                if len(alerts) >=1:
                    Header = alerts[0]["Title"]
                    Message = alerts[0]["Detail"]
                    HeaderText.text =f'''{Header}'''
                    MessageText.text = f'''{Message}'''
                    HeaderText.enabled = True
                    MessageText.enabled = True
                else:
                    HeaderText.enabled = False
                    MessageText.enabled = False
            except:
                HeaderText.enabled = False
                MessageText.enabled = False
                pass



#BEGINNING SEQUENCE#

#Setup some components which will be necessary throughout the game#

#Achievement Setup#
uachievements = [{"Title":"Plutonium","Content":"You found plutonium","XP":43},{"Title":"Transmitter","Content":"Contact home? Or not...","XP":12},{"Title":"Mining","Content":"Some would say you have a miner problem.","XP":8},{"Title":"Showers","Content":"Houston is lost, get cover behind an object","XP":58},{"Title":"Oxygen","Content":"A discarded tank is found laying in the wastes","XP":73},{"Title":"Gills","Content":"Survived a whole minute with a leak in your suit","XP":51}]
achievements = []
achievement_thread_dictionary = {"Occurance":"","Quantity":"","":""}

def achievement_handler(title):
    print(title)
    for achievement in achievements:
        if achievement["Title"] == title:
            return
        else:
            pass

    for achievement in uachievements:
        if achievement["Title"] == title:
            achievements.append(achievement)
            return


achievement_management_thread = threading.Thread(target=achievement_handler, args=())

#Active Alerts List#
alerts = []
#Begin threads for background components#
alertThread = threading.Thread(target=AlertFunction,).start()
noticeThread = threading.Thread(target=NoticeText,).start()


#Defines the Parent of the UI
menu_parent = Entity(parent=camera.ui, y=.15)
#Sets the helmet image as the background of the UI
background = Entity(parent=menu_parent, model='quad', texture='helmet', scale=(1.9,1.9), color=color.white, z=1, world_y=0)



camera.overlay.color = color.black
logo = Sprite(name='Boot Logo', parent=camera.ui, texture='Evanescent-Clear', world_z=camera.overlay.z-1, scale=.1, color=color.clear)
logo.animate_color(color.white, duration=12, delay=1, curve=curve.out_quint_boomerang)
camera.overlay.animate_color(color.clear, duration=1, delay=4)
destroy(logo, delay=5)

def splash_input(key):
    destroy(logo)
    camera.overlay.animate_color(color.clear, duration=.25)

logo.input = splash_input



#### READY TO TAKE INPUT FOR FUNCTIONS OF THE GAME ###

#Step 1 of game - play beeping sound and provide an alert telling the player they are running out of O2#

alerts.append({
    "Title":"OXYGEN",
    "Detail":"35% Oxygen Remaining",
    "Sound":True
    })

print(alerts)



class ExitButton(Button):
    def __init__(self, **kwargs):
        super().__init__(
            name = 'exit_button',
            eternal = True,
            origin = (.5, .5),
            # text_origin = (-.5,-.5),
            position = window.top_right,
            z = -999,
            scale = (.05, .025),
            color = color.red.tint(-.2),
            text = 'x',
            **kwargs)


    def on_click(self):
        print("CALLED QUIT")
        global GameRunning
        GameRunning = False
        application.quit()


#Create objects to find#

plutonium = Button(parent=scene, model='cube', color=color.brown, position=(6,5,5))
plutonium.on_click = Func(achievement_handler, plutonium.position, duration=.5, curve=curve.linear)

enter = TextField(max_lines=2, line_height=5, x=-.89, y=-.45)

##

def input(key):
    if key == 'right mouse down':
        
        box1 = Button(parent=scene, model='cube', color=color.brown, position=(4,5,5))
        box1.on_click = Func(player.animate_position, box1.position, duration=.5, curve=curve.linear)

    if key == 'left mouse down':
        
        e = PhysicsEntity(model='cube', color=color.azure, velocity=Vec3(0), position=player.position+Vec3(0,1.5,0)+player.forward, collider='sphere')
        e.velocity = (camera.forward + Vec3(0,.5,0)) * 10
        
        # physics_entities.append(e)

    if key == "j":
        print("User provided an Acknowledge signal to an active alert")
        try:
            alerts.pop()
            print("Dismissed alert.")
        except:
            print("No alert to dismiss")
            pass



sun = DirectionalLight()
sun.look_at(Vec3(1,-1,-1))

#ui2 = Panel(parent.ui)
skybox_image = load_texture("black.png")
Sky(texture=skybox_image)
window.exit_button.enabled = False
quitter = ExitButton()
app.run()




class InputField(Button):
    def __init__(self, default_value='', label='', max_lines=1, character_limit=24, **kwargs):
        super().__init__(scale=(.5, Text.size*2*max_lines), highlight_scale=1, pressed_scale=1, highlight_color=color.black, **kwargs)

        for key, value in kwargs.items():
            if 'scale' in key:
                setattr(self, key, value)
#
        self.default_value = default_value
        self.limit_content_to = None
        self.hide_content = False   # if set to True, will display content as '*'. can also be set to character instead of True.

        self.next_field = None
        self.submit_on = None   # for example: self.submit_on = 'enter' will call self.on_submit when you press enter.
        self.on_submit = None   # function to be called when you press self.submit_on.
        self.on_value_changed = None

        self.text_field = TextField(world_parent = self, x=-.45, y=.3, z=-.1, max_lines=max_lines, character_limit=character_limit, register_mouse_input = True)
        destroy(self.text_field.bg)
        self.text_field.bg = self

        def render():
            if self.limit_content_to:
                org_length = len(self.text_field.text)
                self.text_field.text = ''.join([e for e in self.text_field.text if e in self.limit_content_to])
                self.text_field.cursor.x -= org_length - len(self.text_field.text)
                self.text_field.cursor.x = max(0, self.text_field.cursor.x)

            if self.hide_content:
                replacement_char = '*'
                if isinstance(self.hide_content, str):
                    replacement_char = self.hide_content

                self.text_field.text_entity.text = replacement_char * len(self.text_field.text)
                return

            if self.on_value_changed and not self.text_field.text_entity.text == self.text_field.text:
                self.on_value_changed()
            self.text_field.text_entity.text = self.text_field.text

        self.text_field.render = render

        self.text_field.scale *= 1.25
        self.text_field.text = default_value
        self.text_field.render()
        self.text_field.shortcuts['indent'] = ('')
        self.text_field.shortcuts['dedent'] = ('')

        self.active = False

        if label:
            self.label = Text(str(label) + ':', parent = self, position = self.text_field.position, scale = 1.25)
            self.text_field.x += 0.1 * (len(str(label)) + 1.0) / 6.0


        for key, value in kwargs.items():
            setattr(self, key, value)

    def input(self, key):
        if key == 'tab' and self.text_field.cursor.y >= self.text_field.max_lines-1 and self.active:
            self.active = False
            if self.next_field:
                mouse.position = self.next_field.get_position(relative_to=camera.ui)
                invoke(setattr, self.next_field, 'active', True, delay=.01)

        if self.active and self.submit_on and key == self.submit_on and self.on_submit:
            self.on_submit()
            self.active = False

    @property
    def text(self):
        return self.text_field.text

    @text.setter
    def text(self, value):
        self.text_field.text = ''
        self.text_field.cursor.position = (0,0)
        self.text_field.add_text(value, move_cursor=True)
        self.text_field.render()

    @property
    def text_color(self):
        return self.text_field.text_entity.color

    @text_color.setter
    def text_color(self, value):
        self.text_field.text_entity.color = value


    @property
    def active(self):
        return self.text_field.active

    @active.setter
    def active(self, value):
        self.text_field.active = value
        # if value == True:
        #     # self.text_field.select_all()
        #     invoke(self.text_field.select_all, delay=.1)
        #     # self.text_field.input(' ')
        #     # self.text_field.erase()

   