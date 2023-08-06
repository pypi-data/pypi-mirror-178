import numpy as np
from scipy.spatial.transform import Rotation
from .utils import RE_TOLERANCE, valid_dim

class RE:
    def __init__(self, name: str = '', dim: int = 3) -> None:
        self.name = name
        self.__rotation = Rotation(quat=[0, 0, 0, 1])

        if valid_dim(dim):
            self.__dim = dim

    # Setter functions
    def identity(self):
        self.__rotation = Rotation.identity()

    def inv(self):
        self.__rotation = self.__rotation.inv()

    def random(self):
        self.__rotation = Rotation.random()

    def from_quat(self, quat: np.ndarray) -> None:
        if self.__dim == 2:
            raise AttributeError(f'Unable to set 2D rotation from quaternion input.')

        self.__rotation = Rotation.from_quat(quat)

    def from_matrix(self, matrix: np.ndarray) -> None:
        if matrix.shape != (self.__dim, self.__dim):
            raise ValueError(f'Input matrix shape must be ({self.__dim}, {self.__dim}) when rotation dimension is {self.__dim}. Current input matrix shape: {matrix.shape}.')

        if self.__dim == 2:
            matrix = np.hstack(matrix, np.zeros(2))
            matrix = np.vstack(matrix, [0, 0, 1])
        
        self.__rotation = Rotation.from_matrix(matrix)

    def from_angle_axis(self, angle_axis: np.ndarray) -> None:
        if self.__dim == 2:
            raise AttributeError(f'Unable to set 2D rotation from angle-axis input.')

        self.__rotation = Rotation.from_rotvec(angle_axis)

    def from_euler(self, sequence: str = None, angles: list = None, degrees: bool = True) -> None:
        if self.__dim == 3:
            self.__rotation = Rotation.from_euler(sequence, angles, degrees)

        # TODO: Verify functionality with test
        elif self.__dim == 2:
            self.__rotation = Rotation.from_euler('z', angles, degrees)

    # Getter functions
    def as_quat(self) -> np.ndarray:
        return self.__rotation.as_quat()

    def as_matrix(self) -> np.ndarray:
        return self.__rotation.as_matrix()[:self.__dim, :self.__dim]

    def as_angle_axis(self) -> np.ndarray:
        return self.__rotation.as_rotvec()

    def as_euler(self, sequence: str = None, degrees: bool = True):
        if self.__dim == 3:
            return self.__rotation.as_euler(sequence, degrees)

        elif self.__dim == 2:
            return self.__rotation.as_euler('z', degrees)[0]

    def yaw(self, degrees: bool = True) -> float:
        '''
        Return rotation angle around the z axis

        Args:
            degrees (bool, optional): Option to return value in degrees or radians. Defaults to True.

        Returns:
            float: Yaw angle (in specified units)
        '''
        if self.__dim == 2:
            raise AttributeError(f'Unable to return yaw angle of 2D rotation (Call as_euler instead).')

        return self.__rotation.as_euler('z', degrees)[0]

    def pitch(self, degrees: bool = True) -> float:
        '''
        Return rotation angle around the y axis

        Args:
            degrees (bool, optional): Option to return value in degrees or radians. Defaults to True.

        Returns:
            float: Pitch angle (in specified units)
        '''
        if self.__dim == 2:
            raise AttributeError(f'Unable to return pitch angle of 2D rotation (Call as_euler instead).')

        return self.__rotation.as_euler('y', degrees)[0]

    def roll(self, degrees: bool = True) -> float:
        '''
        Return rotation angle around the x axis

        Args:
            degrees (bool, optional): Option to return value in degrees or radians. Defaults to True.

        Returns:
            float: Roll angle (in specified units)
        '''
        if self.__dim == 2:
            raise AttributeError(f'Unable to return roll angle of 2D rotation (Call as_euler instead).')

        return self.__rotation.as_euler('x', degrees)[0]

    # Computation functions
    def apply(self, input):
        # Check shape of input
        if input.shape[0] != self.__dim:
            raise ValueError(f'Input shape mismatch: self.__dim ({self.__dim}) != input.shape ({input.shape[0]})')
        
        
        return self.__rotation.apply(input)

    # Operator overloading
    def __str__(self) -> str:
        return f'RE - {self.name}: {self.__repr__()} degrees'

    def __repr__(self) -> str:
        if self.__dim == 3:
            sequence = 'xyz'
        if self.__dim == 2:
            sequence = 'z'

        return f'{self.as_euler(sequence, True)} degrees'

    def __eq__(self, other):
        if isinstance(other, RE):
            return np.allclose(self.as_quat(),
                               other.as_quat(),
                               rtol=RE_TOLERANCE,
                               atol=RE_TOLERANCE)
        else:
            raise TypeError(f'Input parameter is {type(other)}, not RE as expected.')

    def __ne__(self, other):
        if isinstance(other, RE):
            return not np.allclose(self.as_quat(),
                                   other.as_quat(),
                                   rtol=RE_TOLERANCE,
                                   atol=RE_TOLERANCE)
        else:
            raise TypeError(f'Input parameter is {type(other)}, not RE as expected.')
    