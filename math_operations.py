import math as m
import random

def add(a, b):
    """Возвращает сумму двух чисел."""
    return a + b

def multiply(a, b):
    """Возвращает произведение двух чисел."""
    return a * b

def random_sqrt_sum():
    """
    Генерирует случайное целое число от 1 до 100,
    вычисляет его квадратный корень и возвращает сумму числа и его квадратного корня.
    """
    num = random.randint(1, 100)
    return num + m.sqrt(num)