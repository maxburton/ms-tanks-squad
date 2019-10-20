import game
from behavior_tree import BehaviorTree, SequenceNode, Node, SelectorNode, TrueDecorator
from behaviors.wander import Wander
from behaviors.scan import Scan
from behaviors.turn import Turn
from behaviors.aim import Aim
from behaviors.shoot import Shoot
import utils

wander = Wander()
scan = Scan()

wander_node = Node("wander", lambda: wander.update())
scan_node = Node("scan", lambda: scan.update())
sequence_default_node = SequenceNode("default", [wander_node, scan_node])

no_ammo_node = Node("no ammo", lambda: not game.data.has_ammo())
get_ammo_node = Node("get ammo", lambda: get_ammo())
ammo_dec_node = TrueDecorator("ammo", get_ammo_node)
sequence1_node = SequenceNode("ammo", [no_ammo_node, ammo_dec_node])

has_target_node = Node("has target", lambda: game.data.get_target() is not None)
shoot_target_node = Node("shoot target", lambda: shoot_target())
target_dec_node = TrueDecorator("target", shoot_target_node)
sequence2_node = SequenceNode("target", [has_target_node, wander_node, target_dec_node])

root_node = Node("root", lambda: SelectorNode("root", [sequence1_node, sequence2_node, sequence_default_node]).run())


def get_ammo():
    ammo_objs = [obj for obj in game.data.game_objects.values() if
                 obj['Type'] == 'AmmoPickup' and utils.is_uptodate(obj['time'])]
    if len(ammo_objs) < 1:
        return False

    ammo_objs = list(map(lambda obj: (obj, game.data.get_distance_to((obj['X'], obj['Y']))), ammo_objs))
    target = min(ammo_objs, key=lambda x: x[1])[0]
    target = (target['X'], target['Y'])

    return Aim(target).update() and Turn(target).update()


def go_suicide():
    target = game.data.get_suicide_friend()
    if target is not None:
        target = (target['X'], target['Y'])
        return aim.at(target) and turn.to(target)
    return False


def shoot_target():
    target = game.data.get_target()
    if target is not None:
        target = (target['X'], target['Y'])
        return Aim(target).update() and Shoot(target).update()
    return False


def get_tree() -> BehaviorTree:
    tree = BehaviorTree(root_node)
    return tree
