from src.objects import *


class Outliner(object):
    def __init__(
            self,
            mesh_objects: list[Object3D],
            light: Light,
            camera: Camera
        ) -> None:
        self.mesh_objects: list = mesh_objects
        self.light: Light = light
        self.camera: Camera = camera

        self.all_objects: list[Object3D] = self.mesh_objects + [self.light, self.camera]
        self.hidden_objects : list[Object3D] = []
        self.index = 0
        self.selected: Object3D = self.all_objects[self.index]


    def add_mesh_object(self, object: Object3D) -> None:
        self.mesh_objects.append(object)


    def select_next(self) -> None:
        if self.index >= len(self.all_objects) - 1:
            self.index = 0
        else:
            self.index += 1

        self.selected: Object3D = self.all_objects[self.index]


    def select_prev(self):
        if self.index <= 0:
            self.index = len(self.all_objects) - 1
        else:
            self.index -= 1

        self.selected: Object3D = self.all_objects[self.index]


    def render(self) -> None:
        if self.camera:
            self.camera.render(
                    self.mesh_objects,
                    self.light
            )
