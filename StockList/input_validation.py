def input_int(prompt="Please Enter a number: ", err="Invalid Please enter a whole number", gt=None, ge=None, lt=None,
              le=None):
    while True:
        try:
            val = int(input(prompt))
            if gt is not None and val <= gt:
                print(F"Value must be greater than {gt}!")
            elif ge is not None and val < ge:
                print(F"Value must be greater than or equal to {ge}!")
            elif lt is not None and val >= lt:
                print(F"Value must be less than {lt}!")
            elif le is not None and val > le:
                print(F"Value must be less than or equal to {le}!")
            else:
                return val
        except ValueError:
            print(err)


def input_float(prompt="Please Enter a number: ", err="Invalid Please enter a whole number", gt=None, ge=None, lt=None,
                le=None):
    while True:
        try:
            val = float(input(prompt))
            if gt is not None and val <= gt:
                print(F"Value must be greater than {gt}!")
            elif ge is not None and val < ge:
                print(F"Value must be greater than or equal to {ge}!")
            elif lt is not None and val >= lt:
                print(F"Value must be less than {lt}!")
            elif le is not None and val > le:
                print(F"Value must be less than or equal to {le}!")
            else:
                return val
        except ValueError:
            print(err)


def valid_or_invalid(string):
    return bool(string.strip())


def input_string(prompt="Please enter a non-numeric string: ", err="err try again: ", valid_function=valid_or_invalid):
    while True:
        try:
            user_input = input(prompt)
            if valid_function(user_input):
                return user_input
        except ValueError:
            print(err)


def y_or_n(prompt="Please enter yes or no:", err="err try again: "):
    while True:
        user_input = input(prompt)
        user_input = user_input.lower()
        if user_input == "y" or user_input == "yes":
            return True
        elif user_input == "n" or user_input == "no":
            return False


def select_item(prompt="Please type yes or no: ", error="Answer must be yes or no!", choices=["Yes", "No"], map=None):
    value_dict = {}
    for choice in choices:
        value_dict[choice.lower()] = choice
    if map is not None:
        for key in map:
            value_dict[key.lower()] = map[key]
    while True:
        val = input(prompt).lower()
        if val in value_dict:
            return value_dict[val]
        print(error)


