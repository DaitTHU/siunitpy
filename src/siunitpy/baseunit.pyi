'''
The `Unit` class is a sophisticated data structure that encapsulates a 
complete unit of measurement, including its composition from one or more 
`UnitElement` objects with their respective exponents, as well as its 
dimensionality. Additionally, it provides properties to access the unit's 
symbolic representation and its full name, enhancing clarity and convenience 
in scientific and engineering applications.

Properties:
- `symbol`: A string property that represents the symbolic or abbreviated form 
of the unit. This is a concise notation that is commonly used in mathematical 
expressions and scientific literature to represent the unit. For example, the 
symbol for meters is "m", and for seconds it is "s".
- `fullname`: A string property that provides the full name of the unit. This 
is the descriptive name that is used in formal contexts and documentation to 
clarify the unit's meaning. For example, the full name for meters is "meter", 
and for seconds it is "second".

Attributes:
- `elements`: A collection, typically implemented as a dictionary, that maps 
`UnitElement` objects to their corresponding exponents. This structure allows 
for the representation of complex units that are formed by combining multiple 
`UnitElement` instances. Each `UnitElement` may have a different exponent, 
reflecting its contribution to the overall unit composition. For instance, in 
the unit for acceleration (m/s^2), the `UnitElement` "m" (for meters) has an 
exponent of 1, while the "s" (for seconds) has an exponent of -2.
- `dimension`: A data field that characterizes the dimensionality of the unit, 
classifying it within the broader context of physical quantities. This is a 
fundamental feature of the unit, as it distinguishes one type of measurement 
from another. Common dimensions include length (L), mass (M), time (T), 
electric current (I), temperature (Θ), amount of substance (N), and luminous 
intensity (J). The dimension provides a conceptual framework for understanding 
and categorizing units.
- `factor`: A numerical value that serves as the scale factor for the unit, 
enabling conversions to and from a standardized or base unit. This factor is 
essential for aligning the unit with a common reference scale, particularly 
when performing unit conversions. It acts as a multiplier or divisor to adjust 
the unit's value to a different but equivalent unit within the same dimension. 
For example, a factor of 1000 might be applied to convert grams to kilograms.

The `Unit` class is designed to provide a comprehensive and integrated approach 
to handling units of measurement. It ensures that all necessary data for a 
specific unit is consolidated within a single, cohesive object, thereby 
enhancing the accuracy and integrity of scientific, engineering, and other 
computations that involve unit manipulation.
'''

import sys
from fractions import Fraction
from typing import Literal

from .dimension import Dimension
from .unitelement import UnitElement
from .utilcollections.compound import Compound

__all__ = ['BaseUnit']

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing import TypeVar
    Self = TypeVar('Self', bound='Dimension')


class BaseUnit:
    '''The base class of `Unit`.
    '''
    def __init__(self, elements: Compound[UnitElement], dimension: Dimension,
                 factor: float): 
        '''see the document of `baseunit` for parameter explanation.'''

    @property
    def symbol(self) -> str: ...
    @property
    def fullname(self) -> str: ...
    @property
    def dimension(self) -> Dimension: ...
    @property
    def factor(self) -> float: ...
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
    def __hash__(self) -> int: ...
    def deprefix_with_factor(self) -> tuple[Self, float]: ...
    def tobase_with_factor(self) -> tuple[Self, float]: ...
    def simplify_with_factor(self) -> tuple[Self, float]: ...
    def deprefix(self) -> Self: ...
    def tobase(self) -> Self: ...
    def simplify(self) -> Self: ...
    def __eq__(self, other: BaseUnit) -> bool: ...
    def sameas(self, other: BaseUnit) -> bool: ...
    # def parallel(self, other: BaseUnit, /) -> bool: ...
    def isdimensionless(self) -> bool: ...
    def inverse(self) -> Self: ...
    def __mul__(self, other: BaseUnit) -> Self: ...
    def __truediv__(self, other: BaseUnit) -> Self: ...
    def __imul__(self, other: BaseUnit) -> Self: ...
    def __itruediv__(self, other: BaseUnit) -> Self: ...
    def __rtruediv__(self, one: Literal[1]) -> Self: ...
    def __pow__(self, n: int | float | Fraction) -> Self: ...
    def __ipow__(self, n: int | float | Fraction) -> Self: ...
    def nthroot(self, n: int | float | Fraction) -> Self: ...
