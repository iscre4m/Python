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


def read_file() -> str | None:
    try:
        file = open("first.txt", mode = "r", encoding="utf-8")
    except FileNotFoundError as error:
        print(error.strerror)
        return None
    else:
        return file.read()
    finally:
        if file == None:
            return None
        file.close()


def read_file_with() -> str | None:
    try:
        with open("first.txt", "r", encoding="utf-8") as file:
            return file.read()
    except OSError as error:
        print(error.strerror)
        return None


def read_lines() -> None:
    try:
        with open("first.txt") as file:
            count = 1;
            for line in file.readlines():
                print(f'{count}. {line}', end="")
                count += 1
            print()
    except OSError as error:
        print(error.strerror)


def main():
    print(read_file())
    print("----------")
    print(read_file_with())
    print("----------")
    read_lines()


if __name__ == "__main__":
    # write_file(); exit()
    main()