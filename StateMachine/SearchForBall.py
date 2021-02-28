from .State import State
from .StateMachine import StateMachine
from .Action import Action


class LookingAction(Action):

    name = "LookingAction"


# init actions
LookingAction.FoundBall = LookingAction("found ball")
LookingAction.CantFindBall = LookingAction("cant find ball")


class LookForBall(State):

    def run(self):
        State.name = "LookForBall"
        print("looking")

    def next(self, input):
        if input == LookingAction.FoundBall:
            return SearchForBall.FoundBall
        if input == LookingAction.CantFindBall:
            return SearchForBall.LookLeft
        return SearchForBall.LookForBall


class LookLeft(State):

    def run(self):
        State.name = "LookLeft"
        print("looking left")

    def next(self, input):
        if input == LookingAction.FoundBall:
            return SearchForBall.FoundBall
        if input == LookingAction.CantFindBall:
            return SearchForBall.LookFarLeft
        return SearchForBall.LookLeft


class LookFarLeft(State):

    def run(self):
        State.name = "LookFarLeft"
        print("looking far left")

    def next(self, input):
        if input == LookingAction.FoundBall:
            return SearchForBall.FoundBall
        if input == LookingAction.CantFindBall:
            return SearchForBall.LookRight
        return SearchForBall.LookFarLeft


class LookRight(State):

    def run(self):
        State.name = "LookRight"
        print("looking right")

    def next(self, input):
        if input == LookingAction.FoundBall:
            return SearchForBall.FoundBall
        if input == LookingAction.CantFindBall:
            return SearchForBall.LookFarRight
        return SearchForBall.LookRight


class LookFarRight(State):

    def run(self):
        State.name = "LookFarRight"
        print("looking far right")

    def next(self, input):
        if input == LookingAction.FoundBall:
            return SearchForBall.FoundBall
        if input == LookingAction.CantFindBall:
            return SearchForBall.TurnForBall
        return SearchForBall.LookFarRight


class TurnForBall(State):

    def run(self):
        State.name = "TurnForBall"
        print("turning")

    def next(self, input):
        return SearchForBall.LookForBall


class FoundBall(State):

    def run(self):
        State.name = "FoundBall"
        print("found ball")

    def next(self, input):
        return SearchForBall.FoundBall


class SearchForBall(StateMachine):
    def __init__(self):
        # Initial state
        StateMachine.__init__(self, SearchForBall.LookForBall)


# init states
SearchForBall.LookForBall = LookForBall()
SearchForBall.LookLeft = LookLeft()
SearchForBall.LookFarLeft = LookFarLeft()
SearchForBall.LookRight = LookRight()
SearchForBall.LookFarRight = LookFarRight()
SearchForBall.TurnForBall = TurnForBall()
SearchForBall.FoundBall = FoundBall()
