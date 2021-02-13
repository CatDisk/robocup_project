# StateMachine/State.py
# A State has an operation, and can be moved
# into the next State given an Input:


class State:
    name = "not named"

    def toStr(self):
        return self.name
    def __str__(self): return self.name

    # return next state or true to stop the runnung process
    def run(self):
        assert 0, "run not implemented"
        
    def next(self, input):
        assert 0, "next not implemented"