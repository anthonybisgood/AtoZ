"""
language_translator.py
Zach Empkey and Anthony Bisgood
CSc 372 Proj 2
"""
import re

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
    for line in lines:
        lineArr = line.strip().split(" ")
        # if commented line
        if (lineArr[0] == '@'):
            continue
        # if assign variable
        if (lineArr[0] in VARIABLE_TYPES):
            declareVariables(line)
        # if print function
        if (line[0:4] == "show"):
            printFunction(line)
        
        
        
        

if __name__ == "__main__":
    main()
