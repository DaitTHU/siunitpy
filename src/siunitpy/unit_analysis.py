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

from .unitelement import UnitElement
from .utilcollections import Compound
from .utilcollections.utils import _SUPERSCRIPT, neg_after
from .utilcollections.utils import superscript as sup

__all__ = ['_resolve', '_combine', '_combine_fullname']

_UNIT_SEP = re.compile(r'[/.·]+')
_UNIT_EXPO = re.compile(r'[+-]?[0-9]+$')
_REMOVE = re.compile(r'\s|\^?[+-]?[0-9]+$')

# special single char
_SPECIAL_CHAR = {
    'μ': 'µ',  # u+03bc (Greek letter): u+00b5 (micro)
    '℃': '°C', '℉': '°F',
    '٪': '%', '⁒': '%',
    "'": '′', '"': '″',
} | {s: str(i) for i, s in enumerate(_SUPERSCRIPT)}
_SPECIAL_PAT = re.compile('[{}]'.format(''.join(_SPECIAL_CHAR)))


def _resolve(symbol: str, /) -> Compound[UnitElement]:
    '''resolve the unit info from `str`, return elements of Unit.'''
    elements: Compound[UnitElement] = Compound()
    # convertion: for convience to deal with
    symbol = _SPECIAL_PAT.sub(_formularize_unit, symbol)
    # unite = unit(str) + exponent(str)
    unites = [unite for unite in _UNIT_SEP.split(symbol) if unite]
    # get exponent(str)
    expo_match_gen = (_UNIT_EXPO.search(unite) for unite in unites)
    expo = [1 if em is None else int(em.group()) for em in expo_match_gen]
    for i, sep_match in enumerate(_UNIT_SEP.finditer(symbol)):
        if '/' in sep_match.group():
            neg_after(expo, i)  # you can use ElementWiseList
            break
    # remove exponent
    unit_gen = (UnitElement(_REMOVE.sub('', unite)) for unite in unites)
    for unit, e in zip(unit_gen, expo):
        if e != 0:
            elements[unit] += e  # merge the same units
    return elements


def _combine(elements: Compound[UnitElement]) -> str:
    '''combine the info in the dict into a str representing the unit.'''
    symbol = '·'.join(u.symbol + sup(e) for u, e in elements.items() if e > 0)
    if any(e < 0 for e in elements.values()):
        symbol += '/' + \
            '·'.join(u.symbol + sup(-e) for u, e in elements.items() if e < 0)
    return symbol


def _combine_fullname(elements: Compound[UnitElement]) -> str:
    '''combine the info in the dict into a str representing the unit.'''
    symbol = '·'.join(u.fullname + sup(e) for u, e in elements.items() if e > 0)
    if any(e < 0 for e in elements.values()):
        symbol += '/' + \
            '·'.join(u.fullname + sup(-e) for u, e in elements.items() if e < 0)
    return symbol


def _formularize_unit(matchobj: re.Match[str]) -> str:
    return _SPECIAL_CHAR[matchobj.group()]
