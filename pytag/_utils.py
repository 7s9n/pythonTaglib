from ctypes import(
    POINTER,
    Structure,
    c_int
)
def to_byte_str(value: str)-> bytes:
    if not isinstance(value, (str, bytes)):
        value = str(value)
    return value.encode('utf-8', 'ignore') if isinstance(value, str) else value

def to_python_str(value: bytes)-> str:
    return value.decode('utf-8', 'ignore') if isinstance(value, bytes) else value

def to_int(value: float)-> int:
    return int(value) if isinstance(value, float) else value

def wrap_function(_tl, funcname, argtypes= None, restype= None):
    """Simplify wrapping ctypes functions"""
    func = _tl.__getattr__(funcname)
    func.restype = restype
    func.argtypes = argtypes
    return func

# Type utils
class _File(Structure):
    _fields_ = [
        ('dummy', c_int),
    ]

class _Tag(Structure):
    _fields_ = [
        ('dummy', c_int),
    ]

class _AudioProperties(Structure):
    _fields_ = [
        ('dummy', c_int),
    ]

_FilePtr = POINTER(_File)
_TagPtr = POINTER(_Tag)
_AudioPropertiesPtr = POINTER(_AudioProperties)