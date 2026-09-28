# Calculator Functions - Hotfix Division Version

def add(a, b):
    """Function to add two numbers"""
    return a + b

def subtract(a, b):
    """Function to subtract two numbers"""
    return a - b

def divide(a, b):
    """Function to divide two numbers safely"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
