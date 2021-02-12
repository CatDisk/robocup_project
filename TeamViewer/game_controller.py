import json
from message import Message

class GameController():
    def __init__(self, game_inbox):
        self.game_inbox = game_inbox
        self.running = True

    def move_player(self, player_id, pos) -> Message:
        order = {
            "target": player_id,
            "action": "move",
            "params": pos,
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
            print("move <player_id> <x> <y>")
            print("quit")
        elif inpt[0] == "move":
            if len(inpt) == 4:
                try:
                    id = int(inpt[1])
                    x = float(inpt[2])
                    y = float(inpt[3])
                    self.game_inbox.append(self.move_player(id, (x, y)))
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