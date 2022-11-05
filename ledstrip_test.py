# The Adafruit PCA9685 module is a breakout board for the PCA9685
# PWM LED/Servo controller.


class TestLED():
	def __init__(self) -> None:
		self.val = 0

	def set_pwm(self, x,y,col):
		print(x,y, col)

class ledstrip():
	
	pwm = TestLED()

	def on(self):
		self.pwm.set_pwm(0, 0, 4095)
		self.pwm.set_pwm(1, 0, 4095)
		self.pwm.set_pwm(2, 0, 4095)

	def off(self):
		self.pwm.set_pwm(0, 0, 0)
		self.pwm.set_pwm(1, 0, 0)
		self.pwm.set_pwm(2, 0, 0)

	def set_color(self, color):
		if len(color) != 6:


			return
		rHex = color[0:2]
		gHex = color[2:4]
		bHex = color[4:6]
		r = int(rHex, 16)
		g = int(gHex, 16)
		b = int(bHex, 16)
		
		self.pwm.set_pwm(0, 0, int(4095 * r / 255))
		self.pwm.set_pwm(1, 0, int(4095 * g / 255))
		self.pwm.set_pwm(2, 0, int(4095 * b / 255))
