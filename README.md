# siunitpy

SI-Unit-Py is a Python package for dealing with units. 

This package implements [NIST (National Institute of Standards and Technology)](https://www.nist.gov/pml/owm/metric-si/si-units) 
official unit definitions. 

Moreover, it introduce uncertainty.

## Installation

pip installable package: [pypi: siunitpy](https://pypi.org/project/siunitpy/)

```shell
pip install siunitpy
```

## Quickstart: module `siunitpy.SI`

import module `siunitpy.SI` to use 3 very useful classes: `SI`, `si` and `prefix`.

### `SI`: common physical constants

use physical constants through class `SI`:

```python
>>> from siunitpy.SI import SI
>>> SI.c
Constant(value=299792458, uncertainty=0, unit=m/s)
>>> print(SI.me)
9.1093837015e-31 ± 2.8e-40 kg
>>> print(SI.me * SI.c**2)
8.187105776823886e-14 ± 2.516514500463089e-23 J
```

constant class `SI` provide physical constants defined by (or derived from) SI unit system.

### `si`: common SI units

use units through class `si`:

```python
>>> from siunitpy.SI import si
>>> print(1 * si.kg * si.m / si.s**2)
1.0 N
>>> print(760 * si.mmHg.to("Pa"))
101325.0 Pa
```

### `prefix`: unit prefix factor

class `prefix` contains prefix from quetta(Q, = 1e30) to quecto(q, = 1e-30), and byte prefix like ki(2^10, 1024), Mi(2^20), Gi(2^30)... It's just a number factor, not Quantity.
```python
>>> from siunitpy.SI import prefix
>>> prefix.mega
1000000.0
>>> prefix.Pi  # 2**50
1125899906842624
```

## Define Quantity

import `siunit` to define a `Quantity` object:
```python
>>> from siunitpy import Quantity
>>> F = Quantity(1, 'kg.m/s2')
>>> L = Quantity(1, 'm', 1e-4)  # with uncertainty
```

where `F` is a Quantity object, and it has properties:

```python
>>> F.value
1
>>> F.unit
Unit(kg·m/s², dim=T⁻²LM, value=1)
>>> F.dimension
Dimension(T=-2, L=1, M=1, I=0, H=0, N=0, J=0)
>>> L.uncertainty
1e-4
```

objects in `SI` are also Quantity objects.

Quantity objects can make unit conversion and operate with number or Quantity:

```python
>>> print(SI.me.to("keV/c2"))  # unit conversion
510.99894999616424 ± 1.5706848090652466e-07 keV/c²
>>> print(F / (1 * si.m)**2)
1.0 Pa
```
