import json
import queue
from TeamViewer.message import Message
from StateMachine.DefenderStateMachine import Defender
from StateMachine.KeeperStateMachine import Keeper
from StateMachine.StrikerStateMachine import Striker
from StateMachine.Action import Action

class GameController():
    def __init__(self, game_inbox, metadata):
        self.game_inbox = game_inbox
        self.inbox = queue.Queue()
        self.statemachines = []
        self.metadata = metadata
        self.running = True
        self.build_statemachines()

    def build_statemachines(self):
        for player in self.metadata:
            if player[0] == "striker":
                self.statemachines.append(Striker())
            elif player[0] == "keeper":
                self.statemachines.append(Keeper())
            elif player[0] == "defender":
                self.statemachines.append(Defender())
            else:
                raise TypeError("Type \'{}\' is not defined".format(player[0]))

    def move_player(self, player_id, pos, dir):
        order = {
            "target": player_id,
            "action": "move",
            "params": [pos, dir]
        }
        self.msg_handler("order", json.dumps(order), "out")

    def dribble(self, player_id):
        order = {
            "target": player_id,
            "action": "dribble",
            "params": []
        }

    def look(self, player_id, degrees):
        order = {
            "target": player_id,
            "action": "look",
            "params": [degrees]
        }
        self.msg_handler("order", json.dumps(order), "out")
    
    def move_ball(self, deg):
        order = {
            "target": "ball",
            "action": "kick",
            "params": [deg]
        }
        self.msg_handler("order", json.dumps(order), "out")

    def kick(self, player_id):
        order = {
            "target": player_id,
            "action": "kick",
            "params": []
        }
        self.msg_handler("order", json.dumps(order), "out")
    
    def can_see_ball(self, player_id):
        order = {
            "target": player_id,
            "action": "can see ball",
            "params": []
        }
        self.msg_handler("order", json.dumps(order), "out")

    def msg_handler(self, msg_type, payload, mode='out') -> Message:
        message: Message
        if mode == 'out':
            message = Message(msg_type, payload)
            self.game_inbox.put(message)
        #else:
        #    while len(self.inbox) > 0:
        #        msg = self.inbox.pop()
        #        if msg.msg_type == "data":
        #            payload = json.loads(msg.payload)
        #            if payload["data"] == "found ball":
        #                pass
        #            elif payload["data"] == "collision":
        #                pass
        #            elif payload["data"] == "lost ball":
        #                pass
        #            elif payload["data"] == "facing goal":
        #                pass
        #            elif payload["data"] == "ready to shoot":
        #                pass
        #            elif payload["data"] == "too far from ball":
        #                pass
        #            elif payload["data"] == "can't find ball":
        #                pass
        #            elif payload["data"] == "goal":
        #                pass
        return message

    def send_order(self, action, player_id):
        order = {
            "target": player_id,
            "action": action,
            "params": []
        }
        self.msg_handler("order", json.dumps(order), "out")

    def input_handler(self):
        inpt = input("\nEnter a command: ")
        inpt = inpt.split(" ")
        if inpt[0] == "help":
            print("Available commands:\n")
            print("help")
            print("move <player id> <x> <y> <movement direction>")
            print("look <player id> <deg>")
            print("kick <player id>")
            print("see ball <player id>")
            print("move ball <angle>")
            print("reset")
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
        elif inpt[0] == "see" and inpt[1] == "ball":
            if len(inpt) == 3:
                try:
                    id = int(inpt[2])
                    self.can_see_ball(id)
                except:
                    print("Something went wrong!")
            else:
                print("Not a valid input. enter \'help\' for all commands")
        elif inpt[0] == "kick" and inpt[1] == "ball":
            if len(inpt) == 3:
                try:
                    deg = float(inpt[2])
                    self.move_ball(deg)
                except:
                    print("Something went wrong!")
            else:
                print("Not a valid input. enter \'help\' for all commands")
        elif inpt[0] == "kick":
            if len(inpt) == 2:
                try:
                    deg = int(inpt[1])
                    self.kick(deg)
                except:
                    print("Something went wrong!")
            else:
                print("Not a valid input. enter \'help\' for all commands")
        elif inpt[0] == "reset":
           self.game_inbox.put(Message("reset", None))
        elif inpt[0] == "quit":
            self.running = False
            self.game_inbox.put(Message("quit", None))
        else:
            print("Not a valid input. enter \'help\' for all commands")

    #def run(self):
    #    while self.running:
    #        self.input_handler()
    #        for machine in self.statemachines:
    #            machine.run(Action("ready to shoot"))
    def run(self, event):
        while self.running:
            for index, machine in enumerate(self.statemachines):
                self.send_order(str(machine), index)
            event.wait()
            if not self.inbox.empty():
                message = self.inbox.get()
                if message.msg_type == "quit":        
                    self.running = False
                    print("----GameController Stopped----")
            event.clear()
                

if __name__ == '__main__':
    print("Start from game.py!")