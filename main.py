import time
import matplotlib.pyplot as plt
import keyboard
from Vector import Vector3D
from objects import Camera, Cube, Light, Object3D, Torus
from render import Render


def show_3D(vertices):
    limit = 1
    ax = plt.axes(projection="3d")
    ax.scatter(vertices[0],vertices[1],vertices[2])
    # ax.scatter(normales[0],normales[1],normales[2])
    # ax.scatter(light[0],light[1],light[2])
    ax.scatter([-limit,limit],[-limit,limit],[-limit,limit])
    plt.show()

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
    #                   size=Vector3D(1, 1, 1),
    #                   res=Vector3D(20, 20, 20))

    light: Light = Light(position=Vector3D(-0.0, 0.0, 3.0),
                         rotation=Vector3D(),
                         up=Vector3D(0,1,0),
                         dir=Vector3D(0.0, -0.0, 1.0),
                         strenght=11.5)

    camera: Camera = Camera(position=Vector3D(0,0,1.5), 
                            rotation=Vector3D(), 
                           up=Vector3D(0,1,0))

    objects: list = [dona, light, camera]
    i = 0
    selected: Object3D
    speed = 0.1

    # show_3D(cube.vertices)
    while True:
        camera.render(meshes=[dona], light=light)
        
        selected = objects[i]
        
        if keyboard.is_pressed("esc"):
            break
        
        elif keyboard.is_pressed("tab"):
            if i == len(objects) - 1:
                i = 0
            else:
                i += 1
        
        #Move
        elif keyboard.is_pressed("w"):
            selected.set_position(Vector3D(0, 0,-speed))
        elif keyboard.is_pressed("s"):
            selected.set_position(Vector3D(0, 0, speed))
        elif keyboard.is_pressed("d"):
            selected.set_position(Vector3D(0,-speed, 0))
        elif keyboard.is_pressed("a"):
            selected.set_position(Vector3D(0, speed, 0))
        elif keyboard.is_pressed("e"):
            selected.set_position(Vector3D(-speed, 0,0))
        elif keyboard.is_pressed("q"):
            selected.set_position(Vector3D(speed, 0, 0))
        
        #Rotate
        elif keyboard.is_pressed("up"):
            selected.rotate_y(-1)
        elif keyboard.is_pressed("down"):
            selected.rotate_y(1)
        elif keyboard.is_pressed("right"):
            selected.rotate_x(1)
        elif keyboard.is_pressed("left"):
            selected.rotate_x(-1)
        
        # time.sleep(0.04166666666)
        time.sleep(0.01666666666)
