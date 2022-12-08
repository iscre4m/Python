import json

def main():
    j = json.load(open("json.json"))
    print(type(j), j)


if __name__ == "__main__":
    main()