import Adafruit_BBIO.GPIO as GPIO

class Stepper:
    def __init__(self, pins: list[str], states: list[list[int]]):
        # TODO: Figure out what type pin numbers will be/how to access
        self.pins = pins
        self.states: states

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
        

class Robot:
    """Robot contains all of the atomic implementations of robot actions that
    compose the commands defined in main."""
    def __init__(self, left_stepper: Stepper, right_stepper: Stepper) -> None:
        self.X = 0
        self.Y = 0
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

    def dwell(self, time_s: float) -> None:
        """Wait time_s seconds"""
        pass

    def bell(self, time_s: float) -> None:
        """Sound the buzzer"""
        pass

    def retract(self) -> None:
        """Retract the pen."""
        pass

    def recover(self) -> None:
        """Unretract (recover) the pen."""
        pass

    def lightOn(self) -> None:
        """Turn light on"""
        pass

    def lightOff(self) -> None:
        """Turn light off"""
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
right_stepper = Stepper(["P2_2", "P2_4", "P2_6", "P2_8"], stepper_states)
robot = Robot(left_stepper, right_stepper)