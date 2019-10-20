from API import ServerMessageTypes, ServerComms
from game import GameData
import game
import behavior_tree_factory
from behavior_tree import BehaviorTree
import logging


def main(debug, hostname, port, name):
    if debug:
        logging.basicConfig(format='[%(asctime)s] %(message)s', level=logging.DEBUG)
    else:
        logging.basicConfig(format='[%(asctime)s] %(message)s', level=logging.INFO)

    # Connect to game server
    GameServer = ServerComms(hostname, port)

    # Spawn our tank
    logging.info("Creating tank with name '{}'".format(name))
    GameServer.sendMessage(ServerMessageTypes.CREATETANK, {'Name': name})

    # static reference to game, easier for other files to use it
    game.data = GameData(GameServer, name)

    game.data.game_server.sendMessage(ServerMessageTypes.TOGGLEFORWARD)
    # state.game_server.sendMessage(ServerMessageTypes.MOVEFORWARDDISTANCE, {"Amount": 10})

    behavior_tree: BehaviorTree = behavior_tree_factory.get_tree()

    while True:
        messagePayload = GameServer.readMessage()
        game.data.update(messagePayload)

        behavior_tree.run()


if __name__ == '__main__':
    main(False, '127.0.0.1', 8052, f'Human:1')
