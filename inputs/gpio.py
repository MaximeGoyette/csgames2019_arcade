

class GPIO:
    def __init__(self):
        import pigpio

        self.pi = pigpio.pi()

	self.pi.set_pull_up_down(5, pigpio.PUD_DOWN)
        self.pi.set_pull_up_down(6, pigpio.PUD_DOWN)
        self.pi.set_pull_up_down(12, pigpio.PUD_DOWN)
        self.pi.set_pull_up_down(13, pigpio.PUD_DOWN)

    def get_pressed(self):
	return [self.pi.read(5), self.pi.read(13), self.pi.read(12), self.pi.read(6) ]
