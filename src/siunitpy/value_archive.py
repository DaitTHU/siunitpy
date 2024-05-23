# math constants

PI = 3.1415926535897932384626
'''the ratio of the circumference of a circle to its diameter'''
WEIN_ZERO = 4.965114231744276303698759131322893944
'''solution of: x = 5*(1 - exp(-x)); x = 5 + LambertW(-5*exp(-5))'''
WEIN_F_ZERO = 2.82143937212207889340319133
'''solution of: x = 3*(1 - exp(-x)); x = 3 + LambertW(-3*exp(-3))'''

# degree

DEGREE = PI / 180
ARCMIN = DEGREE / 60
ARCSEC = ARCMIN / 60

# time

MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR
SIMPLE_YEAR = 365 * DAY
'''1 simple year = 365 day [s]'''
JULIAN_YEAR = SIMPLE_YEAR + DAY // 4
'''1 Julian year = 365.25 day [s]'''

# physical constants

C = 299_792_458
'''speed of light [m/s]'''
ELC = 1.602176634e-19
'''elementary charge [C]'''

AU = 149597870700
'''astronomical unit [m]'''
PC = AU / ARCSEC
'''parsec [m]'''
LIGHT_YEAR = C * JULIAN_YEAR
'''1 ly = c * 1 yr [m]'''
DALTON = 1.660_539_068_92e-27
'''1 Dalton = mass(12C) / 12'''
EV = ELC
'''electron volt'''
GRAVITY = 9.80665
'''standard acceleration of gravity [m/s2]'''
KELVIN_ZERO = 273.15
'''Kelvin zero point'''
ATM = 101325
'''standard atmosphere [Pa]'''
SSP = 100000
'''standard-state pressure [Pa]'''
MMHG = ATM / 760
'''1 mmHg = 1 atm / 760 [Pa]'''
KCAL = 4184
'''kilo-calorie [J]'''
CAL = KCAL / 1000
'''calorie [J]'''
