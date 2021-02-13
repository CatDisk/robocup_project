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
        # Todo turn head if we find the ball return True else return CantFindBallInPos
        State.name = "LookForBall"
        print("looking")
        return True
    def next(self, input):
        if input == LookingAction.CantFindBallInPos:
            return SearchForBall.TurnForBall
        return SearchForBall.LookForBall


class TurnForBall(State):

    def run(self):
        # TODO turn the robot and return something(not True)
        State.name = "TurnForBall"
        print("turning")
        return 0
    def next(self, input):
        return SearchForBall.LookForBall


class SearchForBall(StateMachine):
    def __init__(self):
        # Initial state
        StateMachine.__init__(self, SearchForBall.LookForBall)


# init states
SearchForBall.LookForBall = LookForBall()
SearchForBall.TurnForBall = TurnForBall()
