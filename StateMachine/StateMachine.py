# StateMachine/StateMachine.py
# Takes a list of Inputs to move from State to
# State using a template method.


class StateMachine:

    def __init__(self, initialState):
        self.currentState = initialState
        self.currentState.run()

    def __str__(self): return self.currentState.toStr()

    # run function goes until it stops(a state returns true)
    def run(self):
        stop = False
        while not stop:
            input = self.currentState.run()
            self.currentState = self.currentState.next(input)
            if(input == True):
                stop = True


    # Template method:
    def runAll(self, inputs):
        for i in inputs:
            print(i)
            self.currentState = self.currentState.next(i)
            self.currentState.run()
