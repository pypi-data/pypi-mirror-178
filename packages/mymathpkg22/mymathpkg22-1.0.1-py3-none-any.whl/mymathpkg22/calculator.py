import math

class Calculator():
    """Calculator module makes simply mathematical operations:
        addition, 
        substraction,
        multiplication,
        division and
        nth root
    
    Give inputs using float data structure.
    """
    def __init__(self):
        """Initializing the calculator object with starting value 0"""
        self._value : float = 0.0
        
    def _is_float(self, number: float) -> bool:
        """ Checks that functions are served with floats. 
        Returns True or False."""
        try:
            float(number)
            if math.isnan(number):
                print(f'''The provided value: {number} is not a number. 
                      Give new value that is a float.''')
                return False
            else:
                return True
        except (TypeError, ValueError):
            print(f'''The provided input "{number}" is not a float. 
                  Give new input that is a float.''')
            return False        
        
    def add(self, number: float) -> float:
        """Add given number to the calculator value
            
            For example:
                >>> example = Calculator()
                >>> example.add(2)
                2.0
                
        """
        if self._is_float(number):
            self._value += number
        return self._value
    
    def subtract(self, number: float) -> float:
        """Subtract given number from the calculator value
            
            For example:
                >>> example = Calculator()
                >>> example.subtract(2)
                -2.0
                
        """
        if self._is_float(number):
            self._value -= number
        return self._value
        
    def multiply(self, number: float) -> float:
        """Multiply the calculator value by given number
            
            For example:
                >>> example = Calculator()
                >>> example.add(2)
                2.0
                >>> example.multiply(2)
                4.0
                
        """
        if self._is_float(number):
            self._value *= number
        return self._value
    
    def divide(self, number: float) -> float:
        """Divide the calculator value by given number
            
            For example:
                >>> example = Calculator()
                >>> example.add(2)
                2.0
                >>> example.divide(2)
                1.0
                
        """
        if self._is_float(number):
            if number == 0:
                print("Zero Division: float division by zero.")
                print("Give a non-zero value for division.")
                return self._value
            self._value /= number
        return self._value

    def nth_root(self, number: float) -> float:
        """Nth root of the calculator value when N is the given number
            
            For example:
                >>> example = Calculator()
                >>> example.add(2)
                2.0
                >>> example.nth_root(2)
                4.0
                
        """
        if self._is_float(number):
            if number < 0 and self._value == 0:
                print("Zero Division:")
                print("Zero can not be raised to a negative power. Give a non-negative value.")
                return self._value
            self._value **= number
        return (self._value)
    
    def reset_memory(self) -> float:
        """Reset the calculator value to zero.
            
            For example:
                >>> example = Calculator()
                >>> example.add(2)
                2.0
                >>> example.reset_memory()
                0.0
                
        """
        self._value = 0.0
        return self._value
    
if __name__ == '__main__':

    import doctest
    
    print(doctest.testmod())