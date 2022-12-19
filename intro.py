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

def write_file():
    try:
        file = open("first.txt", "w", encoding="utf-8")
    except OSError as error:
        print(error.strerror)
    else:
        file.write("First line\n")
        file.write("Second line\n")
        file.write("Third line")
        file.flush()
        file.close()

def write_file_with():
    try:
        with open("first.txt", "w", encoding="utf-8") as file:
            file.write("First line\n")
            file.write("Second line\n")
            file.write("Third line")
    except OSError as error:
        print(error.strerror)

def main():
    # distincts()
    # print(three_distincts())
    # first_lambda = lambda x : x ** x
    # print(first_lambda(4))
    try:
        file = open("first.txt", mode = "r", encoding="utf-8")
    except FileNotFoundError as error:
        print(error.strerror)
    else:
        pass
    # pass

if __name__ == "__main__":
    # write_file(); exit()
    main()