# mymath/utils.py
import random
from .algebra import solve_quadratic

def random_quadratic():
    """
    Генерирует случайные коэффициенты для квадратного уравнения:
    a*x² + b*x + c = 0, где a от 1 до 10 (a не может быть 0),
    b и c от -10 до 10.
    
    Возвращает кортеж (a, b, c, корни_уравнения).
    """
    a = random.randint(1, 10)
    b = random.randint(-10, 10)
    c = random.randint(-10, 10)
    roots = solve_quadratic(a, b, c)
    return (a, b, c, roots)
