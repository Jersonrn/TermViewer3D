import time
import json
import matplotlib.pyplot as plt
import keyboard
from Vector import Vector3D
from objects import Ankylosaurus, Camera, Cube, Light, Object3D, Plane, Sphere, Torus, Suzanne
from render import Render


def _stop_process():
    global process
    process = False

def _swich():
    global i
    if i == len(objects) - 1:
        i = 0
    else:
        i += 1


def on_key_press(event):
    eval( keys[f"{event.name}"] )


if __name__ == "__main__":
    dona: Torus = Torus(position=Vector3D(0,0,-0),
                        rotation=Vector3D(33,0,0),
                        up=Vector3D(0,0,1),
                        major_res= 60,
                        minor_res= 60,
                        major_radio=1,
                        minor_radio=0.25)

    # cube: Cube = Cube(position=Vector3D(0, 0, 0),
    #                   rotation=Vector3D(),
    #                   up= Vector3D(0, 1, 0),
    #                   size=Vector3D(0.8, 0.8, 0.8),
    #                   res=Vector3D(40, 40, 40))

    # plane: Plane = Plane(position=Vector3D(0, 0, 0),
    #                      rotation=Vector3D(0, 0, 0),
    #                      up=Vector3D(0, 0, 1),
    #                      size=Vector3D(1, 1, 0),
    #                      res=Vector3D(10, 10, 0))

#     suzanne: Suzanne = Suzanne(position=Vector3D(0, 0, 0),
#                                rotation=Vector3D(0, 0, 90),
#                                up=Vector3D(0, 1, 0))

    # sphere: Sphere = Sphere(position=Vector3D(0, 0, 0),
    #                         rotation=Vector3D(0, 0, 90),
    #                         up=Vector3D(0, 1, 0))

    # ankylsaurus: Ankylosaurus = Ankylosaurus(position=Vector3D(0, 0, 0),
    #                         rotation=Vector3D(0, 0, 90),
    #                         up=Vector3D(0, 1, 0))

    light: Light = Light(position=Vector3D(-0.0, 0.0, 3.0),
                         rotation=Vector3D(),
                         up=Vector3D(0,1,0),
                         dir=Vector3D(0.0, -0.0, 1.0),
                         strenght=11.5)

    camera: Camera = Camera(position=Vector3D(0,0,1.5), 
                            rotation=Vector3D(), 
                           up=Vector3D(0,1,0))


    with open("settings/keybindings.json") as file:
        keys = json.load(file)


    objects: list = [dona, light, camera]
    i = 0
    selected: Object3D
    speed = 0.1
    process = True
    last_key_time = time.time()

    while process == True:
        camera.render(meshes=[dona], light=light)
        
        selected = objects[i]
        
        current_time = time.time()
        delta_time = current_time - last_key_time
        if delta_time > 1:
            keyboard.on_press(on_key_press, suppress=True)
            last_key_time = time.time()
        else:
            pass
        
        # time.sleep(0.08333333333333333) #12 fps
        # time.sleep(0.04166666666) #24 fps
        time.sleep(0.01666666666) #60 fps
