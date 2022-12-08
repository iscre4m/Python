def distincts() -> list:
    while True:
        try:
            x = input("Input first number: ")
            x = int(x)
            if x < 0:
                raise Exception("Number below zero");
            break
        except ValueError:
            print("Not a number")
        except Exception as ex:
            print(ex)
    
    while True:
        try:
            y = input("Input second number: ")
            y = int(y)
            if y < 0:
                raise Exception("Number below zero")
            break;
        except ValueError:
            print("Not a number")
        except Exception as ex:
            print(ex)

    print("Numbers are equal") if x == y else print("Numbers are not equal")
    
    return x, y


def three_distincts() -> list:
    while True:
        try:
            x = input("Input first number: ")
            x = int(x)
            if x < 0:
                raise Exception("Number below zero");
            break
        except ValueError:
            print("Not a number")
        except Exception as ex:
            print(ex)

    while True:
        try:
            y = input("Input second number: ")
            y = int(y)
            if y < 0:
                raise Exception("Number below zero")
            if y == x:
                raise Exception("Number is not unique")
            break;
        except ValueError:
            print("Not a number")
        except Exception as ex:
            print(ex)

    while True:
        try:
            z = input("Input third number: ")
            z = int(z)
            if z < 0:
                raise Exception("Number below zero")
            if z == x or z == y:
                raise Exception("Number is not unique")
            break;
        except ValueError:
            print("Not a number")
        except Exception as ex:
            print(ex)

    return [x, y, z]


def main():
    # distincts()
    print(three_distincts())


if __name__ == "__main__":
    main()