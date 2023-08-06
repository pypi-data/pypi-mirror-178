# Info, Version
def info():
    print("This is Jia Le's Python Library")
    print('This Library is Developed by Jia Le')
    
def version():
    print('Jia Le Version : v0.0.3') 
    print('Release Date : 11/28/2022')

# Basic Math Libraries.
# Math: Add, Plus (+) 
def add(num1, num2):
    return num1 + num2    

def plus(num1,num2):    
    return num1 + num2  

# Math: Substract, Minus (-)
def substract(num1, num2):
    return num1 - num2

def minus(num1, num2):
    return num1 - num2

# Math: Multiply (x, *)
def multiply(num1, num2):
    return num1 * num2

# Math: Divide (÷, /)
def divide(num1, num2):
    return num1 / num2

# Libraries of Polygon.
# Sum of Interior Angles ((n-2) x 180°)
def interior(n):
    return ((n - 2) * 180)

# Sum of Exterior Angles 
def exterior(numbers_of_side):
    return (360 / numbers_of_side)
