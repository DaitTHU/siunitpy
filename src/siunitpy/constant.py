import operator
from typing import NoReturn, TypeVar

from .quantity import Quantity
from .utilcollections.abc import Linear
from .utilcollections.utils import _inplace

T = TypeVar('T', bound=Linear)


class Constant(Quantity[T]):
    def ito(self, new_unit, *, assertDimension=True) -> NoReturn:
        raise AttributeError('ito() is deleted, please use to().')

    __iadd__ = _inplace(operator.add)  # type: ignore
    __isub__ = _inplace(operator.sub)  # type: ignore
    __imul__ = _inplace(operator.mul)  # type: ignore
    __imatmul__ = _inplace(operator.matmul)  # type: ignore
    __itruediv__ = _inplace(operator.truediv)  # type: ignore
    __ifloordiv__ = _inplace(operator.floordiv)  # type: ignore
    __ipow__ = _inplace(operator.pow)  # type: ignore


def constant(quantity: Quantity[T], unit=None, *, simplify=False,
             relative_uncertainty=None):
    '''to make a Quantity object to a Constant.'''
    if unit is not None:
        quantity.ito(unit)
    elif simplify:
        quantity.simplify_unit(inplace=True)
    if relative_uncertainty is not None:
        quantity.relative_uncertainty = relative_uncertainty
    return Constant(quantity.variable, quantity.unit)
