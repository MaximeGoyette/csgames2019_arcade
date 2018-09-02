

class GPIO:
    def __init__(self):
        import pigpio

        self.pi = pigpio.pi()

        self.pi.set_pull_up_down(14, pigpio.PUD_UP)
        self.pi.set_pull_up_down(15, pigpio.PUD_UP)

    def get_pressed(self):
        return [not self.pi.read(14), not self.pi.read(15)]
