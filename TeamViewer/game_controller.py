import json
from message import Message

class GameController():
    def __init__(self, game_inbox):
        self.game_inbox = game_inbox
        self.running = True

    def move_player(self, player_id, pos, dir) -> Message:
        order = {
            "target": player_id,
            "action": "move",
            "params": [pos, dir]
        }
        return self.msg_handler("order", json.dumps(order), "out")

    def look(self, player_id, degrees) -> Message:
        order = {
            "target": player_id,
            "action": "look",
            "params": [degrees]
        }
        return self.msg_handler("order", json.dumps(order), "out")

    def msg_handler(self, msg_type, payload, mode='out'):
        if mode == 'out':
            return Message(msg_type, payload)

    def input_handler(self):
        inpt = input("\nEnter a command: ")
        inpt = inpt.split(" ")
        if inpt[0] == "help":
            print("Available commands:\n")
            print("help")
            print("move <player id> <x> <y> <movement direction>")
            print("look <player id> <deg>")
            print("quit")
        elif inpt[0] == "move":
            if len(inpt) == 5:
                try:
                    id = int(inpt[1])
                    x = float(inpt[2])
                    y = float(inpt[3])
                    dir = inpt[4]
                    self.game_inbox.append(self.move_player(id, (x, y), dir))
                except:
                    print("Something went wrong!")
            else:
                print("Not a valid input. enter \'help\' for all commands")
        elif inpt[0] == "look":
            if len(inpt) == 3:
                try:
                    id = int(inpt[1])
                    deg = float(inpt[2])
                    self.game_inbox.append(self.look(id, deg))
                except:
                    print("Something went wrong!")
            else:
                print("Not a valid input. enter \'help\' for all commands")
        elif inpt[0] == "quit":
            self.running = False
            self.game_inbox.append(Message("quit", None))
        else:
            print("Not a valid input. enter \'help\' for all commands")

    def run(self):
        while self.running:
            self.input_handler()

if __name__ == '__main__':
    print("Start from game.py!")