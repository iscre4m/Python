class Fruit:
    name = "Apple"

    def __init__(self):
        self.__name = "Kiwi"
        self.x = 10
        self.y = 20
        self.z = 30

    def __str__(self) -> str:
        return f"static: {self.name}, private: {self.__name}"

    def sum_fields(self):
        return self.x + self.y + self.z


def main():
    fruit = Fruit();
    # print(fruit)
    print(fruit.sum_fields())


if __name__ == "__main__":
    main()