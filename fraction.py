import math

class Fraction:
    def __init__(self, numerator=0, denominator=1):
        self.set_numerator(numerator)
        self.set_denominator(denominator)

    def get_numerator(self):
        return self.__numerator

    def set_numerator(self, value):
        try:
            self.__numerator = 0
            self.__numerator = float(value)
        except ValueError:
            print(f"'{value}' is not a number")

    def get_denominator(self):
        return self.__denominator

    def set_denominator(self, value):
        try:
            self.__denominator = 1
            value = float(value)
            if value == 0:
                raise ZeroDivisionError
        except ValueError:
            print(f"'{value}' is not a number")
        except ZeroDivisionError:
            print("Denominator cannot be zero")
        else:
            self.__denominator = value

    def __str__(self) -> str:
        int_num = int(self.__numerator)
        numerator = int_num \
        if int_num == self.__numerator \
        else self.__numerator

        int_den = int(self.__denominator)
        denominator = int_den \
        if int_den == self.__denominator \
        else self.__denominator

        return f"{numerator}/{denominator}"

    def float_value(self) -> float:
        return self.__numerator / self.__denominator

    def reduce(self):
        int_num = int(self.__numerator)
        int_den = int(self.__denominator)
        if int_num == self.__numerator \
        and int_den == self.__denominator:
            gcd = math.gcd(int_num, int_den)
            if gcd > 1:
                self.__numerator /= gcd
                self.__denominator /= gcd

def main():
    fraction = Fraction("12", 0)
    print(fraction.get_denominator())
    fraction.set_numerator(16)
    fraction.set_denominator("2.5")
    print(fraction)
    print(fraction.float_value())
    fraction.reduce()
    print(fraction)
    fraction.set_denominator(4)
    fraction.reduce()
    print(fraction)

if __name__ == "__main__":
    main()