"""
language_translator.py
Zach Empkey and Anthony Bisgood
CSc 372 Proj 2
"""

import math
import re
import sys

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
    # gets the value of the variable, removes semicolon
    value = re.search('(?<=is).*', line).group().strip()
    value = value.replace(";", "")
    type = lineArr[0].split(" ")[0]
    if (type == "int"):
        if not value.isnumeric():
            print("CANNOT CAST TYPE STRING TO INT. VALUE:%s \nLINE:%s " %(value,line))
            exit(1)
        value = eval_intExpr(value)
    if (type == "bool"):
        value = eval_boolExpr(value)
    # creates new Var object with Var type and value
    toAdd = Var(type, value)
    # adds the new variables[VarName] = Var(Type, Value)
    variables[lineArr[0].split(" ")[1]] = toAdd
    return True

    """ takes in 
    """
def eval_intExpr(line):
    expr = re.search('[^is]+$', line).group().strip()
    sol = re.findall('[a-zA-Z]+', expr)
    # if variables
    if sol:
        for el in sol:
            if (el not in variables):
                print("INVALID VARIABLE IN INTEGER EXPRESSION:", re.findall('[a-zA-Z]+', expr),
                "\nLINE:", line)
                exit(1)
            elif (el in variables):
                val = variables[el].val
                expr = expr.replace(el, val)
    try:
        res = math.floor(eval(expr))
        return res
    except:
        print("INVALID INTEGER EXPRESSION:", re.findall('[a-zA-Z]+', expr),
              "\nLINE:", line)
        exit(1)


def eval_boolExpr(expr):
    """Handles boolean expressions, can handle >, <, ==, not, and, or, and integer expresions
    in boolean expression

    Args:
        expr (String): a string representing a boolean expression

    Returns:
        Boolean: the evaluation of the boolean expression
    """
    sol = re.findall('["a-zA-Z"]+', expr)
    if sol:
        for el in sol:
            # if element is not a string
            if (el[0] == '"' and el[-1] == '"' or el == "true" or el == "false"):
                continue
            if (el in variables):
                val = variables[el].val
                expr = expr.replace(el, str(val))
            else:
                print("INVALID VARIABLE IN BOOLEAN EXPRESSION:", el,
                "\nLINE:", expr)
                exit(1)
    expr = expr.replace("&&", " and ").replace("||", " or ").replace("!", " not ").replace("true", " True ").replace("false", " False ")
    try:
        res = eval(expr)
        return res
    except:
        print("INVALID BOOLEAN EXPRESSION:", re.findall('[a-zA-Z]+', expr),
              "\nLINE:", expr)
        exit(1)


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


def ifFunction(condition):
    toRet = eval_boolExpr(condition)
    return toRet


def int_var_expr():
    """
    Getter for regex for variable and int expressions.
    :return: raw string
    """
    return r'(([\d]+|[A-Za-z]+)([ ]?)(\+|-|\*|\/)([ ]?)([\d]+|[A-Za-z]+))(([ ]?)(\+|-|\*|\/)([ ]?)([\d]+|[A-Za-z]+))*'


def bool_expr():
    """
    Getter for regex for bool expressions.
    :return: raw string
    """
    return r'(([!]?(true|false|[A-Za-z]+) (&&|\|\|) )|(([0-9A-Za-z]+) (<|>|==) )|[!]?(true|false|["A-Za-z"]+))+'


def execute_statements(stmts):
    print(stmts[0])
    while eval_boolExpr(stmts[0]):
        print(stmts[0])
        iterateLines(stmts[1:])


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
    comment_pattern = re.compile(r'^([\s]*)@([\S\s]+)')
    declare_pattern = re.compile(r'^(int|string|bool) ([A-Za-z]+) is (true|false|[0-9]+|["\s\S"]+|' + int_var_expr()
                                 + r');([\s]?)')
    print_pattern = re.compile(r'^show\((([A-Za-z]+)|"([\S\s]+)")\);$')
    conditional_pattern = re.compile(r'^(while|if) \(' + bool_expr() + r'\) \{\s?')
    condition_end_pattern = re.compile(r'}')
    while_blocks = []
    while_count = 0  # counts number of concurrent loops for tracking blocks of statements.
    condition_brackets = [] # stack of strings which represent what each { is associated with.
    in_while = False
    for i, line in enumerate(lines):
        # print(lines[i].strip("\n"))
        line = line.strip()
        if not line:
            continue
        if "}" in line:
            numConditions -= 1
        elif "{" in line:
            numConditions += 1

        if in_while:
            if condition_end_pattern:
                end_of = condition_brackets.pop()
                if end_of == "while":
                    execute_statements(while_blocks)
                    in_while = False
            else:
                while_blocks.append(line)
        elif comment_pattern.search(line) or skipLoop:
            if skipLoop:
                if "}" in line and numConditions == bracketToGet:
                    skipLoop = False
            continue
        elif if_pattern.search(line):
            condition_brackets.append("if")
            condition = re.search(r'(?<=\()(.*?)(?=\))', line).group()
            if ifFunction(condition):
                continue
            else:
                bracketToGet += numConditions - 1
                skipLoop = True
        elif while_pattern.search(line):
            in_while = True
            condition_brackets.append("while")
            condition = re.search(r'(?<=\()(.*?)(?=\))', line).group()
            while_blocks.append(condition)
        # if assign variable
        elif declare_pattern.search(line):
            if declareVariables(line) is None:
                print("ERROR!!! CANNOT NAME VARIABLES TO RESTRICTED NAMES.\nLINE:", line)
                return
        # if print function, works for both str and variable printing
        elif print_pattern.search(line):
            if printFunction(line) is None:
                print("ERROR!!! STRING FORMATTED INCORRECTLY.\nLINE:", line)
                return
        elif condition_end_pattern:
            continue
        else:
            print(f"Syntax Error in line {i+1}:\n{line}")
            sys.exit()


def main():
    # file_name = input()
    file_name = "file_test.txt"
    lines = file_handler(file_name)
    iterateLines(lines)


if __name__ == "__main__":
    main()
