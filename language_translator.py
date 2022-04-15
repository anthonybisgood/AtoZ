"""
language_translator.py
Zach Empkey and Anthony Bisgood
CSc 372 Proj 2
"""
import re
import sys

VARIABLE_TYPES = {"string", "int", "bool"}
# contains the name of the variable and the type and the value
# varName:(type, value)
variables = {}


class Var:
    def __init__(self, type, val):
        self.type = type
        self.val = val
        

def file_handler(file_name):
    """
    Separates the file into individual lines. Newlines are maintained.
    :param file_name: Name of the file
    :return: A list of strings
    """
    try:
        with open(file_name) as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("File not found. Ensure that the file is in the same directory and that the name was typed without"
              " errors.")
    return lines


# string x = "hello";
# bool y = True;
# int z = 1234;
def declareVariables(line):
    # splits line into array around =
    lineArr = line.strip().split("=")
    # gets the value of the variable
    value = re.search('[^=]+$', line).group().strip()
    # creates new Var object with Var type and value
    toAdd = Var(lineArr[0].split(" ")[0], value)
    # adds the new variables[VarName] = Var(Type, Value)
    variables[lineArr[0].split(" ")[1]] = toAdd


# show(x);
# show("Hello World!");
def printFunction(line):
    # print string
    if (line[5] == '"'):
        toPrint = re.search('(?<=")(.*?)(?=")', line)
        print(toPrint.group())
    else:
        variableName = re.search('(?<=\()(.*?)(?=\))', line).group()
        print(variables[variableName].val)


def main():
    # file_name = input()
    file_name = "file_test.txt"
    lines = file_handler(file_name)
    for i, line in enumerate(lines):
        lineArr = line.strip().split(" ")
        comment_pattern = re.compile(r'^@([\S\s]+)')
        declare_pattern = re.compile(r'^(Int|String|Bool) ([A-Za-z]+) = (true|false|[0-9]+|"[\s\S]+");([\s]?)')
        print_pattern = re.compile(r'^show\((([A-Za-z]+)|"([\S\s]+)")\);$')
        conditional_pattern = re.compile(r'^(while|if) \((([!]?(true|false|[A-Za-z]+) (&&|\|\|) [!]?(true|false|[A-Za-z]+))|'
                                         r'(([0-9A-Za-z]+) (<|>|==) ([0-9A-Za-z]+))|[!]?(true|false|[A-Za-z]+))\) {\s?')
        boolexpr_pattern = re.compile(r'(([!]?(true|false|[A-Za-z]+) (&&|\|\|) [!]?(true|false|[A-Za-z]+))|'
                                      r'(([0-9A-Za-z]+) (<|>|==) ([0-9A-Za-z]+))|[!]?(true|false|[A-Za-z]+))')
        # if commented line
        if comment_pattern.search(line):
            continue
        # if assign variable
        elif declare_pattern.search(line):
            declareVariables(line)
        # if print function
        elif print_pattern.search(line):
            printFunction(line)
        # TODO conditionals
        elif conditional_pattern.search(line):
            pass
        else:
            print(f"Syntax Error in line {i+1}:\n{line}")
            sys.exit()


if __name__ == "__main__":
    main()
