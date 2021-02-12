# StateMachine/StateMachine.py
# Takes a list of Inputs to move from State to
# State using a template method.


class StateMachine:

    def __init__(self, initialState):
        self.currentState = initialState
        self.currentState.run()

    def __str__(self): return self.currentState.toStr()

    # Template method:
    def runAll(self, inputs):
        for i in inputs:
            print(i)
            self.currentState = self.currentState.next(i)
            self.currentState.run()