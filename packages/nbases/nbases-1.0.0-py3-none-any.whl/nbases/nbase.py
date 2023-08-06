# nbases - number cases conversion

from .errors import (
   DecimalError, 
   BinaryError, 
   OctalError, 
   HexadecimalError,
)

BINARY = ("0", "1")
OCTAL = ("0", "1", "2", "3", "4", "5", "6", "7")
DECIMAL = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
HEX = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", 
       "A", "B", "C", "D", "E", "F",
       "a", "b", "c", "d", "e", "f")

__all__ = ["Decimal", "Binary", "Octal", "Hex"]


class Decimal:
   """Decimal Conversion
   
   Converts any decimal (base 10) to binary, octal or hex. This class
   takes two parameter. First is '`decimal`' argument and this argument
   must be string .In other situations, raises `DecimalError`. Second 
   is  '`max_pow`' that represents biggest number (like 2**100, 8**100
   or 16**100). that must be bigger than '`decimal`'.

   """
   def __init__(self, decimal, max_pow=500):
      
      self.decimal = decimal
      # Before process given decimal, fixes some issues.
      # Given decimal must be in string.
      if not isinstance(self.decimal, str):
         raise TypeError("'decimal' argument must be str")

      # Given decimal must not contain spaces.
      self.decimal = self.decimal.replace(" ", "")

      # Given decimal just can contain '.' and decimal numbers.
      for char in self.decimal:
         if char not in DECIMAL and char != '.':
            error_msg = "inconsistent decimal: '{}'".format(char)
            raise DecimalError(error_msg)
      
      # Seperates given decimal into three part
      self.part1, self.part2, self.part3 = self.decimal.partition(".")

      # It is maximum pow value.
      self.pow = max_pow
      if self.pow < 0:
         raise ValueError("'max_pow' argument is not operatable")

   def to_binary(self):
      """Converts decimal to binary form. For example:
      
      ### Example 1
      >>> result = Decimal('1071').to_binary()
      >>> print(result)
      '10000101111'

      ### Example 2
      >>> result = Decimal('54.75').to_binary()
      >>> print(result)
      '110110.11'

      """
      _binary, _part1, _pow = "", float(self.part1), self.pow
      # This loop provides finding left side of binary.
      while True:
         if 2 ** _pow > _part1: 
            _binary += "0"
            _pow -= 1
         else:
            _binary += "1"
            _part1 -= 2 ** _pow
            _pow -= 1
         # Breaks up the loop.
         if _pow < 0: break
      # If given decimal has fraction, this code block finds right 
      # side of binary.
      if self.part2 == ".":
         _part3 = float(self.part3) / (10 ** len(self.part3))
         # At the end, adds an '.' character.
         _binary += '.' 
         while True:
            if 2 ** _pow <= _part3:
               _binary += "1"
               _part3 -= 2 ** _pow
               _pow -= 1
            else:
               _binary += "0"
               _pow -= 1
            # Breaks up the loop.
            if _pow < -500: break
         # Fixes right side of created binary
         _binary = _binary[:_binary.rindex("1")+1]
      # Fixes left side of created binary
      _binary = _binary[_binary.index("1"):]
         
      return _binary

   def to_octal(self):
      """Converts decimal to octal form. For example:
      
      ### Example 1
      >>> result = Decimal('54.75').to_octal()
      >>> print(result)
      '66.6'

      ### Example 2
      >>> result = Decimal('1453').to_octal()
      >>> print(result)
      '2655'

      """
      _octal, _part1, _pow = "", float(self.part1), self.pow
      # This loop provides finding left side of binary.
      while True:
         if 8 ** _pow > _part1:
            _octal += "0"
            _pow -= 1
         else:
            _octal += str(int(_part1 / 8 ** _pow))
            _part1 -= (8 ** _pow) * int(_part1 / 8 ** _pow)
            _pow -= 1
         # Breaks up the loop.
         if _pow < 0: break
      # If given decimal has fraction, this code block finds right 
      # side of binary.
      if self.part2 == ".":
         _part3 = float(self.part3) / (10 ** len(self.part3))
         # At the end, adds an '.' character.
         _octal += '.' 
         while True:
            if 8 ** _pow < _part3:
               _octal += str(int(_part3 / 8 ** _pow))
               _part3 -= (8 ** _pow) * int(_part3 / 8 ** _pow)
               _pow -= 1
            else:
               _octal += "0"
               _pow -= 1
            # Breaks up the loop.
            if _pow < -500: break
      # Fixes right and left side of created binary
      while True:
         if _octal[0] == "0": _octal = _octal[1:]
         elif _octal[-1] == "0": _octal = _octal[:-1]
         else: break

      return _octal

   def to_hex(self):
      """Converts decimal to hexadecimal form. For example:
      
      ### Example 1
      >>> result = Decimal("218.625").to_hex()
      >>> print(result)
      'DA.A'

      ### Example 2
      >>> result = Decimal("1071").to_hex()
      >>> print(result)
      '42F'

      """
      _hexd, _part1, _pow = "", float(self.part1), self.pow
      # There are also A, B, C, D, E, F chars in hexadecimal.
      def _hex(part, pow):
         # Returns appropriate char according to calculation.   
         if int(part / 16 ** pow) == 10: return "A"
         elif int(part / 16 ** pow) == 11: return "B"
         elif int(part / 16 ** pow) == 12: return "C"
         elif int(part / 16 ** pow) == 13: return "D"
         elif int(part / 16 ** pow) == 14: return "E"
         elif int(part / 16 ** pow) == 15: return "F"
         else: return str(int(part / 16 ** pow))
      # This loop provides finding left side of binary.
      while True:
         if 16 ** _pow > _part1:
            _hexd += "0"
            _pow -= 1
         else:
            _hexd += _hex(_part1, _pow)
            _part1 -= (16 ** _pow) * int(_part1 / 16 ** _pow)
            _pow -= 1
         # Breaks up the loop.
         if _pow < 0: break
      # If given decimal has fraction, this code block finds right 
      # side of binary.
      if self.part2 == ".":
         _part3 = float(self.part3) / (10 ** len(self.part3))
         # At the end, adds an '.' character.
         _hexd += '.' 
         while True:
            if 16 ** _pow < _part3:
               _hexd += _hex(_part3, _pow)
               _part3 -= (16 ** _pow) * int(_part3 / 16 ** _pow)
               _pow -= 1
            else:
               _hexd += "0"
               _pow -= 1
            # Breaks up the loop.
            if _pow < -500: break
      # Fixes right and left side of created binary
      while True:
         if _hexd[0] == "0": _hexd = _hexd[1:]
         elif _hexd[-1] == "0": _hexd = _hexd[:-1]
         else: break

      return _hexd


class Binary:
   """Binary Conversion
   
   Converts any binary (base 2) to decimal, octal or hex. This class
   takes two parameter. First is '`binary`' argument and this argument
   must be string .In other situations, raises `BinaryError`. Second 
   is  '`max_pow`' that represents biggest number (like 8**100, 10**100
   or 16**100). that must be bigger than '`binary`'.

   """
   def __init__(self, binary, max_pow=500):
      
      self.binary = binary
      # Before process given binary, fixes some issues.
      # Given binary must be in string.
      if not isinstance(self.binary, str):
         raise TypeError("'binary' argument must be str")

      # Given binary must not contain spaces.
      self.binary = self.binary.replace(" ", "")

      # Given binary just can contain '.' and binary numbers.
      for char in self.binary:
         if char not in BINARY and char != '.':
            error_msg = "inconsistent binary: '{}'".format(char)
            raise BinaryError(error_msg)
      
      # Seperates given binary into three part
      self.part1, self.part2, self.part3 = self.binary.partition(".")

      # It is maximum pow value.
      self.pow = max_pow
      if self.pow < 0:
         raise ValueError("'max_pow' argument is not operatable")

   def to_decimal(self):
      """Convert binary to decimal form. For example:
      
      ### Example 1
      >>> result = Binary('10110101101').to_decimal()
      >>> print(result)
      '1453'

      ### Example 2
      >>> result = Binary('110110.11').to_decimal()
      >>> print(result)
      '54.75'

      """
      _decimal, _decimal1, _pow = "", 0, len(self.part1)-1
      # This loop provides finding left side of decimal.
      for bin in self.part1:
         _decimal1 += int(bin) * (2 ** _pow)
         _pow -= 1
         # Breaks up the loop.
         if _pow == -1: break
      # If given binary has fraction, this code block finds right 
      # side of decimal.
      if self.part2 == '.':
         _decimal2, _pow, _starter = 0, -(len(self.part3)+1), -1
         # This loop provides finding right side of decimal.
         for bin in self.part3:
            _decimal2 += int(bin) * (2 ** _starter)
            _starter += -1
            # Breaks up the loop.
            if _starter == _pow: break
      # Lastly, concats two side.
      if self.part2 == '.': _decimal += str(_decimal1 + _decimal2)
      else: _decimal += str(_decimal1)

      return _decimal

   def to_octal(self):
      """Convert binary to octal form. For example:
      
      ### Example 1
      >>> result = Binary('10110101101').to_octal()
      >>> print(result)
      '2655'

      ### Example 2
      >>> result = Binary('110110.11').to_octal()
      >>> print(result)
      '66.6'

      """
      # Uses Decimal class.
      return Decimal(self.to_decimal(), self.pow).to_octal()

   def to_hex(self):
      """Convert binary to hexadecimal form. For example:
      
      ### Example 1
      >>> result = Binary('10110101101').to_hex()
      >>> print(result)
      '5AD'

      ### Example 2
      >>> result = Binary('110110.11').to_hex()
      >>> print(result)
      '36.C'

      """
      # Uses Decimal class.
      return Decimal(self.to_decimal(), self.pow).to_hex()


class Octal:
   """Octal Conversion
   
   Converts any octal (base 8) to decimal, binary or hex. This class
   takes two parameter. First is '`octal`' argument and this argument
   must be string .In other situations, raises `OctalError`. Second 
   is  '`max_pow`' that represents biggest number (like 2**100, 10**100
   or 16**100). that must be bigger than '`octal`'.

   """
   def __init__(self, octal, max_pow=500):
      
      self.octal = octal
      # Before process given octal, fixes some issues.
      # Given octal must be in string.
      if not isinstance(self.octal, str):
         raise TypeError("'octal' argument must be str")

      # Given octal must not contain spaces.
      self.octal = self.octal.replace(" ", "")

      # Given octal just can contain '.' and octal numbers.
      for char in self.octal:
         if char not in OCTAL and char != '.':
            error_msg = "inconsistent octal: '{}'".format(char)
            raise OctalError(error_msg)
      
      # Seperates given octal into three part
      self.part1, self.part2, self.part3 = self.octal.partition(".")

      # It is maximum pow value.
      self.pow = max_pow
      if self.pow < 0:
         raise ValueError("'max_pow' argument is not operatable")

   def to_decimal(self):
      """Convert octal to decimal form. For example:
      
      ### Example 1
      >>> result = Octal('2057').to_decimal()
      >>> print(result)
      '1071'

      ### Example 2
      >>> result = Octal('332.5').to_decimal()
      >>> print(result)
      '218.625'

      """
      _decimal, _decimal1, _pow = "", 0, len(self.part1)-1
      # This loop provides finding left side of decimal.
      for bin in self.part1:
         _decimal1 += int(bin) * (8 ** _pow)
         _pow -= 1
         # Breaks up the loop.
         if _pow == -1: break
      # If given octal has fraction, this code block finds right 
      # side of decimal.
      if self.part2 == '.':
         _decimal2, _pow, _starter = 0, -(len(self.part3)+1), -1
         # This loop provides finding right side of decimal.
         for bin in self.part3:
            _decimal2 += int(bin) * (8 ** _starter)
            _starter += -1
            # Breaks up the loop.
            if _starter == _pow: break
      # Lastly, concats two side.
      if self.part2 == '.': _decimal += str(_decimal1 + _decimal2)
      else: _decimal += str(_decimal1)

      return _decimal

   def to_binary(self):
      """Convert octal to binary form. For example:
      
      ### Example 1
      >>> result = Octal('2057').to_binary()
      >>> print(result)
      '10000101111'

      ### Example 2
      >>> result = Octal('332.5').to_binary()
      >>> print(result)
      '11011010.101'

      """
      # Uses Decimal class.
      return Decimal(self.to_decimal(), self.pow).to_binary()

   def to_hex(self):
      """Convert octal to hexadecimal form. For example:
      
      ### Example 1
      >>> result = Octal('2057').to_hex()
      >>> print(result)
      '42F'

      ### Example 2
      >>> result = Octal('332.5').to_hex()
      >>> print(result)
      'DA.A'

      """
      # Uses Decimal class.
      return Decimal(self.to_decimal(), self.pow).to_hex()


class Hex:
   """Hexadecimal Conversion
   
   Converts any hexadecimal (base 8) to decimal, binary or octal. This
   class takes two parameter. First is '`hex`' argument and must be
   string .In other situations, raises `HexadecimalError`. Second is
   '`max_pow`' that represents biggest number (like 2**100, 8**100 or
   10**100). that must be bigger than '`hex`'.

   """
   def __init__(self, hex, max_pow=500):
      
      self.hex = hex
      # Before process given hexadecimal, fixes some issues.
      # Given hexadecimal must be in string.
      if not isinstance(self.hex, str):
         raise TypeError("'hex' argument must be str")

      # Given hexadecimal must not contain spaces.
      self.hex = self.hex.replace(" ", "")

      # Given hexadecimal just can contain '.' and octal numbers.
      for char in self.hex:
         if char not in HEX and char != '.':
            error_msg = "inconsistent hexadecimal: '{}'".format(char)
            raise HexadecimalError(error_msg)
      
      # Seperates given hexadecimal into three part
      self.part1, self.part2, self.part3 = self.hex.partition(".")

      # It is maximum pow value.
      self.pow = max_pow
      if self.pow < 0:
         raise ValueError("'max_pow' argument is not operatable")

   def to_decimal(self):
      """Convert hexadecimal to decimal form. For example:
      
      ### Example 1
      >>> result = Hex('5Ad').to_decimal()
      >>> print(result)
      '1453'

      ### Example 2
      >>> result = Hex('36.C').to_decimal()
      >>> print(result)
      '54.75'

      """
      _decimal, _decimal1, _pow = "", 0, len(self.part1)-1
      # There are also A, B, C, D, E, F chars in hexadecimal.
      def _hex(bin):
         # Returns appropriate number according to 'bin' argument.   
         if bin == "A" or bin == "a": return 10
         elif bin == "B" or bin == "b": return 11
         elif bin == "C" or bin == "c": return 12
         elif bin == "D" or bin == "d": return 13
         elif bin == "E" or bin == "e": return 14
         elif bin == "F" or bin == "f": return 15
         else: return int(bin)
      # This loop provides finding left side of decimal.
      for bin in self.part1:
         _decimal1 += _hex(bin) * (16 ** _pow)
         _pow -= 1
         # Breaks up the loop.
         if _pow == -1: break
      # If given hexadecimal has fraction, this code block finds right 
      # side of decimal.
      if self.part2 == '.':
         _decimal2, _pow, _starter = 0, -(len(self.part3)+1), -1
         # This loop provides finding right side of decimal.
         for bin in self.part3:
            _decimal2 += _hex(bin) * (16 ** _starter)
            _starter += -1
            # Breaks up the loop.
            if _starter == _pow: break
      # Lastly, concats two side.
      if self.part2 == '.': _decimal += str(_decimal1 + _decimal2)
      else: _decimal += str(_decimal1)

      return _decimal

   def to_binary(self):
      """Convert hexadecimal to binary form. For example:
      
      ### Example 1
      >>> result = Hex('5Ad').to_binary()
      >>> print(result)
      '10110101101'

      ### Example 2
      >>> result = Hex('36.C').to_binary()
      >>> print(result)
      '110110.11'

      """
      # Uses Decimal class.
      return Decimal(self.to_decimal(), self.pow).to_binary()

   def to_octal(self):
      """Convert hexadecimal to octal form. For example:
      
      ### Example 1
      >>> result = Hex('5Ad').to_octal()
      >>> print(result)
      '2655'

      ### Example 2
      >>> result = Hex('36.C').to_octal()
      >>> print(result)
      '66.6'

      """
      # Uses Decimal class.
      return Decimal(self.to_decimal(), self.pow).to_octal()