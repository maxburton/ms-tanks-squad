from game import GameData
import game
from behaviors.turn import Turn

class Wander:
    next_point_index = -1

    def __init__(self):
        pass

    def update(self):
        if self.next_point_index == -1:
            next_point = game.data.get_closest_edge_point()
            self.next_point_index = game.data.edge_points.index(next_point)

        next_point = game.data.edge_points[self.next_point_index]
        dst = game.data.get_distance_to(next_point)
        if dst < 5:
            # wrap around if reached end
            self.next_point_index = self.next_point_index + 1 if self.next_point_index < len(
                game.data.edge_points) - 1 else 0
            next_point = game.data.edge_points[self.next_point_index]

        return Turn(next_point).update()
