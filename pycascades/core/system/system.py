from copy import deepcopy

import numpy as np
import abc


class system(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, 'size')
            and callable(subclass.size)
            and hasattr(subclass, 'f')
            and callable(subclass.f)
            or NotImplemented
        )

    @abc.abstractmethod
    def size(self):
        raise NotImplementedError

    @abc.abstractmethod
    def f(self, x, t):
        raise NotImplementedError


class network(system):
    def __init__(self):
        self._elements = []
        self._couplings = []

    def size(self):
        return np.sum([element.size() for element in self._elements])

    def add_element(self, element):
        copy = deepcopy(self)
        copy._elements.append(element)
        return copy

    def add_coupling(self, from_coupling, to_coupling, coupling):
        copy = deepcopy(self)
        if (
            self._elements[from_coupling].size() != coupling.sizes[0]
            or self._elements[to_coupling].size() != coupling.sizes[1]
        ):
            raise Exception("Coupling not possible!")
        copy._couplings.append((from_coupling, to_coupling, coupling))
        return copy

    def f(self, x, t):
        matrix = np.zeros((self.size(), self.size()))
        for cpl in self._couplings:
            i, j, val = cpl
            matrix[i, j] = val.f(t, x[j], x[i])
        diagonal = np.diag(
            [element.f(x[idx], t) for idx, element in enumerate(self._elements)]
        )
        matrix = matrix + diagonal
        return np.add.reduce(matrix, axis=1)


class double_fold(system):
    def __init__(self, a=-1, b=1, c=0, x_0=0.0):
        self._par = {}
        self._par['a'] = a
        self._par['b'] = b
        self._par['c'] = c
        self._par['x_0'] = x_0

    def size(self):
        return 1

    def f(self, x, t):
        return np.array(
            self._par['a'] * pow(x - self._par['x_0'], 3)
            + self._par['b'] * (x - self._par['x_0'])
            + self._par['c']
        )


class pitchfork(system):
    """Can also be used as polar representation of hopf"""

    def __init__(self, a, c):
        self._par['a'] = a
        self._par['c'] = c

    def size(self):
        return 1

    def f(self, x, t):
        return np.array((self._par['c'] - pow(x, 2)) * x * self._par['a'])
