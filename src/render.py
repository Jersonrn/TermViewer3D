import numpy as np
from numpy._typing import NDArray
from objects import Camera, Light


class Render:
    def __init__(self,
                 canvas_width: float = 4.0,
                 canvas_height: float = 4.0, 
                 image_width: float = 87, 
                 image_height: float = 87) -> None:
        self.canvas_width: float = canvas_width 
        self.canvas_height: float = canvas_height 
        self.image_width: float = image_width
        self.image_height: float = image_height
        self.start: float = 0.1
        self.end: float = 100.0
        self.output: NDArray = np.full((int(self.image_width), int(self.image_height)), " ")
        self.zbuffer: NDArray = np.full((int(self.image_width), int(self.image_height)), self.end * -1)

