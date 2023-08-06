class Calculator():
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def add(self):
        return self.a + self.b

    def subtract(self):
        return self.a - self.b

    def multiply(self):
        return self.a*self.b

    def divide(self):
        return self.a/self.b

    def n_root(self):
        return self.a**(1/self.b)

    def reset(self):
        return 0

def calculator():

    print("Select operation: \n 0. Exit \n 1. Add \n 2. Subtract \n 3. Multiply \n 4. Divide \n 5. Take (n) root \n 6. Reset calculator")

    """Starting with the memory 0 and apply the selected action"""
    memory = 0

    while True:

        a = float(memory)
        """Ask what calculation action we want to do"""
        choice = input("Enter choice (0/1/2/3/4/5/6): ")

        if choice == '0':
            print("Exit")
            break

        try:
            if int(choice):
                choice = int(choice)

                if choice == 0:
                    print("Exiting!")
                    break
                elif choice == 1:
                    b = float(input("Enter your number: "))
                    obj = Calculator(a, b)
                    results = obj.add()
                    print(f"Result: {a} + {b} =", results)
                elif choice == 2:
                    b = float(input("Enter your number: "))
                    obj = Calculator(a, b)
                    results = obj.subtract()
                    print(f"Result: {a} - {b} =", results)
                elif choice == 3:
                    b = float(input("Enter your number: "))
                    obj = Calculator(a, b)
                    results = obj.multiply()
                    print(f"Result: {a} * {b} =", results)
                elif choice == 4:
                    b = float(input("Enter your number: "))
                    if b == 0:
                        print("Division from 0 is not allowed")
                        b = float(input("Enter new number: "))
                    obj = Calculator(a, b)
                    results = obj.divide()
                    print(f"Result: {a} / {b} =", results)
                elif choice == 5:
                    b = float(input("Enter your number: "))
                    if (b % 2 == 0) & (a < 0):
                        print("The square (even) root of a negative number does not exist among the set of Real Numbers")
                    else:
                        obj = Calculator(a, b)
                        results = obj.n_root()
                        print(f"Result: {a} ^(1/{b}) =", results)
                elif choice == 6:
                    obj = Calculator(a, b)
                    results = obj.reset()
                    print("Reset to:", results)
                    #results = float(input("Enter new number: "))
                else:
                    print("Invalid choice!")

                """Calculator memory"""
                memory = results
                """Let's ask if we continue another calculation action"""
                next_calculation = input("Let's do next calculation? (yes/no): ")

                if next_calculation == "yes":
                    continue
                else:
                    print("Final result = ",  memory)
                    break
        except:
            print("Choise input value should be interger")

        print()