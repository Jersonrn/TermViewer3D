import numpy as np
from numpy._typing import NDArray
import cupy as cp 
from cupy import ndarray


class Vector3D:
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0 ) -> None:
        self.x, self.y, self.z = (x, y, z)

    def __repr__(self) -> str:
        return f"Vector3D(x: {self.x}, y: {self.y}, z: {self.z})"

    def __add__(self,v:"Vector3D") -> "Vector3D":
        return Vector3D(self.x + v.x, self.y + v.y, self.z + v.z)

    def Vector3D2Array3D(self) -> NDArray:
        return np.array([self.x, self.y, self.z])

    def Vector3D2Array4D(self) -> NDArray:
        return np.array([self.x, self.y, self.z, 1])

    def cpVector3D2Array4D(self) -> ndarray:
        return cp.asarray([self.x, self.y, self.z, 1])

    def dot(self, v: "Vector3D") -> float:
        return np.dot(self.Vector3D2Array3D(), v.Vector3D2Array3D())

    def cross(self, v: "Vector3D") -> "Vector3D":
        return Vector3D(*np.cross(self.Vector3D2Array3D(),v.Vector3D2Array3D()))

    def clamp(self, vmin: float = 0.0, vmax: float = 1.0) -> None:
        self.x, self.y, self.z = np.clip([self.x, self.y, self.z], vmin, vmax)

    def magnitude(self):
        # return np.linalg.norm(self.Vector3D2Array())
        v: NDArray = self.Vector3D2Array3D()
        return np.sqrt(v.dot(v))

    def normalize(self) -> None:
        magnitude: float = self.magnitude()
        self.x /= float(magnitude)
        self.y /= float(magnitude)
        self.z /= float(magnitude)

