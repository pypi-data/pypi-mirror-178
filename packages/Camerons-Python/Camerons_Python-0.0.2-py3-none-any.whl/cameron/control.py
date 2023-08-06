__all__ = ["Lowpass"]


class Lowpass:
    def __init__(self, timeconstant, default=0, dt=None):
        self.timeconstant = timeconstant
        self.default = default
        self.dt = dt
        self.reset()

    @property
    def alpha(self):
        return self.dt / (self.timeconstant + self.dt)

    def filter(self, val, dt=None):
        if dt is not None:
            self.dt = dt
        self.last_val = self.alpha * val + (1 - self.alpha) * self.last_val
        return self.last_val

    def reset(self):
        self.last_val = self.default
