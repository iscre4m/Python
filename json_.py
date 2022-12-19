import json
import re

def convert_type(input):
    if re.match("^[\"\']\w+[\"\']$", input): # на входе строка по типу 'data' или "data"
        return input[1:-1] # убираем кавычки
    elif re.match("^0$|^[1-9]\d*$", input): # 0, 17, 23, ...
        return int(input)
    elif re.match("^0?\.\d+|[1-9]\d*\.\d+$", input): # 0.0023, .17, 12.7, ...
        return float(input)
    elif re.match("^[Tt]rue$", input): # true | True
        return True
    elif re.match("^[Ff]alse$", input): # false | False
        return False
    elif re.match("^[Nn]one$"): # none | None
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
