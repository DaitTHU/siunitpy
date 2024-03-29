'''ConstClass is a class storing static constants.
It's similar to Enum, but members of Enum need an extra value attribute
to access its value, and I think it's unnecessary. 
So I build myEnum myself.
'''


__all__ = ['ConstMeta', 'ConstClass']


class ConstMeta(type):
    def __new__(metacls, cls, bases, attrs):  # type: ignore
        return super().__new__(metacls, cls, bases, attrs)

    def __init__(self, cls, bases, attrs):
        return super().__init__(cls, bases, attrs)
    
    def __call__(self, *args, **kwds):
        raise TypeError('Cannot instantiate Const objects.')

    def __setattr__(self, name, value):
        raise AttributeError("Cannot modify Const member.")

    def __delattr__(self, name):
        raise AttributeError("Cannot delete Const member.")


class ConstClass(metaclass=ConstMeta):
    pass 
