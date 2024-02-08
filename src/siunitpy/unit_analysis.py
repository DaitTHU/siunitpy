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
from .unit_data import (_PREFIX, _PREFIX_FULLNAME, _PREFIX_FULLNAME_MAXLEN,
                        _PREFIX_FULLNAME_MINLEN, _PREFIX_MAXLEN,
                        _SPECIAL_DIMENSIONLESS, _UNIT_DIMVAL, _UNIT_FULLNAME)
from .utilcollections import Compound
from .utilcollections.utils import _SUPERSCRIPT, _prod, _sum, neg_after
from .utilcollections.utils import superscript as sup
from .utilcollections.utils import unzip

__all__ = ['_resolve', '_combine']

_ONE = Fraction(1)

_UNIT_SEP = re.compile(r'[/.·]+')
_UNIT_EXPO = re.compile(r'[0-9+-]+$')
_UNIT_STR = re.compile(r'[^0-9 +-]+')

# special single char
_FORMULARIZE = {
    'μ': 'µ',  # u+03bc (Greek letter): u+00b5 (micro)
    '℃': '°C', '℉': '°F',
    '٪': '%', '⁒': '%',
} | {s: str(i) for i, s in enumerate(_SUPERSCRIPT)}
_SPECIAL_CHAR = re.compile(r'eV/c[2²]?|[' + ''.join(_FORMULARIZE) + ']')
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
    symbol = _SPECIAL_CHAR.sub(_formularize_unit, symbol)
    # special dimensionless case
    if symbol in _SPECIAL_DIMENSIONLESS:
        return Compound({symbol: _ONE}, move_dict=True), \
            DimensionConst.DIMENSIONLESS, _SPECIAL_DIMENSIONLESS[symbol]
    elif symbol in _UNIT_DIMVAL:
        return Compound({symbol: _ONE}, move_dict=True), *_UNIT_DIMVAL[symbol]
    # unite = unit(str) + exponent(str)
    unites = [unite for unite in _UNIT_SEP.split(symbol) if unite]
    # get exponent(str)
    expo_match_gen = (_UNIT_EXPO.search(unite) for unite in unites)
    expo = [1 if em is None else int(em.group()) for em in expo_match_gen]
    for i, sep_match in enumerate(_UNIT_SEP.finditer(symbol)):
        if '/' in sep_match.group():
            neg_after(expo, i)  # you can use ElementWiseList
            break
    # merge the same units
    elements: Compound[str] = Compound({}, move_dict=True)
    # remove exponent
    unit_match_gen = (_UNIT_STR.search(unite) for unite in unites)
    udv = unzip(_resolve_single(um.group()) for um in unit_match_gen if um)
    if not udv:  # is empty
        return elements, DimensionConst.DIMENSIONLESS, 1
    units, dims, vals = udv
    for unit, e in zip(units, expo):
        if e != 0:
            elements[unit] += e
    dimension = _sum(dim * e for dim, e in zip(dims, expo)) or \
        DimensionConst.DIMENSIONLESS
    value = _prod(val ** e for val, e in zip(vals, expo)) or 1
    # special cases, when things like 'C2/F·J' -> ''
    if dimension == DimensionConst.DIMENSIONLESS:
        elements.clear()
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


def _resolve_single(unit: str) -> tuple[str, Dimension, float]:
    '''resolve a single, unexponented unit str, return its 
    dimension and value (1 unit = ? SI-standard unit).
    '''
    if unit in _UNIT_DIMVAL:
        return unit, *_UNIT_DIMVAL[unit]
    # prefixed case
    for prefix_len in range(_PREFIX_MAXLEN):
        prefix, deprefixed_unit = unit[:prefix_len + 1], unit[prefix_len + 1:]
        if prefix == 'u':
            prefix = 'µ'
        if prefix in _PREFIX and deprefixed_unit in _UNIT_DIMVAL:
            unit = prefix + deprefixed_unit
            prefix_factor = _PREFIX[prefix].factor
            dim, value = _UNIT_DIMVAL[deprefixed_unit]
            return unit, dim, prefix_factor * value
    # fullname case
    if unit in _UNIT_FULLNAME:
        unit = _UNIT_FULLNAME[unit]
        return unit, *_UNIT_DIMVAL[unit]
    for prefix_len in range(_PREFIX_FULLNAME_MINLEN, _PREFIX_FULLNAME_MAXLEN):
        prefix, deprefixed_unit = unit[:prefix_len + 1], unit[prefix_len + 1:]
        if prefix in _PREFIX_FULLNAME and deprefixed_unit in _UNIT_FULLNAME:
            prefix = _PREFIX_FULLNAME[prefix]
            deprefixed_unit = _UNIT_FULLNAME[deprefixed_unit]
            unit = prefix + deprefixed_unit
            prefix_factor = _PREFIX[prefix].factor
            dim, value = _UNIT_DIMVAL[deprefixed_unit]
            return unit, dim, prefix_factor * value
    raise UnitSymbolError(f"'{unit}' is not a valid unit.")


def _formularize_unit(matchobj: re.Match[str]) -> str:
    return _FORMULARIZE[matchobj.group()]


def _specialize_unit(matchobj: re.Match[str]) -> str:
    return _SPECIALIZE[matchobj.group()]


class UnitSymbolError(ValueError):
    pass
