import game


class Aim:
    def __init__(self, pt):
        self.pt = pt

    def update(self):
        if not game.data.aiming_at(self.pt):
            game.data.aim_at_heading(self.pt)
        return True
