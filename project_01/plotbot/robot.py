"""
--------------------------------------------------------------------------
robot.py - singleton robot implementation (wip)
--------------------------------------------------------------------------
License:   
Copyright 2024 - Andrew Bare

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------
"""

import Adafruit_BBIO.GPIO as GPIO

import time
import math

STEP_LENGTH = 1 # Empirical value that must be set once we get the actual length of a step on the robot

class Stepper:
    def __init__(self, pins, states):
        # TODO: Figure out what type pin numbers will be/how to access
        self.pins = pins
        self.states = states

        # The current stepper state; "lead pin" is the first one energized on a step
        self.lead_pin = 0

        # Setup GPIO pins for output & set low
        for pin in self.pins:
            print(f"GPIO setup {pin}")
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)

    def write_pins(self, values):
        """Write values to pins.
        
        If values is the wrong length, a ValueError should be thrown
        automatically. This method makes the step() method on subclasses much
        more concise."""
        for i in range(len(self.pins)):
            pin = self.pins[i]
            print("GPIO output")
            GPIO.output(pin, GPIO.HIGH if values[i] else GPIO.LOW)

    def step(self):
        """Perform one step."""
        self.write_pins(self.states[self.lead_pin])
        # Increment lead pin so the next run steps to the next state. If we've
        # hit the end of states, go back to state 0.
        if self.lead_pin < len(self.states) - 1:
            self.lead_pin += 1
        else:
            self.lead_pin = 0
        

class Robot:
    """Robot contains all of the atomic implementations of robot actions that
    compose the commands defined in main."""
    def __init__(self, left_stepper, right_stepper):
        self.X = 0
        self.Y = 0
        self.Z = 0
        self.orientation = 0 # Right-handed orientation [deg]
        self.left_stepper = left_stepper
        self.right_stepper = right_stepper

    def reorient(self, absolute_angle):
        pass

    def move(self, distance):
        step_count = math.floor(distance / STEP_LENGTH)
        for i in range(1, step_count):
            self.left_stepper.step()
            self.right_stepper.step()

    def zmove(self, distance) -> None:
        """Move the pen (Z)"""
        pass


stepper_states = [
            [1, 0, 0, 0],
            [1, 1, 0, 0],
            [0, 1, 0, 1],
            [0, 1, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 1],
            [0, 0, 0, 1],
            [1, 0, 0, 1]
        ]

# TODO: Replace with config file params?
left_stepper = Stepper(["P1_29", "P1_31", "P1_33", "P1_35"], stepper_states)
right_stepper = Stepper(["P1_30", "P1_32", "P1_34", "P1_36"], stepper_states)
robot = Robot(left_stepper, right_stepper)