import game


class Turn:
    def __init__(self, pt):
        self.pt = pt

    def update(self):
        if not game.data.facing_at(self.pt):
            game.data.turn_to_heading(self.pt)
        return True
