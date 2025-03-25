import math

def solve_quadratic(a, b, c):
    """
    Решает квадратное уравнение ax² + bx + c = 0.
    
    Возвращает кортеж с корнями. Если дискриминант отрицательный, возвращаются комплексные корни.
    """
    if a == 0:
        raise ValueError("Коэффициент 'a' не может быть равен 0 для квадратного уравнения.")
    
    discriminant = b**2 - 4*a*c
    if discriminant >= 0:
        root1 = (-b + math.sqrt(discriminant)) / (2*a)
        root2 = (-b - math.sqrt(discriminant)) / (2*a)
        return (root1, root2)
    else:
        real_part = -b / (2*a)
        imaginary_part = math.sqrt(-discriminant) / (2*a)
        return (complex(real_part, imaginary_part), complex(real_part, -imaginary_part))