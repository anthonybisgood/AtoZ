"""
language_translator.py
Zach Empkey and Anthony Bisgood
CSc 372 Proj 2
"""
import re

RESTRICTED_NAMES = ["string", "int", "bool", "if", "while", "is"]
VARIABLE_TYPES = ["string", "int", "bool"]
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
    lineArr = line.strip().split("is")
    if (lineArr[0].split(" ")[1]) in RESTRICTED_NAMES:
        return None
    # gets the value of the variable
    value = re.search('[^is]+$', line).group().strip()
    type = lineArr[0].split(" ")[0]
    if (type == "int"):
        eval_intExpr(value)
    # creates new Var object with Var type and value
    toAdd = Var(type, value)
    # adds the new variables[VarName] = Var(Type, Value)
    variables[lineArr[0].split(" ")[1]] = toAdd
    return True

def eval_intExpr(expr):
    print(expr)


# show(x);
# show("Hello World!");
def printFunction(line):
    # print string
    if (line[5] == '"'):
        toPrint = re.search('(?<=")(.*?)(?=")', line)
        if toPrint == None:
            return None
        print(toPrint.group())
    else:
        variableName = re.search('(?<=\()(.*?)(?=\))', line).group()
        if (variableName not in variables):
            print("Variable name inputed is not a valid variable")
            return
        print(variables[variableName].val)
    return True

# TODO: Finish function
def ifFunction(line):
    if (line == 'True'):
        return True
    return False


def iterateLines(lines):
    """Iterates over teh lines in the output of given code.

    Args:
        lines (array): an array of code given as strings 
    """
    skipLoop = False
    # if we have to skip over if statements inside of if statements, keep track of
    # which level you are in
    bracketToGet = 0
    numConditions = 0
    for i in range(len(lines)):
        # print(lines[i].strip("\n"))
        line = lines[i].strip()
        if not line:
            continue
        
        if ("}" in line):
            numConditions -= 1
        elif ("{" in line):
            numConditions += 1
        
        if (line[0] == '@' or skipLoop):
            if (skipLoop):
                if ("}" in line and numConditions == bracketToGet):
                    skipLoop = False
            continue
        if (line[0:2] == "if"):
            condition = re.search('(?<=\()(.*?)(?=\))', line).group()
            if ifFunction(condition) == True:
                continue
            else:
                bracketToGet += numConditions - 1
                skipLoop = True
            
        lineArr = line.strip().split(" ")
        # if assign variable
        if (lineArr[0] in VARIABLE_TYPES):
            if declareVariables(line) == None:
                print("ERROR!!! CANNOT NAME VARIABLES TO RESTRICTED NAMES.\nLINE:",line)
                return
        # if print function, works for both str and variable printing
        if (line[0:4] == "show"):
            if printFunction(line) == None:
                print("ERROR!!! STRING FORMATED INCORRECTLY.\nLINE:",line)
                return
            

            


def main():
    # file_name = input()
    file_name = "file_test.txt"
    lines = file_handler(file_name)
    iterateLines(lines)
            
        
        
        
        
        

if __name__ == "__main__":
    main()
