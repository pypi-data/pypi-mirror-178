# Exceptions for nbases 

class DecimalError(Exception):
   """Rasises error, if given decimal is not suppoted."""

class BinaryError(Exception):
   """Raises error, if given binary is not supported."""

class OctalError(Exception):
   """Raises error, if given octal is not supported."""

class HexadecimalError(Exception):
   """Raises error, if given hexadecimal is not supported."""