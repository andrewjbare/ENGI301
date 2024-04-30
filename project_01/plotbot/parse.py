import sys
import logging
import math

from robot import robot

class Peekable:
    def __init__(self, input):
        self._input = input
        self._index = 0

    def __iter__(self):
        return self
    
    def next(self):
        if self._index < len(self._input):
            character = self._input[self._index]
            self._index += 1
            print(character, end="")
            return character
        else:
            raise StopIteration
        
    def peek(self):
        if self._index < len(self._input):
            character = self._input[self._index]
            return character
        else:
            return None
        
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f"({self.type}, {self.value})"

class ParseError(Exception):
    """Error while parsing the gcode file."""
    def __init__(self, message) -> None:
        self.message = message
    
class Lexer:
    def __init__(self, stream):
        self.stream = stream
        self.tokens = []

    def skip_comment(self):
        while True:
            character = self.stream.next()
            if character == ")":
                break

    def read_number(self):
        number = []
        valid = [".", "-"]
        while True:
            character = self.stream.next()
            next = self.stream.peek()
            if character.isnumeric() or character in valid:
                number.append(character)
            if not next.isnumeric() and not next in valid:
                return "".join(number)

                

    def read_next(self):
        character = self.stream.next()
        ignore = [" ", "\n"]
        if character in ignore:
            return
        elif character == "(":
            self.skip_comment()
        elif character.isalpha():
            number = self.read_number()
            self.tokens.append(Token(character, number))
        else:
            message = "Unexpected character " + character
            raise ParseError(message)
            
    
    def read(self):
        while True:
            try:
                self.read_next()
            except StopIteration:
                print("Tokenizing finished")
                break

class Command:
    def __init__(self, args: dict[str, int]):
        self.args = args

    def __str__(self):
        return f"{type(self).__name__}({self.args})"
        
    def execute(self) -> None:
        logging.info(f"Execute called on Command Superclass. ???")
        pass

    def logExecution(self) -> None:
        logging.info(f"Command {self.__class__.__name__} executed.")


class Move(Command):
    """Encompasses G0 (Rapid move) & G1 (Linear move) commands"""
    def __init__(self, args) -> None:
        super().__init__(args)
        if "X" in self.args and "Y" in self.args:
            self.dX = float(self.args["X"]) - robot.X
            self.dY = float(self.args["Y"]) - robot.Y
            try:
                self.absolute_angle = math.degrees(math.atan(self.dY / self.dX))
            except ZeroDivisionError:
                self.absolute_angle = 0 if self.dY > 0 else -180 # yowza
            self.distance = math.sqrt(self.dX ** 2 + self.dY ** 2)
            self.dZ = 0

        elif "Z" in self.args:
            self.dZ = float(self.args["Z"]) - robot.Z
            self.absolute_angle = 0
            self.distance = 0
        
        # Future: add arc moves
    
    def execute(self) -> None:
        """Reorient & move the robot."""
        robot.reorient(self.absolute_angle)
        robot.move(self.distance)
        robot.zmove(self.dZ)


# class ControlledArcMove(Command):
#     def __init__(self, X: float, Y: float, I: float, J: float) -> None:
#         self.X = X
#         self.Y = Y
#         self.I = I
#         self.J = J

#         self.dX = self.args["X"] - robot.X
#         self.dY = self.args["Y"]- robot.Y
#         self.absolute_angle = math.degrees(math.atan(self.dY / self.dX))

#     def execute(self) -> None:
#         """Reorient & arcmove the robot."""
#         robot.reorient(self.absolute_angle)
        

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

class Ignore(Command):
    """Rationale here is that some (many) commands can be ignored for MVP but
    might someday be useful to handle - better to acknowledge them than squash them"""
    pass

class Parser:
    def __init__(self, tokens):
        self.tokens = Peekable(tokens)
        self.commands = {
            "G00": Move,
            "G01": Move,
            "G02": Move, # Future ControlledArcMove
            "G03": Move, # Future ContorlledArcMove
            "G04": Dwell,
            "G53": Ignore, # CNC plane select (irrelevant)
            "G54": Ignore, # CNC plane select (irrelevant)
            "G55": Ignore, # CNC plane select (irrelevant)
            "G56": Ignore, # CNC plane select (irrelevant)
            "G57": Ignore, # CNC plane select (irrelevant)
            "G58": Ignore, # CNC plane select (irrelevant)
            "G59": Ignore, # CNC plane select (irrelevant)
            "G90": Ignore, # Absolute positioning. Relative positioning not supported.
            "M3": Ignore,
            "M05": Ignore,
            "M30": Ignore
        }
        self.program = []

    def is_command(self, token) -> bool:
        if token == None:
            return False
        return token.type in ["G", "M"]

    def parse_command(self, token):
        command_name = token.type + token.value
        try:
            command = self.commands[command_name]
            arguments = {}
            while True:
                if self.is_command(self.tokens.peek()):
                    return command(arguments)
                else: # next token is an argument to command
                    arg_token = self.tokens.next()
                    arguments[arg_token.type] = arg_token.value
        except KeyError:
            raise ParseError(f"Command {command_name} is invalid or not supported.")
    
    def parse_token(self):
        token = self.tokens.next()
        if self.is_command(token):
            self.program.append(self.parse_command(token))
        else:
            raise ParseError(f"Unexpected token {str(token)}")
        
    def parse(self):
        while True:
            try:
                self.parse_token()
            except StopIteration:
                print("parse finished")
                return self.program
            
def parse(filename) -> list[Command]:

    with open(filename, "r") as f:
        gcode = "".join(f.readlines())
        stream = Peekable(gcode)
        lexer = Lexer(stream)
        lexer.read()
        parser = Parser(lexer.tokens)
        return parser.parse()

        
if __name__ == "__main__":
    filename = "square.nc"

    try:
        with open(filename, "r") as f:
            gcode = "".join(f.readlines())
            stream = Peekable(gcode)
            lexer = Lexer(stream)
            lexer.read()
            print("Tokens:")
            print(list(map(str, lexer.tokens)))
            parser = Parser(lexer.tokens)
            program = parser.parse()
            print("Program:")
            print(list(map(str, program)))
    except FileNotFoundError:
        print("File not found.")
        sys.exit()