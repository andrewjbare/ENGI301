import Adafruit_GPIO as GPIO

class Stepper:
    def __init__(self, pins):
        # TODO: Figure out what type pin numbers will be/how to access
        self.pins = pins

        # The current stepper state; "lead pin" is the first one energized on a step
        self.lead_pin = 0

        # Setup GPIO pins for output & set low
        for pin in pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)

class FullStepper(Stepper):
    def __init__(self, pins):
        super().__init__(pins)

    def step(self):
        """Perform one full step (2 phases on). This means 4 states:
        PIN       0 1 2 3
        STATE 1:  1 1 0 0
        STATE 2:  0 1 1 0
        STATE 3:  0 0 1 1
        STATE 4:  1 0 0 1
        """
        pass


class HalfStepper(Stepper):
    def __init__(self, pins):
        super().__init__(pins)
        

    def step(self):
        """Perform one half step (2 phases on). This means 8 states:
        PIN       0 1 2 3
        STATE 1:  1 0 0 0
        STATE 2:  1 1 0 0
        STATE 3:  0 1 0 0
        STATE 4:  0 1 1 0
        STATE 5:  0 0 1 0
        STATE 6:  0 0 1 1
        STATE 7:  0 0 0 1
        STATE 8:  1 0 0 1
        """
        pass


class Robot:
    def __init__(self, left_stepper: Stepper, right_stepper: Stepper) -> None:
        self.position = [0, 0] # Position x, y [in]
        self.orientation = 0 # Right-handed orientation [deg]
        self.left_stepper = left_stepper
        self.right_stepper = right_stepper

    def reorient(self, absolute_angle: float) -> None:
        pass

    def move(self, distance: float):
        pass

    def arcmove(self, distance: float, angle: float) -> None:
        """Move distance arclength and end at an angle differing by angle"""
        pass

    def dwell(self, P: int) -> None:
        """Wait P milliseconds"""
        pass

    def bell(self, P: float) -> None:
        """Sound the buzzer (default 1 second)"""
        pass

    def retract(self) -> None:
        """Retract the pen."""
        pass

    def recover(self) -> None:
        """Unretract (recover) the pen."""
        pass

    def light(self, doLight: bool) -> None:
        """Turn on (doLight = True) or off (doLight = False) the running
        light."""
        pass

# TODO: Replace with config file params
left_stepper = Stepper([0, 1, 2, 3])
right_stepper = Stepper([4, 5, 6, 7])
robot = Robot(left_stepper, right_stepper)