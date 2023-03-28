from numba import jit
from numba import float64    # import the types
from numba.experimental import jitclass
import numpy as np

spec = [
    ('x', float64),
    ('y', float64),
    ('z', float64)
]

@jitclass(spec)
class Vector3D:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x, self.y, self.z = x, y, z

    def Vector3D2Array(self):
        return np.array([self.x, self.y, self.z])

    @jit
    def magnitude(self):
        # v = self.Vector3D2Array()
        # return np.sqrt(v.dot(v))
        return np.sqrt(self.x**2 + self.y**2 + self.z**2)

v = Vector3D(3, 7, 4)
print(v.magnitude())

