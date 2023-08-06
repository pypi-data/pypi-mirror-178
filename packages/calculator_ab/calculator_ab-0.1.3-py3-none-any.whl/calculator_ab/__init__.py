"""A calculator.
Performs a math operation with two numbers.
Input numbers are floats.
"""

__version__ = "0.1.3"


class Calculator:

    def __init__(self, number_1: float, number_2: float):
        self.number_1 = number_1
        self.number_2 = number_2

    def addition(self):
        """Adds two numbers"""
        return self.number_1 + self.number_2

    def subtraction(self):
        """Subtracts one number from another"""
        return self.number_1 - self.number_2

    def multiplication(self):
        """Multiplies two numbers"""
        return self.number_1 * self.number_2

    def division(self):
        """Divides one number from another"""
        return self.number_1 / self.number_2

    def n_root(self):
        """Takes n root of a number"""
        return self.number_1 ** (1 / user_number_2)

    def action(self, user_action):
        """All possible actions:
        +, -, *, /, r"""
        if user_action == '+':
            return self.addition()
        elif user_action == '-':
            return self.subtraction()
        elif user_action == '*':
            return self.multiplication()
        elif user_action == '/':
            return self.division()
        elif user_action == 'r':
            return self.n_root()


print('*' * 60)
print("CALCULATOR")
print('*' * 60)
print("To Reset press C, to Quit - Q")
print('*' * 60)

print("Calculator examples:"
      "\n 2 + 2 -> 4 | Addition"
      "\n 7 - 2 -> 5 | Subtraction"
      "\n 2 * 4 -> 8 | Multiplication"
      "\n 9 / 3 -> 3 | Division"
      "\n 8 r 3 -> 2 | N root")
print('*' * 60)
print("Enter your calculation: \n")

k = 0
memory = 0
further = True
while further:

    if k == 0:
        user_input = input()
        user_input = user_input.strip().split(' ')

        if user_input[0].lower() == 'q':
            further = False
            print('*' * 60)
            print("Closing Calculator")
            break
        if user_input[0].lower() == 'c':
            memory = 0
            continue

        user_number_1 = float(user_input[0])
        action = user_input[1]
        user_number_2 = float(user_input[2])

        calc = Calculator(user_number_1, user_number_2)
        result = calc.action(action)

    else:
        user_input = input(f"{memory}")
        user_input = user_input.strip().split(' ')

        if user_input[0].lower() == 'q':
            further = False
            print('*' * 60)
            print("Closing Calculator")
            break
        if user_input[0].lower() == 'c':
            memory = 0
            continue

        action = user_input[0]
        user_number_2 = float(user_input[1])

        calc = Calculator(memory, user_number_2)
        result = calc.action(action)

    memory = result
    k += 1
