from math_operations import add, multiply, random_sqrt_sum
import random

def main():
    print("Демонстрация работы random_sqrt_sum() из модуля math_operations:")
    result = random_sqrt_sum()
    print("Результат random_sqrt_sum():", result)
    
    # Бонусное задание:
    print("\nБонусное задание:")
    # Генерируем два случайных числа от 1 до 100
    num1 = random.randint(1, 100)
    num2 = random.randint(1, 100)
    print("Сгенерированные случайные числа:", num1, "и", num2)
    
    # Применяем multiply() к сгенерированным числам
    product = multiply(num1, num2)
    print("Произведение двух чисел:", product)
    
    # Используем add() для объединения произведения с результатом random_sqrt_sum()
    bonus_result = add(product, random_sqrt_sum())
    print("Результат сложения произведения с random_sqrt_sum():", bonus_result)

if __name__ == "__main__":
    main()
