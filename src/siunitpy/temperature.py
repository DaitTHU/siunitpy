from fractions import Fraction
from typing import TypeVar, overload

from .quantity import Quantity
from .unit import Unit
from .unitconst import UnitConst
from .utilecollections.constclass import ConstClass

__all__ = ['Temperature', 'degree']

T = TypeVar('T', int, float)

_ONE = Fraction(1)
_FIVE_NINTHS = Fraction(5, 9)
_NINE_FIFTHS = Fraction(9, 5)
_ABSOLUTE_ZERO = -273.15

_TEMPERATURE_UNIT = {
    'K': UnitConst.KELVIN,
    '°C': UnitConst.DEGREE_CELSIUS,
    '°F': Unit('°F'),
}


class Temperature(Quantity):
    @overload
    def __init__(self, unit: str | Unit): ...

    @overload
    def __init__(self, value: T, unit: str | Unit = '°C',
                 uncertainty: T = 0): ...

    def __init__(self, value, /, unit=None, uncertainty=0):
        if isinstance(value, (str, Unit)):
            if unit is not None:
                constructor = f'{self.__class__.__name__}()'
                raise ValueError(f"{constructor} can't take 2nd arg "
                                 f"when the 1st is a {type(value)}.")
            value, unit = 1, value
        elif unit is None:
            unit = '°C'
        elif not isinstance(unit, (str, Unit)):
            raise TypeError(f"{type(unit) = } is not 'str' or 'Unit'.")
        self._value = value
        self._unit = Temperature.declared_degree(unit)
        self._uncertainty = uncertainty

    def to(self, new_unit: str | Unit):
        new_unit = Temperature.declared_degree(new_unit)
        value, uncertainty = self.__transform(new_unit)
        return Temperature(value, new_unit, uncertainty)

    @staticmethod
    def declared_degree(unit: str | Unit, /) -> Unit:
        if isinstance(unit, str):
            if unit in _TEMPERATURE_UNIT:
                return _TEMPERATURE_UNIT[unit]
            unit = Unit(unit)
        if isinstance(unit, Unit) and unit.symbol in _TEMPERATURE_UNIT:
            return _TEMPERATURE_UNIT[unit.symbol]
        raise TypeError(f"'{unit} is not a temperature unit.")

    def __rmul__(self, other):
        return Temperature(other * self.value, self.unit, other * self.uncertainty)

    def __as_celsius(self) -> tuple[T, Fraction]:
        if self.unit.symbol == 'K':
            return self.value + _ABSOLUTE_ZERO, _ONE
        if self.unit.symbol == '°C':
            return self.value, _ONE
        return (self.value - 32) * 5 / 9, _FIVE_NINTHS

    @staticmethod
    def __celsius_to(value: T, new_unit: Unit) -> tuple[T, Fraction]:
        if new_unit.symbol == 'K':
            return value - _ABSOLUTE_ZERO, _ONE
        if new_unit.symbol == '°C':
            return value, _ONE
        return value * 9 / 5 + 32, _NINE_FIFTHS

    def __transform(self, new_unit: Unit) -> tuple[T, T]:
        celsius_value, factor1 = self.__as_celsius()
        new_value, factor2 = Temperature.__celsius_to(celsius_value, new_unit)
        return new_value, self.uncertainty * float(factor1 * factor2)


class degree(ConstClass):
    K = Temperature('K')
    C = Temperature('°C')
    F = Temperature('°F')
