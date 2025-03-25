# mymath/geometry.py
import math

def circle_area(radius):
    """
    Вычисляет площадь круга по формуле: π * r².
    """
    if radius < 0:
        raise ValueError("Радиус не может быть отрицательным.")
    return math.pi * radius ** 2
