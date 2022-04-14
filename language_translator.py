"""
language_translator.py
Zach Empkey and Anthony Bisgood
CSc 372 Proj 2
"""
import re


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


def main():
    # file_name = input()
    file_name = "file_test.txt"
    lines = file_handler(file_name)


if __name__ == "__main__":
    main()
