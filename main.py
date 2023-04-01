from Vector import Vector3D
from objects import Torus

if __name__ == "__main__":
    dona: Torus = Torus(position=Vector3D(0,0,-4),
                        rotation=Vector3D(),
                        up=Vector3D(0,0,1),
                        major_res=30,
                        minor_res=30,
                        major_radio=1,
                        minor_radio=0.55)

