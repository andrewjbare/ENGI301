"""
--------------------------------------------------------------------------
plotbot.py
--------------------------------------------------------------------------
License:   
Copyright 2024 - Andrew Bare

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, 
this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF 
THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------
"""

from robot import robot

import sys
import logging
import math

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
        self.dX = X - robot.X
        self.dY = Y - robot.Y
        self.absolute_angle = math.degrees(math.atan(self.dY / self.dX))
        self.distance = math.sqrt(self.dX ** 2 + self.dY ** 2)

    def execute(self) -> None:
        """Reorient & move the robot."""
        robot.reorient(self.absolute_angle)
        robot.move(self.distance)

class ControlledArcMove(Command):
    def __init__(self, X: float, Y: float, I: float, J: float) -> None:
        self.X = X
        self.Y = Y
        self.I = I
        self.J = J

        self.dX = X - robot.X
        self.dY = Y - robot.Y
        self.absolute_angle = math.degrees(math.atan(self.dY / self.dX))

    def execute(self) -> None:
        """Reorient & arcmove the robot."""
        robot.reorient(self.absolute_angle)
        

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
            # TODO: See how well this error handling works - might need
            # improvement/pen testing for bad gcode files. Anticipate bugs here
            try: # Get the first word of the line and see if it's a valid command
                command = self.commands[words[0]]
            except ValueError:
                raise ParseError(
                    f"Invalid gcode command on line {line_number}: {line}"
                    ) from None
            try:
                # Get the rest of the words on the line & see if they correspond
                # to the command's arguments. Extra arguments will throw an
                # error, but in the future this should be handled behavior (ignored)
                command_sequence.append(command(*words[1:]))
            except:
                raise ParseError(
                    f"Incorrect number of arguments on line {line_number}: {line}"
                    )
            
        command_sequence.extend(self.append)
        return command_sequence
    
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

    logging.info("Exiting.")
    
    # Load file from command line argument or default to default.nc in the
    # local directory. If not found, exit.

    # Get list of Commands from parser.

    # Execute programrunner

    # Exit
