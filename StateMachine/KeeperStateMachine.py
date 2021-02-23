from .State import State
from .StateMachine import StateMachine
from .Action import Action
from .SearchForBall import SearchForBall

class KeeperAction(Action):

    name = "KeeperAction"


# Definition of all Keeper Actions
KeeperAction.LostBall = Action("lost ball")
KeeperAction.FoundBall = Action("found ball")
KeeperAction.HasBall = Action("has ball")
KeeperAction.FarFromGoal = Action("far from goal")
KeeperAction.IsAtGoal = Action("is at goal")
KeeperAction.BallApproachesLeft = Action("Ball is approaching on the left side")
KeeperAction.BallApproachesRight = Action("Ball is approaching on the right side")

class StayPut(State):

    def run(self):
        #  wait for instructions
        State.name = "StayPut"
        print("staying put")

    def next(self, input):
        if input == KeeperAction.LostBall:
            return Keeper.SearchBall
        if input == KeeperAction.HasBall:
            return Keeper.Pass
        if input == KeeperAction.FarFromGoal:
            return Keeper.GoToGoal
        if input == KeeperAction.BallApproachesLeft:
            return Keeper.GoLeft
        if input == KeeperAction.BallApproachesRight:
            return Keeper.GoRight
        return Keeper.StayPut


class GoLeft(State):

    def run(self):
        # step to the left
        State.name = "GoLeft"
        print("going left")

    def next(self, input):
        return Keeper.StayPut


class GoRight(State):

    def run(self):
        # step to the right
        State.name = "GoRight"
        print("going right")

    def next(self, input):
        return Keeper.StayPut


class SearchBall(State):

    def run(self):
        State.name = "SearchBall"
        print("searching")

    def next(self, input):
        if input == KeeperAction.FoundBall:
            return Keeper.StayPut
        return Keeper.SearchBall


class GoToGoal(State):

    def run(self):
        State.name = "GoToGoal"
        print("going to the goal")

    def next(self, input):
        if input == KeeperAction.IsAtGoal:
            return Keeper.StayPut
        return Keeper.GoToGoal


class Pass(State):

    def run(self):
        # pass to player (create a state machine)
        State.name = "Pass"
        print("Passing to nearest free player")

    def next(self, input):
        return Keeper.StayPut


class Keeper(StateMachine):
    def __init__(self):
        # Initial state
        StateMachine.__init__(self, Keeper.StayPut)


# Static variable initialization:
Keeper.StayPut = StayPut()
Keeper.GoLeft = GoLeft()
Keeper.GoRight = GoRight()
Keeper.Pass = Pass()
Keeper.GoToGoal = GoToGoal()
Keeper.SearchBall = SearchBall()

