"""Simple, reusable and optimized XOR ciphers in Python."""

__description__ = "Simple, reusable and optimized XOR ciphers in Python."
__url__ = "https://github.com/RealistikDash/xor-cipher"

__title__ = "xor_cipher"
__author__ = "RealistikDash, nekitdev"
__license__ = "MIT"
__version__ = "2.2.0"

from xor_cipher.core import (
    DEFAULT_ENCODING,
    DEFAULT_ERRORS,
    FAST,
    cyclic_xor,
    cyclic_xor_unsafe,
    cyclic_xor_string,
    cyclic_xor_string_unsafe,
    xor,
    xor_string,
)

__all__ = (
    "DEFAULT_ENCODING",
    "DEFAULT_ERRORS",
    "FAST",
    "cyclic_xor",
    "cyclic_xor_unsafe",
    "cyclic_xor_string",
    "cyclic_xor_string_unsafe",
    "xor",
    "xor_string",
)
