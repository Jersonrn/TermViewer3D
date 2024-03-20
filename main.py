import time
from src.objects import *
from src.vector import Vector3D
from src.outliner import Outliner


MAX_FPS = 60
process = True


def main():
    dona: Torus = Torus(
            position=Vector3D(0.16,0,-0),
            rotation=Vector3D(33,0,0),
            up=Vector3D(0,0,1),
            major_res= 80,
            minor_res= 80,
            major_radio=1,
            minor_radio=0.25
    )

    light: Light = Light(
            position=Vector3D(-0.0, 0.0, 3.0),
            rotation=Vector3D(),
            up=Vector3D(0,1,0),
            dir=Vector3D(0.0, -0.0, 1.0),
            strenght=11.5
    )

    camera: Camera = Camera(
            position=Vector3D(0,0,1.5), 
            rotation=Vector3D(), 
            up=Vector3D(0,1,0)
    )

    outliner: Outliner = Outliner(
            mesh_objects=[dona],
            light=light,
            camera=camera
            )


    while process:
        outliner.selected.rotate_x(1)
        outliner.selected.rotate_y(0.5)

        outliner.render()

        time.sleep(1/MAX_FPS)



if __name__ == "__main__":
    main()
