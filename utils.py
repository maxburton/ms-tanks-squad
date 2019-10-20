import math
from datetime import datetime


def get_distance(x1, y1, x2, y2):
    headingX = x2 - x1
    headingY = y2 - y1
    return math.sqrt((headingX * headingX) + (headingY * headingY))


def get_diff(target_time):
    diff = datetime.now() - target_time
    return diff.total_seconds() * 1e+6 + diff.microseconds


def is_uptodate(target_time):
    return get_diff(target_time) < 1e+6


def radian_to_degree(angle):
    return angle * (180.0 / math.pi)


def get_heading(x1, y1, x2, y2):
    heading = math.atan2(y2 - y1, x2 - x1)
    heading = radian_to_degree(heading)
    heading = math.fmod((heading - 360), 360)
    return abs(heading)


def looking_at(self, x2, y2):
    heading = self.get_tank_heading(self.state.me)
    target_heading = get_heading(self.state.me['X'], self.state.me['Y'], x2, y2)
    dif = abs(heading - target_heading)
    if dif > 5:
        return False
    return True


def get_closest_point(x1, y1, coord_list):
    return min(coord_list, key=lambda k: get_distance(x1, y1, k[0], k[1]))
