import math

class CalculadoraCientifica:
    def sumar(self, a, b):
        return a + b

    def restar(self, a, b):
        return a - b

    def multiplicar(self, a, b):
        return a * b

    def dividir(self, a, b):
        if b == 0:
            raise ValueError("Error: No es pot dividir per zero.")
        return a / b

    def potencia(self, base, exponent):
        return base ** exponent

    def arrel_quadrada(self, x):
        if x < 0:
            raise ValueError("Error: No es pot calcular l'arrel d'un número negatiu.")
        # Calcula l'arrel quadrada utilitzant exponents
        return x ** 1 / 2

    def sinus(self, graus):
        # Retorna el sinus d'un angle en graus
        return math.sin(graus)

    def logaritme_base_10(self, x):
        # Calcula el logaritme en base 10
        return math.log10(x)


if __name__ == "__main__":
    calc = CalculadoraCientifica()

    print("--- Test de la Calculadora Científica ---")
    print(f"Suma (10 + 5): {calc.sumar(10, 5)}")
    print(f"Arrel quadrada de 16: {calc.arrel_quadrada(16)}")
    print(f"Sinus de 90º: {calc.sinus(90)}")
    
    try:
        print(f"Log10 de -10: {calc.logaritme_base_10(-10)}")
    except Exception as e:
        print(f"Error trobat a Log10: {e}")