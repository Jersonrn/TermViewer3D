import sys
import numpy as np
import cupy as cp
from cupy import float64, ndarray, cos, sin
from numpy._typing import NDArray
from Vector import Vector3D

from pywavefront import Wavefront
from pywavefront.mesh import Mesh
from pywavefront.material import Material


class Object3D:
    def __init__(self,
                 position: Vector3D = Vector3D(),
                 rotation: Vector3D = Vector3D(),
                 up: Vector3D = Vector3D(0, 1, 0)) -> None:
        
        self.position: Vector3D = position
        self.rotation: Vector3D = rotation
        self.up: Vector3D = up
        self.matrix: cp.NDArray = cp.array([
            [1.0000, 0.0000, 0.0000, 0.0000],
            [0.0000, 1.0000, 0.0000, 0.0000],
            [0.0000, 0.0000, 1.0000, 0.0000],
            [0.0000, 0.0000, 0.0000, 1.0000],
            ])
        
        self.__set_defaults(self.position, self.rotation)

    def set_position(self, pos: Vector3D) -> None:
        Pm: cp.NDArray = cp.array([
            [1.0000, 0.0000, 0.0000, pos.x],
            [0.0000, 1.0000, 0.0000, pos.y],
            [0.0000, 0.0000, 1.0000, pos.z],
            [0.0000, 0.0000, 0.0000, 1.000],
            ])
        
        self.matrix = cp.dot(Pm, self.matrix)

    def rotate_x(self, angle: int) -> None:
        angle = cp.deg2rad(angle)
        Rx: cp.NDArray = cp.array([
            [1.0000, 0.00000000000000000, 0.000000000000000000, 0.0000],
            [0.0000, float64(cos(angle)), float64(-sin(angle)), 0.0000],
            [0.0000, float64(sin(angle)), float64( cos(angle)), 0.0000],
            [0.0000, 0.00000000000000000, 0.000000000000000000, 1.0000],
            ])
        
        self.matrix = cp.dot(Rx, self.matrix)

    def local_rotate_x(self, angle) -> None: ...
    
    def rotate_y(self, angle) -> None:
        angle = cp.deg2rad(angle)
        Ry: cp.NDArray = cp.array([
            [float64( cos(angle)), 0.0000, float64(sin(angle)), 0.0000],
            [0.000000000000000000, 1.0000, 0.000000000000000000, 0.0000],
            [float64(-sin(angle)), 0.0000, float64(cos(angle)), 0.0000],
            [0.000000000000000000, 0.0000, 0.000000000000000000, 1.0000],
            ])
        
        self.matrix = cp.dot(Ry, self.matrix)

    def local_rotate_y(self, angle) -> None: ...

    def rotate_z(self, angle) -> None:
        angle = cp.deg2rad(angle)
        Rz: cp.NDArray = cp.array([
            [float64(cos(angle)), float64(-sin(angle)), 0.0000, 0.0000],
            [float64(sin(angle)), float64( cos(angle)), 0.0000, 0.0000],
            [0.00000000000000000, 0.000000000000000000, 1.0000, 0.0000],
            [0.00000000000000000, 0.000000000000000000, 0.0000, 1.0000],
            ])
        
        self.matrix = cp.dot(Rz, self.matrix)

    def local_rotate_z(self, angle) -> None: ...

    def __set_defaults(self, position, rotation) -> None:
        self.set_position(position)
        self.rotate_x(rotation.x)
        self.rotate_y(rotation.y)
        self.rotate_z(rotation.z)

    def local_to_global(self, a): ...

    def global_to_local(self, a): ...

    @staticmethod
    def ascupy(a) -> ndarray:
        a = cp.asarray(a)
        return a


class Torus(Object3D):
    def __init__(self,
                 position: Vector3D = Vector3D(),
                 rotation: Vector3D = Vector3D(),
                 up: Vector3D = Vector3D(0, 1, 0),
                 major_res: int = 10,
                 minor_res: int = 10,
                 major_radio: float = 10,
                 minor_radio: float = 3) -> None:
        super().__init__(position, rotation, up)
        self.vertices: ndarray
        self.normales: ndarray
        self.update_mesh(minor_res, major_res,
                         minor_radio, major_radio,
                         self.up)

    def update_mesh(self, minor_res: int, major_res: int,
                    minor_radio: float, major_radio: float,
                    up: Vector3D) -> None:
        i = cp.linspace(start=0, stop=360, num=minor_res, endpoint=False)
        j = cp.linspace(start=0, stop=360, num=major_res, endpoint=False)
        alpha, phi = cp.meshgrid(i, j)
        
        #X_UP
        if up.x == 1 and up.y == 0 and up.z == 0:
            vertices: NDArray = cp.array([
                (minor_radio * cp.sin(cp.deg2rad(alpha))),
                (major_radio + minor_radio * cp.cos(cp.deg2rad(alpha))) * cp.cos(cp.deg2rad(phi)),
                (major_radio + minor_radio * cp.cos(cp.deg2rad(alpha))) * cp.sin(cp.deg2rad(phi))
                ])
            vertices = cp.reshape(vertices, (3,-1))
            
            homogeneus = np.ones((1, len(vertices[0])), dtype=int)
            vertices = np.vstack((vertices, homogeneus))
            
            self.vertices = vertices
            self.normales = vertices
        
        #Y_UP
        elif up.x == 0 and up.y == 1 and up.z == 0:
            vertices: NDArray = cp.array([
                (major_radio + minor_radio * cp.cos(cp.deg2rad(alpha))) * cp.cos(cp.deg2rad(phi)),
                (minor_radio * cp.sin(cp.deg2rad(alpha))),
                (major_radio + minor_radio * cp.cos(cp.deg2rad(alpha))) * -cp.sin(cp.deg2rad(phi))
                ])
            vertices = cp.reshape(vertices, (3,-1))
            
            homogeneus = np.ones((1, len(vertices[0])), dtype=int)
            vertices = np.vstack((vertices, homogeneus))
            
            self.vertices = vertices
            self.normales = vertices
        
        #Z_UP
        elif up.x == 0 and up.y == 0 and up.z == 1:
            vertices = cp.array([
                (major_radio + minor_radio * cp.cos(cp.deg2rad(alpha))) * cp.cos(cp.deg2rad(phi)),
                (major_radio + minor_radio * cp.cos(cp.deg2rad(alpha))) * cp.sin(cp.deg2rad(phi)),
                (minor_radio * cp.sin(cp.deg2rad(alpha))),
                ], dtype=float64)
            vertices = cp.reshape(vertices, (3,-1))
            
            homogeneus = np.ones((1, len(vertices[0])), dtype=int)
            vertices = np.vstack((vertices, homogeneus))
            
            self.vertices = vertices
            self.normales = vertices
            
        else:
            raise Exception(ValueError)

    def local_to_global(self, a):
        return cp.dot(self.matrix, a)
        # return super().local_to_global(a)

    def global_to_local(self, a):
        return cp.dot(self.matrix, a)
        # return super().global_to_local(a)


class Light(Object3D):
    def __init__(self,
                 position: Vector3D = Vector3D(),
                 rotation: Vector3D = Vector3D(),
                 up: Vector3D = Vector3D(0, 1, 0), 
                 dir: Vector3D = Vector3D(0,-1,0), 
                 strenght:float = 11.0) -> None:
        super().__init__(position, rotation, up)
        self.dir: Vector3D = dir
        self.strenght: float = strenght

    def local_to_global(self, a):
        return cp.dot(self.matrix, a)
        # return super().local_to_global(a)

    def global_to_local(self, a):
        return cp.dot(self.matrix, a)
        # return super().global_to_local(a)


class Camera(Object3D):
    def __init__(self,
                 position: Vector3D = Vector3D(),
                 rotation: Vector3D = Vector3D(),
                 up: Vector3D = Vector3D(0, 1, 0), 
                 dir: Vector3D = Vector3D(0, 0, -1), 
                 canvas_width:  float = 4.0, 
                 canvas_height: float = 4.0, 
                 image_width: float = 87, 
                 image_height: float = 87) -> None:
        super().__init__(position, rotation, up)
        self.dir: Vector3D = dir
        self.canvas_width: float = canvas_width 
        self.canvas_height: float = canvas_height 
        self.image_width: float = image_width
        self.image_height: float = image_height
        self.start: float = 0.1
        self.end: float = 100.0
        self.output: NDArray = np.full((int(self.image_width), int(self.image_height)), " ")
 
    def global_to_local(self, a):
        return cp.dot(cp.linalg.inv(self.matrix), a)
        # return super().global_to_local(a)

    def local_to_global(self, a):
        return cp.dot(cp.linalg.inv(self.matrix), a)
        # return super().local_to_global(a)

    def __join_vertices_and_normals(self, meshes):
        #Concatena todos los vertices y los transforma a WorldSpace
        return cp.concatenate([cp.asarray([mesh.local_to_global(mesh.vertices),
                                           mesh.local_to_global(mesh.normales)])
                               for mesh in meshes], axis=1)

    def sort_by_distance(self, vertices, normales):
        i = np.argsort(vertices[:,2])#[::-1]
        vertices = vertices[i]
        normales = normales[i]
        return vertices, normales

    # def __other_perspective_projection(self, vertices, camera) -> None:
    #     # mask = (vertices[:, 2] == 0) | (np.isnan(vertices[:, 2])) #Mask is not...
    #     # vertices[:, 2][mask] = 1e-10#                               ...necessary
    #     vertices = np.dot(np.linalg.inv(camera.matrix), vertices)[:-1]
    #     p_screen = vertices[:2] / -vertices[-1]

    def __perspective_projection(self, vertices) -> NDArray:
        p_screen = np.array(vertices[:, :2] / -vertices[:, 2, None])
        # p_screen = self.__crop_screen(p_screen)
        return p_screen

    def __crop_screen(self, p_screen, normales) -> tuple:
        mask = np.logical_and(np.absolute(p_screen[:,0]) < self.canvas_width,
                              np.absolute(p_screen[:,1]) < self.canvas_height)
        p_screen = p_screen[mask]
        normales = normales[mask]
        return p_screen, normales

    def __normalize_point(self, p_screen) -> NDArray:
        p_norm = np.array([
            [(p_screen[:,0] + self.canvas_width * 0.5) / self.canvas_width,
             (p_screen[:,1] + self.canvas_height * 0.5) / self.canvas_height]
            ])
        return p_norm[0].T

    def __raster_point(self, p_norm) -> NDArray:
        p_raster = np.array([
            [np.floor(p_norm[:,0] * self.image_width),
             np.floor((1 - p_norm[:,1]) * self.image_height)]
            ])
        return p_raster[0].T

    def __luminance(self, normales, light_dir) -> NDArray:
        # return (np.dot(normales, light_dir)) / (np.linalg.norm(normales, axis=1) * np.linalg.norm(light_dir))
        x, y, z = (0, 1, 2)
        return np.array(
                (normales[:,x] * light_dir[x]) +
                (normales[:,y] * light_dir[y]) +
                (normales[:,z] * light_dir[z]) )

    def __luminance_normalized(self, luminance) -> NDArray:
        l_min = np.amin(luminance)
        l_max = np.amax(luminance)
        return np.array(
                # (1-(-1)) * ((luminance - l_min) / (l_max - l_min)) + (-1)
                2 * ((luminance - l_min) / (l_max - l_min)) - 1
                )

    def clear_terminal(self) -> None:
        sys.stdout.write("\033[2J")
        sys.stdout.write("\033[H")

    def write_in_terminal(self):
        colors = {
                "@": (255, 255, 255),
                "$": (255, 255, 255),
                "#": (245, 245, 245),
                "*": (235, 235, 235),
                "!": (225, 225, 225),
                "=": (215, 215, 215),
                ";": (205, 205, 205),
                ":": (195, 195, 195),
                "~": (185, 185, 185),
                "-": (175, 175, 175),
                ",": (165, 165, 165),
                ".": (155, 155, 155)
                }
        for i in range(int(self.image_width)):
            for j in range(int(self.image_height)):
                pixel = self.output[i][j]
                color = colors.get(pixel,(000, 000, 000))
                sys.stdout.write(f"\033[1;38;2;{color[0]};{color[1]};{color[2]}m{str(pixel)} \033[0m")
            sys.stdout.write("\n")


    def render(self, meshes, light: Light) -> None:
        self.output = np.full((int(self.image_width), int(self.image_height)), " ")

        vertices, normales = self.__join_vertices_and_normals(meshes)
        vertices = self.global_to_local(vertices)[:-1].T
        normales = self.global_to_local(normales)[:-1].T
        
        # OOZ: NDArray = np.array(1 / vertices[:,2])
        # v = np.column_stack((vertices,OOZ))
        # i = np.argsort(v[:,3])
        # vertices = vertices[i]
        # normales = normales[i]
     
        vertices, normales = cp.asnumpy(vertices), cp.asnumpy(normales)
        vertices, normales = self.sort_by_distance(vertices, normales)
        
        p_screen = self.__perspective_projection(vertices)
        p_screen, normales = self.__crop_screen(p_screen, normales)
        
        p_norm: NDArray = self.__normalize_point(p_screen)
        
        p_raster: NDArray = self.__raster_point(p_norm)
        
        ascii = np.array([".", ",", "-", "~", ":", ";", "=", "!", "*", "#", "$", "@"])
        
        light_dir = light.local_to_global(light.dir.cpVector3D2Array4D())
        light_dir = self.global_to_local(light_dir)[:-1]
        light_dir = cp.asnumpy(light_dir)
        
        luminance = self.__luminance(normales, light_dir)
        luminance = self.__luminance_normalized(luminance)
        lumin_index = (luminance * light.strenght).astype(int)
        lumin_index[lumin_index > (ascii.shape[0] - 1)] = (ascii.shape[0] - 1)
        
        mask = np.logical_and(luminance > 0,
                              np.logical_and(p_raster[:,0] < self.image_width,
                                             p_raster[:,1] < self.image_height))
        
        self.output[p_raster[:,0].astype(int)[mask],
                    p_raster[:,1].astype(int)[mask]] = ascii[lumin_index[mask]]
        
        self.clear_terminal()
        self.write_in_terminal()


class Cube(Object3D):
    def __init__(self,
                 position: Vector3D = Vector3D(),
                 rotation: Vector3D = Vector3D(),
                 up: Vector3D = Vector3D(0, 1, 0),
                 size: Vector3D = Vector3D(1, 1, 1),
                 res: Vector3D = Vector3D(10, 10, 10)) -> None:
        super().__init__(position, rotation, up)
        self.vertices: NDArray
        self.normales: NDArray
        self.update_mesh(size, res)

    def update_mesh(self, size: Vector3D, res: Vector3D):
        i: NDArray = np.linspace(start=-size.x, stop=size.x,
                                 num=int(res.x), endpoint=True)
        
        j: NDArray = np.linspace(start=-size.y, stop=size.y,
                                 num=int(res.y), endpoint=True)
        
        k: NDArray = np.linspace(start=size.z, stop=-size.z,
                                 num=int(res.z), endpoint=True)
        
        x, y, z = np.meshgrid(i, j, k)
        x, y, z = x.ravel(), y.ravel(), z.ravel()
        vertices = np.array([x, y, z])
        
        # mask =  np.logical_and(vertices[0] > -size.x, np.logical_and(vertices[0] < size.x,
        #         np.logical_and(vertices[1] > -size.y, np.logical_and(vertices[1] < size.y,
        #         np.logical_and(vertices[2] > -size.z, vertices[2] < size.z)))))
        
        mask_x = np.logical_or(vertices[0] == (-size.x), vertices[0] == (size.x))
        mask_y = np.logical_or(vertices[1] == (-size.y), vertices[1] == (size.y))
        mask_z = np.logical_or(vertices[2] == (-size.z), vertices[2] == (size.z))
        mask = np.logical_or(mask_x, np.logical_or(mask_y, mask_z))

        vertices = vertices.transpose()
        vertices = vertices[mask]
        vertices = vertices.transpose()

        homogeneus = np.ones((1, len(vertices[0])), dtype=int)
        vertices = np.vstack((vertices, homogeneus))
        
        self.vertices = self.ascupy( vertices )
        self.normales = self.ascupy( vertices )

    def local_to_global(self, a):
        return cp.dot(self.matrix, a)
        # return super().local_to_global(a)

    def global_to_local(self, a):
        return cp.dot(self.matrix, a)
        # return super().global_to_local(a)

class Plane(Object3D):
    def __init__(self,
                 position: Vector3D = Vector3D(),
                 rotation: Vector3D = Vector3D(),
                 up: Vector3D = Vector3D(0, 1, 0),
                 size: Vector3D = Vector3D(1, 1, 0),
                 res: Vector3D = Vector3D(10, 10, 0)) -> None:
        super().__init__(position, rotation, up)
        self.vertices: NDArray
        self.normales: NDArray
        self.update_mesh(size, res)
        
    def update_mesh(self, size, res) -> None:
        i: NDArray = np.linspace(start=-size.x, stop=size.x,
                                 num=int(res.x), endpoint=True)
        
        j: NDArray = np.linspace(start=-size.y, stop=size.y,
                                 num=int(res.y), endpoint=True)
        x, y = np.meshgrid(i, j)
        x, y = np.ravel(x), np.ravel(y)
        
        z = np.zeros((len(x)), dtype=int)
        homogeneus = np.ones(len(x), dtype=int)
        
        if self.up.x == 1 and self.up.y == 0 and self.up.z == 0:
            vertices = np.array([z, y, x, homogeneus])
            self.vertices = self.ascupy( vertices )
            self.normales = self.ascupy( vertices )
        
        elif self.up.x == 0 and self.up.y == 1 and self.up.z == 0:
            vertices = np.array([x, z, y, homogeneus])
            self.vertices = self.ascupy( vertices )
            self.normales = self.ascupy( vertices )
        
        elif self.up.x == 0 and self.up.y == 0 and self.up.z == 1:
            vertices = np.array([x, y, z, homogeneus])
            self.vertices = self.ascupy( vertices )
            self.normales = self.ascupy( vertices )
        
        else:
            raise Exception(ValueError)

    def local_to_global(self, a):
        return cp.dot(self.matrix, a)
        # return super().local_to_global(a)

    def global_to_local(self, a):
        return cp.dot(self.matrix, a)
        # return super().global_to_local(a)

class Suzanne(Object3D):
    def __init__(self,
                 position: Vector3D = Vector3D(),
                 rotation: Vector3D = Vector3D(),
                 up: Vector3D = Vector3D(0, 1, 0)) -> None:
        super().__init__(position, rotation, up)
        self.vertices: ndarray
        self.normales: ndarray
        self.update_mesh()

    def import_obj(self):
        suzanne = Wavefront("3D_Models/Suzanne.obj")
        suzanne.parse()
        # m = suzanne.materials.items()
        vertices = np.array(suzanne.vertices)
        
        homogeneus = np.ones((vertices.shape[0], 1), dtype=int)
        
        vertices = np.concatenate((vertices, homogeneus), axis=1)
        
        vertices = vertices.transpose()
        
        return self.ascupy(vertices)

    def update_mesh(self) -> None:
        vertices = self.import_obj()
        normales = vertices
        
        self.vertices = vertices
        self.normales = normales

    def local_to_global(self, a):
        return cp.dot(self.matrix, a)
        # return super().local_to_global(a)

    def global_to_local(self, a):
        return cp.dot(self.matrix, a)
        # return super().global_to_local(a)
