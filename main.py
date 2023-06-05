from ursina import *
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




from ursina.shaders import lit_with_shadows_shader
Entity.default_shader = lit_with_shadows_shader
DirectionalLight().look_at(Vec3(1,-1,-1))

ground = Entity(model='plane', scale=32, texture='white_cube', texture_scale=Vec2(32), collider='box')

from ursina.prefabs.first_person_controller import FirstPersonController
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

skybox_image = load_texture("black.png")
Sky(texture=skybox_image)

app.run()


