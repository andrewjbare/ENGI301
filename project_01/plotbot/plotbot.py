# Script for running robot

import threading
import logging
import sys

import parse
from robot import robot

if __name__ == "__main__":
    program_file = sys.argv[1]
    program = parse.parse(program_file)
    for command in program:
        print(f"Executing {str(command)}... ", end="")
        command.execute()
        print("Done.")
    print("Program execution complete.")