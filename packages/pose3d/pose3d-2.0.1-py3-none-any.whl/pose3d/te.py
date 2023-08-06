import numpy as np

from .utils import valid_dim

class TE:
    def __init__(self, name: str ='', dim: int = 3, vector: np.ndarray = None) -> None:
        self.name = name

        if valid_dim(dim):
            self.__dim = dim

        if vector is None:
            self.__vector = np.zeros(self.__dim)
        else:
            if valid_dim(len(vector)):
                self.__dim = len(vector)
                self.__vector = vector

    # Setter functions
    def random(self) -> None:
        self.from_vector(np.random.rand(self.__dim))

    def from_vector(self, vector: np.ndarray) -> None:
        if vector.shape == self.__vector.shape:
            self.__vector = vector

    def zero(self) -> None:
        self.from_vector(np.zeros(self.__dim))

    def inv(self) -> None:
        self.from_vector(-self.vector())

    # Getter functions
    def vector(self) -> np.ndarray:
        return self.__vector

    def x(self) -> float:
        return float(self.vector()[0])

    def y(self) -> float:
        return float(self.vector()[1])

    def z(self) -> float:
        return float(self.vector()[2])

    # Operator overloads
    def __str__(self) -> str:
        return f'TE{self.__dim} - {self.name}: {self.vector()}'

    def __repr__(self) -> str:
        return f'{self.vector()}'

    def __add__(self, other):
        if isinstance(other, TE):
            if other.vector().shape == self.vector().shape:
                return TE(name=f'Sum of {self.name} and {other.name}',
                          vector=self.vector() + other.vector())

        elif isinstance(other, np.ndarray):
            if other.shape == self.vector().shape:
                return TE(name=self.name,
                           vector=self.vector() + other)

        else:
            raise TypeError(f'Input parameter is {type(other)}, not TE or np.ndarray as expected.')

    def __sub__(self, other):
        if isinstance(other, TE):
            if other.vector().shape == self.vector().shape:
                return TE(name=f'Sum of {self.name} and {other.name}',
                          vector=self.vector() - other.vector())

        elif isinstance(other, np.ndarray):
            if other.shape == self.vector().shape:
                return TE(name=self.name,
                           vector=self.vector() - other)

        else:
            raise TypeError(f'Input parameter is {type(other)}, not TE or np.ndarray as expected.')

    def __iadd__(self, other):
        if isinstance(other, TE):
            if other.vector().shape == self.vector().shape:
                self.from_vector(self.vector() + other.vector())

        elif isinstance(other, np.ndarray):
            if other.shape == self.vector().shape:
                self.from_vector(self.vector() + other)

        else:
            raise TypeError(f'Input parameter is {type(other)}, not TE or np.ndarray as expected.')

    def __isub__(self, other):
        if isinstance(other, TE):
            if other.vector().shape == self.vector().shape:
                self.from_vector(self.vector() - other.vector())

        elif isinstance(other, np.ndarray):
            if other.shape == self.vector().shape:
                self.from_vector(self.vector() - other)

        else:
            raise TypeError(f'Input parameter is {type(other)}, not TE or np.ndarray as expected.')

    def __eq__(self, other):
        if isinstance(other, TE):
            return np.array_equal(self.vector(), other.vector())
            
        elif isinstance(other, np.ndarray):
            return np.array_equal(self.vector(), other)

        else:
            raise TypeError(f'Input parameter is {type(other)}, not TE or np.ndarray as expected.')

    def __ne__(self, other):
        if isinstance(other, TE):
            return not np.array_equal(self.vector(), other.vector())
            
        elif isinstance(other, np.ndarray):
            return not np.array_equal(self.vector(), other)

        else:
            raise TypeError(f'Input parameter is {type(other)}, not TE or np.ndarray as expected.')

    def __neg__(self):
        self.from_vector(-self.vector())

    def __abs__(self):
        self.from_vector(abs(self.vector()))
