'''    
Resolving rules
---
- for special elements, convert it to formular, like '℃' -> '°C'.
- some special dimensionless unit should not be prefixed or combined, 
  like '%', '°', '″'...
- split the symbol into element list by linkers: '/', '.', '·' 
  (and their combination), after the first '/', all elements are the 
  denominators.
- exponents of the elements are the digits and sign at the end of each
  substring.
- elements are the first combination without digits
  and sign and space and '^'.
'''

if False:
    try:
        # download regex module: https://pypi.org/project/regex/
        import regex as re
    except ImportError:
        import re
        raise ImportWarning('please use regex.')
import re
from fractions import Fraction

from .dimension import Dimension
from .dimensionconst import DimensionConst
from .templatelib import Compound, Vector
from .templatelib.utils import _prod, _sum, unzip
from .unit_data import (
    _PREFIX_FACTOR, _SPECIAL_DIMENSIONLESS, _SUPERSCRIPT, _UNITS)

__all__ = ['_resolve', '_combine', '_deprefix']

_UNIT_SEP = re.compile(r'[/.·]+')
_UNIT_EXPO = re.compile(r'[0-9+-]+$')
_UNIT_STR = re.compile(r'[^0-9 +-]+')

_FORMULARIZE = {
    'μ': 'µ',
    '℃': '°C', '℉': '°F',
    '٪': '%', '⁒': '%',
} | {s: str(i) for i, s in enumerate(_SUPERSCRIPT)}
_SPECIAL_UNIT = re.compile(r'eV/c[2²]?|' + '|'.join(_FORMULARIZE))
_FORMULARIZE |= {'eV/c': 'eVpc', 'eV/c2': 'eVpcc', 'eV/c²': 'eVpcc'}
_FORMULAIC_UNIT = re.compile(r'eVpcc?')
_SPECIALIZE = {'eVpc': 'eV/c', 'eVpcc': 'eV/c²'}


def _resolve(symbol: str, /) -> tuple[Compound[str], Dimension, float]:
    '''resolve the unit info from `str`, there are 3 return values:
    - `elements`: `Compound[str]`, key is element (i.e. basic unit), value
                  is exponent.
    - `dimension`: `Dimension`, dimension of the unit.
    - `value`: `float`, value of the unit, i.e. 1 unit = ? standard unit.

    Example:
    ---
    symbol `'cal/h.m2'` through resolving:
    - `elements`: `{'cal': 1, 'h': -1, 'm': -2}`
    - `dimension`: `(0, 1, -3, 0, 0, 0, 0)`
    - 1 cal = 4.1868 J, 1 h = 3600 s, 1 m = 1 m, thus 
      `value` = 4.1868 / (3600 * 1**2) = `0.001163`
    '''
    # convertion: for convience to deal with
    symbol = _SPECIAL_UNIT.sub(_formularize_unit, symbol)
    # special dimensionless case
    if symbol in _SPECIAL_DIMENSIONLESS:
        return Compound({symbol: Fraction(1)}), \
            DimensionConst.DIMENSIONLESS, _SPECIAL_DIMENSIONLESS[symbol]
    elif symbol in _UNITS:
        return Compound({symbol: Fraction(1)}), *_UNITS[symbol]
    units = [unit for unit in _UNIT_SEP.split(symbol) if unit]
    # get exponent
    ematch_gen = (_UNIT_EXPO.search(unit) for unit in units)
    expo = Vector(1 if e is None else int(e.group()) for e in ematch_gen)
    for i, sepmatch in enumerate(_UNIT_SEP.finditer(symbol)):
        if '/' in sepmatch.group():
            expo[i + 1:] = -expo[i + 1:]
            break
    # remove exponent
    units = [_UNIT_STR.search(unit).group() for unit in units]  # type: ignore
    elements: Compound[str] = Compound({})  # merge the same items
    for unit, e in zip(units, expo):
        if e != 0:
            elements[unit] += e
    dims, vals = unzip(_resolve_elem(unit) for unit in elements)
    dimension = _sum(dim * e for dim, e in zip(dims, expo)) or \
        DimensionConst.DIMENSIONLESS
    value = _prod(val ** e for val, e in zip(vals, expo)) or 1
    # special cases, when things like 'C2/F·J' -> ''
    if dimension == DimensionConst.DIMENSIONLESS:
        elements = Compound({})
    if isinstance(value, float) and value.is_integer():
        value = int(value)
    return elements, dimension, value


def _combine(elements: Compound[str]) -> str:
    '''combine the info in the dict into a str representing the unit.'''
    symbol = '·'.join(unit + sup(e) for unit, e in elements.items() if e > 0)
    if any(e < 0 for e in elements.values()):
        symbol += '/' + \
            '·'.join(unit + sup(-e) for unit, e in elements.items() if e < 0)
        return symbol
    return _FORMULAIC_UNIT.sub(_specialize_unit, symbol)


def _deprefix(unit_elements: Compound[str]) -> tuple[Compound[str], float]:
    new_elements = unit_elements.copy()
    factor = 1
    for unit in unit_elements.keys():
        if unit in _UNITS:  # not prefixed
            continue
        e = new_elements.pop(unit)
        factor *= _PREFIX_FACTOR[unit[0]] ** e
        if len(unit) > 1:  # not a single prefix
            new_elements[unit[1:]] += e
    return new_elements, factor


def _resolve_elem(unit: str) -> tuple[Dimension, float]:
    '''resolve a single, unexponented unit str, return its 
    dimension and value (1 unit = ? SI-standard unit).
    '''
    if unit in _UNITS:
        return _UNITS[unit]
    # prefixed case
    try:
        prefix_factor = _PREFIX_FACTOR[unit[0]]
    except KeyError:
        raise UnitSymbolError(f"'{unit}' is not a valid unit.")
    # de-prefix
    nit = unit[1:]
    if nit in _UNITS:
        dim, value = _UNITS[nit]
        return dim, prefix_factor * value
    raise UnitSymbolError(f"'{unit}' is not a valid unit.")


def _formularize_unit(matchobj: re.Match[str]) -> str:
    return _FORMULARIZE[matchobj.group()]


def _specialize_unit(matchobj: re.Match[str]) -> str:
    return _SPECIALIZE[matchobj.group()]


def sup(expo: Fraction) -> str:
    '''superscript'''
    if expo.numerator < 0:
        return '⁻¹' if expo == -1 else '⁻' + sup(-expo)
    if expo == 1:
        return ''
    if expo.denominator == 1:
        return int_sup(expo.numerator)
    return int_sup(expo.numerator) + 'ᐟ' + int_sup(expo.denominator)


def int_sup(number: int) -> str:
    return ''.join(_SUPERSCRIPT[int(digit)] for digit in str(number))


class UnitSymbolError(Exception):
    pass
