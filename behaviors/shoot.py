import game
from API import ServerMessageTypes


class Shoot:
    def __init__(self, pt):
        self.pt = pt

    def update(self):
        if game.data.aiming_at(self.pt):
            game.data.shoot()
        return True
