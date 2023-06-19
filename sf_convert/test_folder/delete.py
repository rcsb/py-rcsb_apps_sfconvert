# class MyClass:
#     def __init__(self):
#         self.__private_var = 10

#     def another_method(self):
#         print(self.__private_var)  # Accessing the private variable inside another method

# # Usage:
# obj = MyClass()
# obj.another_method()  # This will print '10'


class Test:
    def __init__(self):
        setattr(self, '_Test__private', 'Value')

    def print_private(self):
        print(self.__private)

t = Test()
t.print_private()  # Prints 'Value'
