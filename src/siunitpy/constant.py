import operator
from typing import NoReturn, TypeVar

from .quantity import Quantity
from .unit import Unit
from .utilcollections.utils import _inplace

__all__ = ['Constant', 'constant']

T = TypeVar('T')


class Constant(Quantity[T]):
    def ito(self, new_unit: str | Unit, *, assertDimension=True) -> NoReturn:
        raise AttributeError('ito() is deleted, please use to().')

    def ideprefix_unit(self) -> NoReturn:
        raise AttributeError('ito_...() is deleted, please use to_...().')

    def ito_basic_unit(self) -> NoReturn:
        raise AttributeError('ito_...() is deleted, please use to_...().')

    def isimplify_unit(self) -> NoReturn:
        raise AttributeError('itry_...() is deleted, please use try_...().')

    __iadd__ = _inplace(operator.add)
    __isub__ = _inplace(operator.sub)
    __imul__ = _inplace(operator.mul)
    __imatmul__ = _inplace(operator.matmul)
    __itruediv__ = _inplace(operator.truediv)
    __ifloordiv__ = _inplace(operator.floordiv)
    __ipow__ = _inplace(operator.pow)


def constant(quantity: Quantity[T]) -> Constant[T]:
    '''to make a Quantity object to a Constant.'''
    return Constant(quantity.variable, quantity.unit)
