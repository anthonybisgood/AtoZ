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
    """A class that stores the type and value of the variable.
    """
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
            if (lines):
                return lines
    except FileNotFoundError:
        print("File not found. Ensure that the file is in the same directory and that the name was typed without"
              " errors.")
    return 


def declareVariables(line):
    """Function for declaring variables in our language. Stores variables by name:(type, value)
    if the class Var. Also performs type checking to and variable name checking to make sure
    that you cant declare a variable from another variable that hasnt been declared yet.
    Examples:
        string x = "hello";
        bool y = True;
        int z = 1234;
        int a = z-23;
    Args:
        line (String): The current line of the variable we want to declare, written in 
        our new language
    Returns:
        Boolean: True or None depending on if the operation succeded
    """
    # splits line into array around =
    lineArr = line.strip().split("is")
    if (lineArr[0].split(" ")[1]) in RESTRICTED_NAMES:
        return None
    # gets the value of the variable, removes semicolon
    value = re.search('(?<=is).*', line).group().strip()
    value = value.replace(";", "")
    type = lineArr[0].split(" ")[0]
    if (type == "int"):
        value = eval_intExpr(value)
    if (type == "bool"):
        value = eval_boolExpr(value)
    if (type == "string"):
        value = eval_string(value)
    # creates new Var object with Var type and value
    toAdd = Var(type, value)
    # adds the new variables[VarName] = Var(Type, Value)
    variables[lineArr[0].split(" ")[1]] = toAdd
    return True

def eval_string(line):
    if ('"' not in line):
        if (line in variables):
            return variables[line].val
    return line

def eval_intExpr(line):
    """Evaluates integer expressions and can handle +,-,*,/,and % operations. Uses eval function
    to evaluate and return an integer.
    Args:
        line (String): The current line of the variable we are performing integer evaluation on.
    Returns:
        int: the result of our line parameter
    """
    expr = re.search('[^is]+$', line).group().strip()
    sol = re.findall('[a-zA-Z]+', expr)
    # if variables
    if sol:
        for el in sol:
            if (el not in variables):
                print("INVALID VARIABLE IN INTEGER EXPRESSION:", el, "\nLINE:", line)
                exit(1)
            elif (el in variables):
                val = variables[el].val
                if (variables[el].type != "int"):
                    print(f"CANNOT ADD INTEGER AND ANY OTHER TYPE: {el}\nLINE: {line}")
                    exit(1)
                expr = expr.replace(el, str(val))
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
    """When called, prints out the line 
    Args:
        line (String): The line, including show() that we are going to print
    Returns:
        Boolean/None: True if it works, none if formated incorrectly
    """
    line = re.search('(?<=\()(.*?)(?=\))', line).group()
    # print string
    if (line[0] == '"' and line[-1] == '"'):
        toPrint = re.search('(?<=")(.*?)(?=")', line)
        if toPrint == None:
            return None
        print(toPrint.group())
        return True
    # print variable
    elif (line in variables):
        print(variables[line].val)
        return True
    return None


def ifFunction(condition):
    toRet = eval_boolExpr(condition)
    return toRet


def int_var_expr():
    """
    Getter for regex for variable and int expressions.
    :return: raw string
    """
    return r'(([\d]+|[A-Za-z]+)([ ]?)(\+|-|\*|\/|\%)([ ]?)([\d]+|[A-Za-z]+))(([ ]?)(\+|-|\*|\/|\%)([ ]?)([\d]+|[A-Za-z]+))*'


def bool_expr():
    """
    Getter for regex for bool expressions.
    :return: raw string'
    """
    return r'(([!]?(true|false|"([\S\s]+)"|[0-9A-Za-z]+) (&&|\|\|) )|' \
           r'(("([\S\s]+)"|[0-9A-Za-z]+) (<|>|==|>=|<=|-|\+|\*|\/|%) )|' \
           r'([!]?(true|false|"([\S\s]+)"|[0-9A-Za-z]+)))+'


def execute_statements(stmts):
    """Used for while loops, stmts[0] is the conditional that we iterate through until it is false.
    stmts[1:] are the lines residing inside the while loop including other while loops. Iterates over
    the list and calls iterateLines with the statements inside the while loop
    Args:
        stmts (List[String]): a list of strings representing the commands to run
    """
    #print(f"condition: {stmts[0]}")
    #print(f"other stuff: {stmts[1:]}")
    while eval_boolExpr(stmts[0]):
        iterateLines(stmts[1:])


def iterateLines(lines):
    """Iterates over teh lines in the output of given code.
    Args:
        lines (array): an array of code given as strings
    """
    argNum = 0
    skipLoop = False
    # if we have to skip over if statements inside of if statements, keep track of
    # which level you are in
    bracketToGet = 0
    numConditions = 0
    comment_pattern = re.compile(r'^([\s]*)@([\S\s]+)')
    declare_pattern = re.compile(r'^(int|string|bool) ([A-Za-z]+) is (true|false|[0-9]+|["\s\S"]+|' + int_var_expr()
                                 + r');([\s]?)')
    print_pattern = re.compile(r'^show\((([A-Za-z]+)|"([\S\s]+)")\);$')
    if_pattern = re.compile(r'^(if) \(' + bool_expr() + r'\) \{\s?')
    while_pattern = re.compile(r'^(while) \(' + bool_expr() + r'\) \{\s?')
    condition_end_pattern = re.compile(r'^}$')
    arg_pattern = re.compile(r'^arg\(([A-Za-z]+)\);$')
    
    while_blocks = []
    condition_brackets = [] # stack of strings which represent what each { is associated with.
    in_while = False
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        if "}" in line:
            numConditions -= 1
        elif "{" in line:
            numConditions += 1
        if comment_pattern.search(line) or skipLoop:
            if skipLoop:
                if "}" in line and numConditions == bracketToGet:
                    skipLoop = False
            continue
        elif in_while:
            if numConditions == 0:
                end_of = condition_brackets.pop()
                if end_of == "while":
                    execute_statements(while_blocks)
                    in_while = False
            else:
                while_blocks.append(line)
        # if we hit a while loop
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
        elif if_pattern.search(line):
            condition_brackets.append("if")
            condition = re.search(r'(?<=\()(.*?)(?=\))', line).group()
            if ifFunction(condition):
                continue
            else:
                bracketToGet += numConditions - 1
                skipLoop = True
        elif arg_pattern.search(line):
            # 2 is type, 3 is value
            arg_type = sys.argv[2 + argNum*2]
            arg_val  = sys.argv[3 + argNum*2]
            arg_var  = re.search(r'(?<=\()(.*?)(?=\))', line).group()
            assign_line = f"{arg_type} {arg_var} is {arg_val};"
            argNum = argNum + 1
            if declareVariables(assign_line) is None:
                print("ERROR!!! CANNOT NAME VARIABLES TO RESTRICTED NAMES.\nLINE:", line)
                return
        elif condition_end_pattern.search(line):
            continue
        else:
            print(while_blocks)
            print(f"Syntax Error in line {i+1}:\n{line}")
            sys.exit()

def main():
    if (len(sys.argv) > 1):
        file_name = sys.argv[1]
    else:
        file_name = "test.txt"
    lines = file_handler(file_name)
    iterateLines(lines)


if __name__ == "__main__":
    main()
