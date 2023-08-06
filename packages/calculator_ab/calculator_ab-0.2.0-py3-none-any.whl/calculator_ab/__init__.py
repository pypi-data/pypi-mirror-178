"""A calculator."""

__version__ = "0.2.0"


class Calculator:
    """Performs a math operation with two numbers.
    Input numbers are floats.
    """

    def __init__(self, memory: float, number_2: float):
        self.memory = memory
        self.number_2 = number_2

    def add(self):
        """Adds two numbers"""
        return self.memory + self.number_2

    def sub(self):
        """Subtracts one number from another"""
        return self.memory - self.number_2

    def multi(self):
        """Multiplies two numbers"""
        return self.memory * self.number_2

    def div(self):
        """Divides one number from another"""
        return self.memory / self.number_2

    def n_root(self):
        """Takes n root of a number"""
        return self.memory ** (1 / self.number_2)

    def reset(self):
        """Resets the memory"""
        self.memory = 0

calc = Calculator
k = calc.add(5)
print(k)




    # def action(self, user_action):
    #     """All possible actions:
    #     +, -, *, /, r"""
    #     if user_action == "+":
    #         return self.addition()
    #     if user_action == "-":
    #         return self.subtraction()
    #     if user_action == "*":
    #         return self.multiplication()
    #     if user_action == "/":
    #         return self.division()
    #     if user_action == "r":
    #         return self.n_root()
    #     return None


# print("*" * 60)
# print("CALCULATOR")
# print("*" * 60)
# print("To Reset press C, to Quit - Q")
# print("*" * 60)
#
# print(
#     "Calculator examples:"
#     "\n 2 + 2 -> 4 | Addition"
#     "\n 7 - 2 -> 5 | Subtraction"
#     "\n 2 * 4 -> 8 | Multiplication"
#     "\n 9 / 3 -> 3 | Division"
#     "\n 8 r 3 -> 2 | N root"
# )
# print("*" * 60)
# print("Enter your calculation: \n")
#
# k = 0
# MEMORY = 0
# FURTHER = True
# while FURTHER:
#
#     if k == 0:
#         user_input = input().strip().split(" ")
#
#         if user_input[0].lower() == "q":
#             FURTHER = False
#             print("*" * 60)
#             print("Closing Calculator")
#             break
#         if user_input[0].lower() == "c":
#             MEMORY = 0
#             continue
#
#         user_number_1 = float(user_input[0])
#         action = user_input[1]
#         user_number_2 = float(user_input[2])
#
#         calc = Calculator(user_number_1, user_number_2)
#         result = calc.action(action)
#
#     else:
#         user_input = input(f"{MEMORY}").strip().split(" ")
#
#         if user_input[0].lower() == "q":
#             FURTHER = False
#             print("*" * 60)
#             print("Closing Calculator")
#             break
#         if user_input[0].lower() == "c":
#             MEMORY = 0
#             continue
#
#         action = user_input[0]
#         user_number_2 = float(user_input[1])
#
#         calc = Calculator(MEMORY, user_number_2)
#         result = calc.action(action)
#
#     MEMORY = result
#     k += 1
