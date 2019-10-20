from datetime import datetime
from statistics import mean
from API import ServerMessageTypes, ServerComms
import utils


class GameData:
    game_server: ServerComms
    game_objects = {}
    me = None
    bot_name = ""
    snitch_holder_id = None

    edge1 = (70, 75)
    edge2 = (55, 90)
    edge_points = [(62, 0), (0, 103), (-62, 0), (0, -103)]

    turning = False
    turning_target = None
    aiming = False
    aiming_target = None

    def __init__(self, game_server, bot_name: str):
        self.game_server = game_server
        self.bot_name = bot_name

    # update internal game data with information from server
    def update(self, message_payload):
        message_type = message_payload['messageType']

        if message_type == ServerMessageTypes.OBJECTUPDATE:
            self._update_time(message_payload)
            self._update_mobility(message_payload)
            if message_payload['Name'] == '':
                message_payload['Name'] = message_payload['Id']
            # TODO: Cleanup old objects, since they will accumulate forever
            self.game_objects[message_payload['Name']] = message_payload

        elif message_type == ServerMessageTypes.DESTROYED:
            self.game_server.sendMessage(ServerMessageTypes.TOGGLEFORWARD)

        elif message_type == ServerMessageTypes.SNITCHPICKUP:
            self.snitch_holder_id = message_payload['Id']

        else:
            print("Unknown message:", message_payload)

        self.me = self._get_me()

        if self.turning and self.turning_target is not None and self.facing_at(self.turning_target):
            self.turning_target = None
            self.turning = False

        if self.aiming and self.aiming_target is not None and self.aiming_at(self.aiming_target):
            self.aiming_target = None
            self.aiming = False

    def get_turret_heading(self):
        return self.me['TurretHeading']

    def get_tank_heading(self):
        return self.me['Heading']

    def get_distance_to(self, pt: (int, int)):
        return utils.get_distance(self.me['X'], self.me['Y'], pt[0], pt[1])

    def get_closest_edge_point(self):
        return self.get_closest_to_me(self.edge_points)

    def get_closest_to_me(self, pt_lst: [(int, int)]):
        return utils.get_closest_point(self.me['X'], self.me['Y'], pt_lst)

    def start_scanning(self):
        self.game_server.sendMessage(ServerMessageTypes.TOGGLETURRETLEFT)
        self.aiming = True
        self.aiming_target = None

    def aim_at_heading(self, pt):
        heading = utils.get_heading(self.me['X'], self.me['Y'], pt[0], pt[1])
        self.game_server.sendMessage(ServerMessageTypes.TURNTURRETTOHEADING, {"Amount": heading})
        self.aiming = True
        self.aiming_target = pt

    def aiming_at(self, pt):
        target_heading = utils.get_heading(self.me['X'], self.me['Y'], pt[0], pt[1])
        dif = abs(self.get_turret_heading() - target_heading)
        if dif > 5:
            return False
        return True

    def facing_at(self, pt):
        target_heading = utils.get_heading(self.me['X'], self.me['Y'], pt[0], pt[1])
        diff = abs(self.get_tank_heading() - target_heading)
        if diff > 5:
            return False
        return True

    def shoot(self):
        self.game_server.sendMessage(ServerMessageTypes.FIRE)

    def turn_to_heading(self, pt):
        heading = utils.get_heading(self.me['X'], self.me['Y'], pt[0], pt[1])
        self.game_server.sendMessage(ServerMessageTypes.TURNTOHEADING, {"Amount": heading})
        self.turning = True
        self.turning_target = pt

    def get_suicide_friend(self):
        targets = list(filter(self.is_valid_suicide_friend, self.game_objects.values()))
        if len(targets) < 1:
            return None
        results = list(map(lambda x: self.get_distance_to((x['X'], x['Y'])), targets))
        return self.game_objects[min(results, key=lambda x: x[0])[1]]

    def is_valid_suicide_friend(self, obj):
        if obj['Type'] != 'Tank':
            return False
        if obj['Name'] == self.bot_name:
            return False
        if not utils.is_uptodate(obj['time']):
            return False
        if not self.is_teammate(obj) or obj['Health'] < 2:
            return False
        return True

    def get_target(self):
        targets = list(filter(self.is_valid_target, self.game_objects.values()))
        if len(targets) < 1:
            return None
        results = list(map(lambda x: self._get_score(x), targets))
        return self.game_objects[min(results, key=lambda x: x[0])[1]]

    def is_valid_target(self, obj):
        if obj['Type'] != 'Tank':
            return False
        if obj['Name'] == self.bot_name:
            return False
        if not utils.is_uptodate(obj['time']):
            return False
        if obj['Health'] < 1:
            return False
        if self.is_teammate(obj) and obj['Health'] > 1:
            return False
        return True

    def is_teammate(self, obj):
        if ':' not in obj['Name'] or ':' not in self.bot_name:
            return False
        return obj['Name'].split(':')[0] == self.bot_name.split(':')[0]

    def get_health(self):
        return self.me['Health']

    def has_ammo(self):
        return self.me['Ammo'] > 0

    def _get_score(self, tank):
        score = tank['mobility'] * 50 + \
                self.get_distance_to((tank['X'], tank['Y'])) + \
                tank['Health'] * 100
        if self.snitch_holder_id == tank['Id']:
            score = 0  # GO KILL EM BOY
        return score, tank['Name']

    # return bot self game object
    def _get_me(self):
        if self.bot_name not in self.game_objects:
            return None
        return self.game_objects[self.bot_name]

    # timestamp the message
    def _update_time(self, message_payload):
        message_payload['time'] = datetime.now()

    # update target mobility coefficient
    def _update_mobility(self, message_payload):
        name = message_payload['Name']
        if name not in self.game_objects:
            message_payload['mobility'] = 0  # TODO: Why tho
            return

        old_state = self.game_objects[name]
        dist = utils.get_distance(message_payload['X'], message_payload['Y'],
                                  old_state['X'], old_state['Y'])
        if 'mobility' not in message_payload:
            message_payload['mobility'] = dist
        else:
            message_payload['mobility'] = mean((message_payload['mobility'], dist))


data: GameData = None
