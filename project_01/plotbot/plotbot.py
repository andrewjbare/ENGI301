from robot import robot

import sys
import time
import logging
import threading
from typing import Sequence

VERSION = 0.1

class Command:
    def execute(self) -> None:
        logging.info(f"Execute called on Command Superclass. ???")
        pass

    def logExecution(self) -> None:
        logging.info(f"Command {self.__class__.__name__} executed.")

class Move(Command):
    """Encompasses G0 (Rapid move) & G1 (Linear move) commands"""
    def __init__(self, X: float, Y: float) -> None:
        self.X = X
        self.Y = Y

    def execute(self) -> None:
        """Reorient & move the robot."""
        pass

class ControlledArcMove(Command):
    def __init__(self, X: float, Y: float, I: float, J: float) -> None:
        self.X = X
        self.Y = Y
        self.I = I
        self.J = J

    def execute(self) -> None:
        """Reorient & arcmove the robot."""
        pass

class Dwell(Command):
    def __init__(self, P: int) -> None:
        self.P = P

    def execute(self):
        robot.dwell(self.P)

class Bell(Command):
    def __init__(self, P: float) -> None:
        self.P = P

    def execute(self):
        robot.bell(self.P)

class Retract(Command):
    def execute(self):
        robot.retract()

class Recover(Command):
    def execute(self):
        robot.recover()


class ParseError(Exception):
    """Error while parsing the gcode file."""
    def __init__(self, message) -> None:
        self.message = message

class Parser:
    """Turns Gcode text into a list of Commands."""
    def __init__(self, gcode: list[str],
                 prepend: list[Command],
                 append: list[Command]) -> None:
        self.gcode = gcode
        self.prepend = prepend
        self.append = append
        self.commands = {
            "G0": Move,
            "G1": Move,
            "G2": ControlledArcMove,
            "G3": ControlledArcMove,
            "G4": Dwell,
            "G10": Retract,
            "G11": Recover,
            "G22": Retract,
            "G23": Recover
        }
        pass

    def parse(self) -> list[Command]:
        """Create list of Command objects representing gcode"""
        command_sequence = self.prepend # Command sequence the begins execution
        for line_number in range(len(self.gcode)):
            line = self.gcode[line_number]
            words = line.split()
            try: # Get the first word of the line and see if it's a valid command
                command = self.commands[words[0]]
            except ValueError:
                raise ParseError(
                    f"Invalid gcode command on line {line_number}: {line}"
                    ) from None
            try:
                # Get the rest of the words on the line & see if they correspond
                # to the command's arguments. Extra arguments are ignored.
                command_sequence.append(command(*words[1:]))
            except:
                raise ParseError(
                    f"Incorrect number of arguments on line {line_number}: {line}"
                    ) from None
        return []
    
class ProgramRunner:
    """Runs list of Gcode commands."""
    def __init__(self, commands: list[Command]):
        self.commands = commands
        pass

    def execute(self) -> None:
        logging.info("Beginning program execution.")
        for command in self.commands:
            command.execute()
            command.logExecution()
        logging.info("Program execution finished.")
    
if __name__ == "__main__":
    logging.info(f"plotbot.py version {VERSION}")

    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "default.nc"

    try:
        with open("filename", "r") as f:
            prepend: list[Command] = [
                Dwell(1),
                Bell(1)
            ]
            append: list[Command] = [
                Bell(1)
            ]
            gcode = f.readlines()
            commands = Parser(gcode, prepend, append).parse()
            ProgramRunner(commands).execute()
    except FileNotFoundError:
        logging.error(f"File {filename} not found, exiting.")
    
    # Load file from command line argument or default to default.nc in the
    # local directory. If not found, exit.

    # Get list of Commands from parser.

    # Execute programrunner

    # Exit
