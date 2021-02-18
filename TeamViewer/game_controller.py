import json
from message import Message

class GameController():
    def __init__(self, game_inbox):
        self.game_inbox = game_inbox
        self.inbox = []
        self.running = True

    def move_player(self, player_id, pos, dir):
        order = {
            "target": player_id,
            "action": "move",
            "params": [pos, dir]
        }
        self.msg_handler("order", json.dumps(order), "out")

    def look(self, player_id, degrees):
        order = {
            "target": player_id,
            "action": "look",
            "params": [degrees]
        }
        self.msg_handler("order", json.dumps(order), "out")
    
    def kick(self, deg):
        order = {
            "target": "ball",
            "action": "kick",
            "params": [deg]
        }
        self.msg_handler("order", json.dumps(order), "out")

    def msg_handler(self, msg_type, payload, mode='out') -> Message:
        message: Message
        if mode == 'out':
            message = Message(msg_type, payload)
            self.game_inbox.append(message)
        else:
            while len(self.inbox) > 0:
                msg = self.inbox.pop()
                if msg.msg_type == "data":
                    payload = json.loads(msg.payload)
                    if payload["data"] == "found ball":
                        pass
                    elif payload["data"] == "collision":
                        pass
                    elif payload["data"] == "lost ball":
                        pass
                    elif payload["data"] == "facing goal":
                        pass
                    elif payload["data"] == "ready to shoot":
                        pass
                    elif payload["data"] == "too far from ball":
                        pass
                    elif payload["data"] == "can't find ball":
                        pass
                    elif payload["data"] == "goal":
                        pass
        return message

    def input_handler(self):
        inpt = input("\nEnter a command: ")
        inpt = inpt.split(" ")
        if inpt[0] == "help":
            print("Available commands:\n")
            print("help")
            print("move <player id> <x> <y> <movement direction>")
            print("look <player id> <deg>")
            print("kick <deg>")
            print("quit")
        elif inpt[0] == "move":
            if len(inpt) == 5:
                try:
                    id = int(inpt[1])
                    x = float(inpt[2])
                    y = float(inpt[3])
                    dir = inpt[4]
                    self.move_player(id, (x, y), dir)
                except:
                    print("Something went wrong!")
            else:
                print("Not a valid input. enter \'help\' for all commands")
        elif inpt[0] == "look":
            if len(inpt) == 3:
                try:
                    id = int(inpt[1])
                    deg = float(inpt[2])
                    self.look(id, deg)
                except:
                    print("Something went wrong!")
            else:
                print("Not a valid input. enter \'help\' for all commands")
        elif inpt[0] == "kick":
            if len(inpt) == 2:
                try:
                    deg = float(inpt[1])
                    self.kick(deg)
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