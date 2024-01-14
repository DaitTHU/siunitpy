from abc import ABCMeta, abstractmethod


class Linear(metaclass=ABCMeta):
    __slots__ = ()


class Value(Linear):
    __slots__ = ()
    @abstractmethod
    def __add__(self, other): raise NotImplementedError
    @abstractmethod
    def __sub__(self, other): raise NotImplementedError
    @abstractmethod
    def __mul__(self, other): raise NotImplementedError
    @abstractmethod
    def __truediv__(self, other): raise NotImplementedError
    @abstractmethod
    def __add__(self, other): raise NotImplementedError
    @abstractmethod
    def __add__(self, other): raise NotImplementedError
