"""A calculator."""

__version__ = "0.3.0"


class Calculator:
    """Performs a math operation with two numbers.
    Input numbers are floats.
    """

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
        if user_action == "+":
            return self.addition()
        if user_action == "-":
            return self.subtraction()
        if user_action == "*":
            return self.multiplication()
        if user_action == "/":
            return self.division()
        if user_action == "r":
            return self.n_root()
        return None


print("*" * 60)
print("CALCULATOR")
print("*" * 60)
print("To Reset press C, to Quit - Q")
print("*" * 60)

print(
    "Calculator examples:"
    "\n 2 + 2 -> 4 | Addition"
    "\n 7 - 2 -> 5 | Subtraction"
    "\n 2 * 4 -> 8 | Multiplication"
    "\n 9 / 3 -> 3 | Division"
    "\n 8 r 3 -> 2 | N root"
)
print("*" * 60)
print("Enter your calculation: \n")

k = 0
MEMORY = 0
FURTHER = True
while FURTHER:

    if k == 0:
        user_input = input().strip().split(" ")

        if user_input[0].lower() == "q":
            FURTHER = False
            print("*" * 60)
            print("Closing Calculator")
            break
        if user_input[0].lower() == "c":
            MEMORY = 0
            continue

        user_number_1 = float(user_input[0])
        action = user_input[1]
        user_number_2 = float(user_input[2])

        calc = Calculator(user_number_1, user_number_2)
        result = calc.action(action)

    else:
        user_input = input(f"{MEMORY}").strip().split(" ")

        if user_input[0].lower() == "q":
            FURTHER = False
            print("*" * 60)
            print("Closing Calculator")
            break
        if user_input[0].lower() == "c":
            MEMORY = 0
            continue

        action = user_input[0]
        user_number_2 = float(user_input[1])

        calc = Calculator(MEMORY, user_number_2)
        result = calc.action(action)

    MEMORY = result
    k += 1
