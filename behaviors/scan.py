import game


class Scan:
    def __init__(self):
        pass

    def update(self):
        if not game.data.aiming:
            game.data.start_scanning()
        return True
