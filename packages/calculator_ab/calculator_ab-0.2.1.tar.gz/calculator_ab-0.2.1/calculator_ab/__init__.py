"""A calculator."""

__version__ = "0.2.1"


class Calculator:
    """Performs a math operation with two numbers.
    Input numbers are integers.
    """

    def __init__(self):
        self.result = 0

    def add(self, value):
        """Adds two numbers"""
        self.value = value
        self.result += self.value
        return self.result

    def subtract(self, value):
        """Subtracts one number from another"""
        self.value = value
        self.result -= self.value
        return self.result

    def multiply(self, value):
        """Multiplies two numbers"""
        self.value = value
        self.result *= self.value
        return self.result

    def divide(self, value):
        """Divides one number from another"""
        self.value = value
        self.result /= self.value
        return self.result

    def n_root(self, value):
        """Takes n root of a number"""
        self.value = value
        self.result = self.result ** (1 / self.value)
        return self.result

    def reset(self):
        """Resets the memory"""
        self.result = 0
        return self.result


calc = Calculator()
k = calc.add(5)
print(k)
k = calc.add(4)
print(k)
k = calc.subtract(2)
print(k)
k = calc.multiply(2)
print(k)
k = calc.reset()
print(k)
k = calc.add(10)
print(k)
