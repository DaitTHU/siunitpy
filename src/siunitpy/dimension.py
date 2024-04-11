import operator
from typing import Iterable, SupportsIndex

from .utilcollections.utils import _inplace, common_rational
from .utilcollections.utils import superscript as sup

_DIM_SYMBOL = ('T', 'L', 'M', 'I', 'H', 'N', 'J')
_DIM_NUM = len(_DIM_SYMBOL)


def _unpack_vector():
    def __getter(i: int): return lambda self: self[i]  # closure
    return (property(__getter(i)) for i in range(_DIM_NUM))


class Dimension:
    __slots__ = ('__vector',)

    def __init__(self, T=0, L=0, M=0, I=0, H=0, N=0, J=0) -> None:
        dimension_vector = (T, L, M, I, H, N, J)
        self.__vector = tuple(map(common_rational, dimension_vector))

    @classmethod
    def unpack(cls, iterable: dict | Iterable, /):
        if isinstance(iterable, dict):
            return cls(**iterable)
        return cls(*iterable)

    def __getitem__(self, key: SupportsIndex): return self.__vector[key]

    def __iter__(self): return iter(self.__vector)

    T, L, M, I, H, N, J = _unpack_vector()
    time, length, mass, electric_current, thermodynamic_temperature, \
        amount_of_substance, luminous_intensity = T, L, M, I, H, N, J

    def __repr__(self) -> str:
        para = ', '.join(f'{s}={v}' for s, v in zip(_DIM_SYMBOL, self))
        return '{}({})'.format(self.__class__.__name__, para)

    def __str__(self) -> str:
        return ''.join(s + sup(v) for s, v in zip(_DIM_SYMBOL, self) if v)

    def __len__(self) -> int: return _DIM_NUM

    def __hash__(self) -> int: return hash(self.__vector)

    def __eq__(self, other: 'Dimension') -> bool:
        return self.__vector == other.__vector

    def inverse(self): 
        '''inverse of the Dimension.'''
        return self.unpack(map(operator.neg, self))

    def __mul__(self, other):
        return self.unpack(map(operator.add, self, other))

    def __truediv__(self, other):
        return self.unpack(map(operator.sub, self, other))

    __imul__ = _inplace(__mul__)
    __itruediv__ = _inplace(__truediv__)

    def __rtruediv__(self, other):
        '''only used in 1/dimension.'''
        if other is not 1:
            raise ValueError(
                'Only 1 or Dimensiond object can divide Dimension object.')
        return self.inverse()

    def __pow__(self, other):
        return self.unpack(x * other for x in self)

    def nthroot(self, n):
        '''inverse operation of power.'''
        return self.unpack(x / n for x in self)

    @staticmethod
    def product(dim_iter: Iterable['Dimension']):
        '''return the product of dimension objects.'''
        start = _DIMENSIONLESS
        for dim in dim_iter:
            start *= dim
        return start


_DIMENSIONLESS = Dimension()


if __name__ == '__main__':
    a = '''
    time
    length
    mass
    electric current
    thermodynamic temperature
    amount of substance
    luminous intensity
    '''
    print(a.replace(' ', '_').upper())
