import operator
from typing import NoReturn, TypeVar

from .quantity import Quantity, Unit
from .utilcollections.abc import Linear
from .utilcollections.utils import _inplace

__all__ = ['Constant', 'constant']

T = TypeVar('T', bound=Linear)


class Constant(Quantity[T]):
    def ito(self, new_unit: str | Unit, *, assertDimension=True) -> NoReturn:
        raise AttributeError('ito() is deleted, please use to().')

    __iadd__ = _inplace(operator.add)  # type: ignore
    __isub__ = _inplace(operator.sub)  # type: ignore
    __imul__ = _inplace(operator.mul)  # type: ignore
    __imatmul__ = _inplace(operator.matmul)  # type: ignore
    __itruediv__ = _inplace(operator.truediv)  # type: ignore
    __ifloordiv__ = _inplace(operator.floordiv)  # type: ignore
    __ipow__ = _inplace(operator.pow)  # type: ignore


def constant(quantity: Quantity[T]):
    '''to make a Quantity object to a Constant.'''
    return Constant(quantity.variable, quantity.unit)


class OneUnit(Constant[float]):
    '''1 unit'''
    def __init__(self, unit: str | Unit) -> None:
        super().__init__(1, unit)  # type: ignore

    def __rmatmul__(self, other):
        try:
            return super().__rmatmul__(other)
        except (TypeError, ValueError):
            return super().__mul__(other)
