import operator
from typing import Any, NoReturn, TypeVar

from .quantity import Quantity
from .unit import Unit
from .utilcollections.abc import Linear
from .utilcollections.utils import _inplace

__all__ = ['Constant', 'constant']

T = TypeVar('T', bound=Linear[Any, Any])


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
