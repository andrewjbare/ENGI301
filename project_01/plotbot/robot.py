import Adafruit_BBIO.GPIO as GPIO

class Stepper:
    def __init__(self, pins: list[str]):
        # TODO: Figure out what type pin numbers will be/how to access
        self.pins = pins
        self.states: list[list[int]] = []

        # The current stepper state; "lead pin" is the first one energized on a step
        self.lead_pin = 0

        # Setup GPIO pins for output & set low
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)

    def write_pins(self, values: list[int]) -> None:
        """Write values to pins.
        
        If values is the wrong length, a ValueError should be thrown
        automatically. This method makes the step() method on subclasses much
        more concise."""
        for i in range(len(self.pins)):
            pin = self.pins[i]
            GPIO.output(pin, GPIO.HIGH if values[i] else GPIO.LOW)

    def step(self) -> None:
        """Perform one step."""
        self.write_pins(self.states[self.lead_pin])
        # Increment lead pin so the next run steps to the next state. If we've
        # hit the end of states, go back to state 0.
        if self.lead_pin < len(self.states):
            self.lead_pin += 1
        else:
            self.lead_pin = 0


class FullStepper(Stepper):
    def __init__(self, pins):
        super().__init__(pins)
        self.states = [
            [1, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 1],
            [1, 0, 0, 1]
        ]

class HalfStepper(Stepper):
    def __init__(self, pins):
        super().__init__(pins)
        self.states = [
            [1, 0, 0, 0],
            [1, 1, 0, 0],
            [0, 1, 0, 1],
            [0, 1, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 1],
            [0, 0, 0, 1],
            [1, 0, 0, 1]
        ]
        

class Robot:
    """Robot contains all of the atomic implementations of robot actions that
    compose the commands defined in main."""
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