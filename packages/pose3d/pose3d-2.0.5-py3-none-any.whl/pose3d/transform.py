import numpy as np

from .te import TE
from .re import RE

from .pose import Pose

from .utils import valid_dim

class Transform:
    def __init__(self, name: str, orig: str = 'origin', dest: str = 'destination', dim: int = 3) -> None:
        # Set strings
        self.name = name
        self.origin = orig
        self.destination = dest

        # Init translation and orientation
        if valid_dim(dim):
            self.__dim = dim
            self.translation = TE(dim=self.__dim)
            self.rotation = RE(dim=self.__dim)

    # Setter functions
    def between_poses(self, pose_1: Pose, pose_2: Pose):
        '''
        Compute transform between 2 poses (3D).

        This instance of Transform will be modifed to compute the transform from pose_1 to pose_2.

        Args:
            pose_1 (Pose): Origin pose.
            pose_2 (Pose): Destination pose.
        '''
        pose_type = type(pose_1)
        if len(pose_1.position.vector()) != len(pose_2.position.vector()):
            raise AttributeError(f'Number of dimensions between both poses do not match: pose_1.__dim = {pose_1.__dim} and pose_2.__dim = {pose_2.__dim}')

        # Modify dimension of transformation depending on pose_1 and pose_2
        if pose_1.position.vector().shape != self.__dim:
            self.__dim = len(pose_1.position.vector())
            self.rotation = RE(dim=self.__dim)

        # Compute rotation from pose_1 to pose_2
        self.rotation.from_matrix(np.linalg.inv(pose_2.orientation.as_matrix()) * pose_1.orientation.as_matrix())
        self.translation.from_vector(pose_2.position.vector() - pose_1.position.vector())


    def identity(self) -> None:
        self.translation.zero()
        self.rotation.identity()
        

    def inv(self):
        self.rotation = self.rotation.inv()
        self.translation.from_vector(-self.rotation.apply(self.translation.vector()))

    def random(self):
        self.translation.random()
        self.rotation.random()
    
    # Getter functions
    def matrix(self, homogeneous: bool = True) -> np.ndarray:

        matrix = np.eye(self.__dim + 1)
        
        if self.origin != self.destination:
            matrix[:self.__dim, :self.__dim] = self.rotation.as_matrix()
            matrix[:self.__dim, self.__dim] = self.translation.vector()

        if not homogeneous:
            return matrix[:self.__dim, :]
        
        return matrix

    # Computation functions
    def apply(self, io):
        # If io is pose
        if isinstance(io, Pose):
            io.orientation.from_matrix(np.matmul(self.rotation.as_matrix(), io.orientation.as_matrix()))
            io.position += self.translation

        # If io is numpy vector
        if isinstance(io, np.ndarray):
            io = self.rotation.apply(io) + self.translation

        return io

    # Operator overloads
    def __repr__(self) -> str:
        return f'''Transform ({self.__dim}D) - {self.name}:
        Position:    {self.position.__repr__}
        Orientation: {self.orientation.__repr__}'''

    def __str__(self) -> str:
        return f'Translation: {self.position.__repr__}\nRotation:    {self.orientation.__repr__}'

    def __eq__(self, other: object) -> bool:
        return self.translation == other.translation and self.rotation == other.rotation

    def __ne__(self, other: object) -> bool:
        return self.translation != other.translation or self.rotation != other.rotation