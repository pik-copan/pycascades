import math


class linear_coupling():
    sizes = (1, 1)

    def __init__(self, strength):
        self._strength = strength

    def f(self, t, x_from, x_to):
        return self._strength * x_from


class multiplicative_coupling():
    sizes = (1, 1)

    def __init__(self, strength):
        self._strength = strength

    def f(self, t, x_from, x_to):
        return self._strength * x_from * x_to


class hopf_to_cusp():
    sizes = (1, 1)

    def __init__(self, strength, frequency, shift):
        self._strength = strength
        self._frequency = frequency
        self._shift = shift

    def f(self, t, x_from, x_to):
        return (
            self._strength
            * x_from
            * math.sin(self._frequency * t + self._shift)
        )


class hopf_to_hopf():
    sizes = (1, 1)

    def __init__(self, strength, frequency, shift):
        self._strength = strength
        self._frequency = frequency
        self._shift = shift

    def f(self, t, x_from, x_to):
        return (
            self._strength
            * x_to
            * x_from
            * math.sin(self._frequency * t + self._shift)
        )
