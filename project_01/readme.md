<h1>PlotBot</h1>
PlotBot is a robot (+ gcode parser/interpreter/etc) that can plot arbitrary images from gcode on a PocketBeagle. It uses only the Adafruit_BBIO library to interface with the PocketBeagle's GPIO pins.

<h1>Usage</h1>
To use, call plotbot.py with a gcode (typically, .nc) file. The robot will parse and run the gcode from there. Errors are printed directly to console. If no file is provided, nothing will happen. This software is meant specifically for the robot described at [https://www.hackster.io/ajbare224/plotbot-d3e337](https://www.hackster.io/ajbare224/plotbot-d3e337)

<h1>Build Instructions/Notes</h1>
Run the accompanying config.sh file to set up the PocketBeagle's GPIO pins for use by the Python scripts. No other major prep is necessary. If running automatically on a robot, create & set the file before running.

<h1>Software</h1>
There are a few notable differences between this software and tradtional CNC software:
- Feedrate is rather unimportant. As long as the robot gets where it needs to go in a reasonable time, I'm happy. This is in contrast to e.g. a CNC mill for which very precise feedrate is desired.
- The dynamics of the system are a little weird. In order to change direction, the robot must either perform a controlled arc move (G2/G3, not yet implemented), or stop & change its direction, likely lifting the pen to do so. Software is simplified considerably if the pen is placed directly between the wheels of the robot (it can simply turn on a dime), so this was assumed for PlotBot. It still means that each straight-line move command (G0/G1) must usually also include a turn - something traiditonal CNC programs can do, but with an interface overcomplicated for this application (e.g., suitable for a 5-axis CNC).

<h2>Description</h2>
The software consists of three major parts:
plotbot.py - runs the actual program. This is 50% complete and still needs to implement some fo the features described on Hackster.
parse.py - ingests gcode (.nc file) and returns a program (list of command objects) that can be easily carried out by the main program
robot.py - represents the actual robot. This class is designed so that all of the implementation-specific information lives here, rather than in the main program.

<h1>Future Work</h1>
Future work will make this program more feature-rich, including more commands, more convenient operation and better error handling.