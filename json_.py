import json
import re

def convert_type(input):
    if re.match("^[\"\']\w+[\"\']$", input):
        return input[1:-1]
    elif re.match("^0$|^[1-9]\d*$", input):
        return int(input)
    elif re.match("^0?\.\d+|[1-9]\d*\.\d+$", input):
        return float(input)
    elif re.match("^[Tt]rue$", input):
        return True
    elif re.match("^[Ff]alse$", input):
        return False
    elif input == "None":
        return None

def main():
    print("Input entry (key=value) or empty string to exit: ")
    result = dict()
    with open("result.json", "w", encoding = "utf-8") as file:
        while True:
            try:
                entry = input();
                if entry == "":
                    break
                if not re.match("^\w+=(0?\.\d+|0|[1-9]\d*(\.\d+)?|[Tt]rue|[Ff]alse|[Nn]one|[\"\']\w+[\"\'])$", entry):
                    raise ValueError(f'Invalid entry input \'{entry}\'')
                split = entry.split('=')
                key = split[0]
                value = convert_type(split[1])
                result[key] = value
            except ValueError as error:
                print(error)
        print(json.dumps(result, indent = 4))
        json.dump(result, file, indent = 4)


if __name__ == "__main__":
    main()