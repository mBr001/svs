from peripherals import Keyboard

class Steerage:
    def __init__(self, manipulator, mobile_platform):
        self.manipulator = manipulator
        self.mobile_platform = mobile_platform

        # Init keyboard control
        self.keyboard = Keyboard()

        # self.peripherals.bd.when_double_pressed = self.make_snap

        # Control moving of Mobile Platform via keyboard
        self.keyboard.events.forward += self.forward
        self.keyboard.events.backward += self.backward
        self.keyboard.events.left += self.left
        self.keyboard.events.right += self.right
        self.keyboard.events.mobile_platform_halt += self.mobile_platform_halt

        # Control Manipulator via keyboard
        self.keyboard.events.get_some_debug_data += self.rbc_test
        self.keyboard.events.manipulator_halt += self.manipulator.halt
        self.keyboard.events.manipulator_status_update += self.manipulator_status_update
        self.keyboard.events.manipulator_forward += self.manipulator.forward
        self.keyboard.events.manipulator_backward += self.manipulator.backward

        # CAUTION: Inverted values. MIN is MAX
        self.motor_power = 170

    def move(self, motor_l, motor_r):
        self.mobile_platform.send(motor_l * self.motor_power, motor_r * self.motor_power)

    def forward(self):
        self.mobile_platform.send(220, 220)

    def backward(self):
        self.mobile_platform.send(-220, -220)

    def left(self):
        self.mobile_platform.send(int(-1 * self.motor_power), 1 * self.motor_power)

    def right(self):
        self.mobile_platform.send(1 * self.motor_power, int(-1 * self.motor_power))

    def mobile_platform_halt(self):
        # Stop gracefully
        self.mobile_platform.send(0 * self.motor_power, 0 * self.motor_power)

    def rbc_test(self):
        self.manipulator.get_status()


    def manipulator_status_update(self):
        self.manipulator.get_status()
