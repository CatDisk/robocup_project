import time
import threading
from game import Game
from message import Message

def main():
    game = Game()
    game.add_player((100, 100), 0, "blue")
    t1 = threading.Thread(target = game.start)
    t1.start()
    game.inbox.append(Message("move player", [(200, 100)]))
    time.sleep(2)
    game.inbox.append(Message("move player", [(200, 200)]))
    time.sleep(1)
    game.inbox.append(Message("move player", [(100, 200)]))
    time.sleep(1)
    game.inbox.append(Message("move player", [(100, 100)]))
    time.sleep(2)
    game.inbox.append(Message("quit", []))



if __name__ == '__main__':
    main()