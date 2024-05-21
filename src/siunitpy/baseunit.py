from .dimension import Dimension
from .unit_analysis import _combine, _combine_fullname
from .unit_archive import _BASE_SI, _UNIT_STD
from .unitelement import UnitElement
from .utilcollections.compound import Compound
from .utilcollections.utils import _inplace, common_rational

_SIMPLE_EXPONENT = tuple(map(common_rational, (1, -1, 2, -2)))


class BaseUnit:
    __slots__ = ('_elements', '_dimension', '_factor', '_symbol')

    def __init__(self, elements: Compound[UnitElement], dimension: Dimension,
                 factor: float):
        self._elements = elements
        self._dimension = dimension
        self._factor = factor
        self._symbol = _combine(self._elements)

    @property
    def symbol(self) -> str: return self._symbol
    @property
    def fullname(self) -> str: return _combine_fullname(self._elements)
    @property
    def dimension(self) -> Dimension: return self._dimension
    @property
    def factor(self) -> float: return self._factor

    def __repr__(self) -> str:
        cls = self.__class__.__name__
        return f'{cls}({self.symbol}, {self.dimension}, factor={self.factor})'

    def __str__(self) -> str: return self.symbol

    def __hash__(self) -> int: return hash((self.dimension, self.factor))

    def __eq__(self, other: 'BaseUnit') -> bool:
        return self.dimension == other.dimension and self.factor == other.factor

    def sameas(self, other: 'BaseUnit', /) -> bool:
        return self._elements == other._elements

    def isdimensionless(self) -> bool:
        return self.dimension.isdimensionless()

    def deprefix_with_factor(self):
        elements = self._elements
        factor = 1
        for unit in self._elements:
            if unit.prefix == '':  # not prefixed
                continue
            if elements is self._elements:
                elements = self._elements.copy()
            e = elements.pop(unit)
            factor *= unit.prefix_factor**e
            if unit.base:  # not a single prefix
                elements[unit.deprefix()] += e
        if elements is self._elements:
            return self, 1
        cls = self.__class__
        return cls(elements, self.dimension, self.factor / factor), factor

    def deprefix(self):
        '''return a new unit that remove all the prefix.'''
        return self.deprefix_with_factor()[0]

    def tobase_with_factor(self):
        elems = Compound({UnitElement(unit): e for unit, e in
                          zip(_BASE_SI, self.dimension) if e}, copy=False)
        return self.__class__(elems, self.dimension, 1), self.factor

    def tobase(self):
        '''return a combination of base SI unit 
        (i.e. m, kg, s, A, K, mol, cd) 
        with the same dimension.
        '''
        return self.tobase_with_factor()[0]

    def simplify_with_factor(self):
        if len(self._elements) < 2:
            return self, 1
        for expo in _SIMPLE_EXPONENT:
            symbol = _UNIT_STD.get(self.dimension.nthroot(expo))
            if symbol is None:
                continue
            elements = Compound({UnitElement(symbol): expo}, copy=False)
            return self.__class__(elements, self.dimension, 1), self.factor
        return self, 1  # fail to simplify

    def simplify(self):
        '''try if the complex unit can be simplified as a single unit
        (i.e. `u`, `u⁻¹`, `u²`, `u⁻²`). 
        
        `u` is one of the chosen standard SI units for different dimensions,
        like mass for kg, length for m, time for s, etc.
        Here is the full list of them:
        - Base: m[L], kg[M], s[T], A[I], K[H], mol[N], cd[J];
        - Mechanic: Hz[T⁻¹], N[T⁻²LM], Pa[T⁻²L⁻¹M], J[T⁻²L²M], W[T⁻³L²M];
        - Electromagnetic: C[TI], V[T⁻³L²MI⁻¹], F[T⁴L⁻²M⁻¹I²], Ω[T⁻³L²MI⁻²], 
            S[T³L⁻²M⁻¹I²], Wb[T⁻²L²MI⁻¹], T[T⁻²MI⁻¹], H[T⁻²L²MI⁻²];
        - Other: lx[L⁻²J], Gy[T⁻²L²], kat[T⁻¹N]
        '''
        return self.simplify_with_factor()[0]
    
    def reduce(self, unit):
        '''TODO: 
        
        example: 
        >>> Unit('ohm.A2/m3').reduce('W')
        Unit('W/m3')
        '''
        pass

    def inverse(self):
        '''inverse of the unit.'''
        cls = self.__class__
        return cls(-self._elements, self.dimension.inverse(), 1 / self.factor)

    def __mul__(self, other: 'BaseUnit'):
        return self.__class__(self._elements + other._elements,
                              self.dimension * other.dimension,
                              self.factor * other.factor)

    def __truediv__(self, other: 'BaseUnit'):
        return self.__class__(self._elements - other._elements,
                              self.dimension / other.dimension,
                              self.factor / other.factor)

    def __pow__(self, n):
        return self.__class__(self._elements * n,
                              self.dimension**n,
                              self.factor**n)

    __imul__ = _inplace(__mul__)
    __itruediv__ = _inplace(__truediv__)
    __ipow__ = _inplace(__pow__)

    def __rtruediv__(self, one):
        '''only used in 1/unit.'''
        if one is not 1:
            raise ValueError('only 1 or Unit object can divide Unit object.')
        return self.inverse()

    def nthroot(self, n):
        '''inverse operation of power.'''
        return self.__class__(self._elements / n,
                              self.dimension.nthroot(n),
                              self.factor**(1 / n))
