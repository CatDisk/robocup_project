from State import State
from StateMachine import StateMachine
from Action import Action


class LookingAction(Action):

    name = "LookingAction"


# init actions
LookingAction.FoundBall = LookingAction("found ball")
LookingAction.CantFindBallInPos = LookingAction("can't find the ball in current position")


class LookForBall(State):

    def run(self):
        State.name = "LookForBall"
        print("looking")

    def next(self, input):
        if input == LookingAction.CantFindBallInPos:
            return SearchForBall.TurnForBall
        return SearchForBall.LookForBall


class TurnForBall(State):

    def run(self):
        State.name = "TurnForBall"
        print("turning")

    def next(self, input):
        return SearchForBall.LookForBall


class SearchForBall(StateMachine):
    def __init__(self):
        # Initial state
        StateMachine.__init__(self, SearchForBall.LookForBall)


# init states
SearchForBall.LookForBall = LookForBall()
SearchForBall.TurnForBall = TurnForBall()
