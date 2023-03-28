import numpy as np
from numpy._typing import NDArray
from Vector import Vector3D

class Object3D:
    def __init__(self,
                 position: Vector3D = Vector3D(),
                 rotation: Vector3D = Vector3D(),
                 up: Vector3D = Vector3D(0, 1, 0)) -> None:
        
        self.position: Vector3D = position
        self.rotation: Vector3D = rotation
        self.up: Vector3D = up
        self.matrix: NDArray = np.array([
            [1.0000, 0.0000, 0.0000, 0.0000],
            [0.0000, 1.0000, 0.0000, 0.0000],
            [0.0000, 0.0000, 1.0000, 0.0000],
            [0.0000, 0.0000, 0.0000, 1.0000],
            ])
        
        self.__set_defaults(self.position, self.rotation)

    def set_position(self, pos: Vector3D):
        Pm: NDArray = np.array([
            [1.0000,0.0000,0.0000,pos.x],
            [0.0000,1.0000,0.0000,pos.y],
            [0.0000,0.0000,1.0000,pos.z],
            [0.0000,0.0000,0.0000,1.000],
            ])
        
        self.matrix = np.dot(Pm,self.matrix)

    def rotate_x(self, angle) -> None:
        angle = np.deg2rad(angle)
        Rx: NDArray = np.array([
            [1.0000, 0.00000000000, 0.000000000000, 0.0000],
            [0.0000, np.cos(angle), -np.sin(angle), 0.0000],
            [0.0000, np.sin(angle),  np.cos(angle), 0.0000],
            [0.0000, 0.00000000000, 0.000000000000, 1.0000],
            ])
        
        self.matrix = np.dot(Rx,self.matrix)
    
    def rotate_y(self, angle) -> None:
        angle = np.deg2rad(angle)
        Ry: NDArray = np.array([
            [ np.cos(angle), 0.0000, np.sin(angle), 0.0000],
            [0.000000000000, 1.0000, 0.00000000000, 0.0000],
            [-np.sin(angle), 0.0000, np.cos(angle), 0.0000],
            [0.000000000000, 0.0000, 0.00000000000, 1.0000],
            ])
        
        self.matrix = np.dot(Ry,self.matrix)

    def rotate_z(self, angle) -> None:
        angle = np.deg2rad(angle)
        Rz: NDArray = np.array([
            [np.cos(angle),-np.sin(angle), 0.0000, 0.0000],
            [np.sin(angle), np.cos(angle), 0.0000, 0.0000],
            [0.00000000000, 0.00000000000, 1.0000, 0.0000],
            [0.00000000000, 0.00000000000, 0.0000, 1.0000],
            ])
        
        self.matrix = np.dot(Rz,self.matrix)

    def __set_defaults(self, position, rotation) -> None:
        self.set_position(position)
        self.rotate_x(rotation.x)
        self.rotate_y(rotation.y)
        self.rotate_z(rotation.z)


class Torus(Object3D):
    def __init__(self,
                 position: Vector3D = Vector3D(),
                 up: Vector3D = Vector3D(0, 1, 0),
                 major_res: int = 10,
                 minor_res: int = 10,
                 major_radio: float = 10,
                 minor_radio: float = 3) -> None:
        super().__init__(position, up)
        self.major_res: int = major_res
        self.minor_res: int  = minor_res
        self.major_radio: float = major_radio
        self.minor_radio: float = minor_radio
        self.vertices: NDArray
        self.normales: NDArray
        self.update_mesh(self.minor_res, self.major_res,
                         self.minor_radio, self.major_radio)

    def update_mesh(self, minor_res: int, major_res: int,
                    minor_radio: float, major_radio: float) -> None:
        i: NDArray = np.linspace(start=0, stop=360, num=minor_res, endpoint=False)
        j: NDArray = np.linspace(start=0, stop=360, num=major_res, endpoint=False)
        alpha,phi = np.meshgrid(i,j)
        
        vertices: NDArray = np.array([
            [(major_radio + minor_radio * np.cos(np.deg2rad(alpha))) * np.cos(np.deg2rad(phi))],
            [minor_radio * np.cos(np.deg2rad(alpha))],
            [(major_radio + minor_radio * np.cos(np.deg2rad(alpha))) * -np.sin(np.deg2rad(phi))]
            ]).reshape(3,-1)
        
        normales: NDArray = np.array([
            [(minor_radio * np.cos(np.deg2rad(alpha))) * np.cos(np.deg2rad(phi))],
            [minor_radio * np.cos(np.deg2rad(alpha))],
            [(minor_radio * np.cos(np.deg2rad(alpha))) * -np.sin(np.deg2rad(phi))]
            ]).reshape(3,-1)
        
        self.vertices: NDArray = vertices
        self.normales: NDArray = normales


dona: Torus = Torus(Vector3D(2,3,1))
print(dona.matrix)
# dona.rotate_x(90)

