def run():
    n = int(input("🔢 Ingresa n: "))

    if n < 0:
        raise ValueError("n debe ser >= 0")

    result = 1

    for i in range(1, n + 1):
        result *= i

    return result