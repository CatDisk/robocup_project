from .State import State
from .StateMachine import StateMachine
from .Action import Action
from .SearchForBall import *


class StrikerAction(Action):
    name = "StrikerAction"


# Definition of all Striker Actions
StrikerAction.ReadyToShoot = Action("ready to shoot")
StrikerAction.TooFarFromBall = Action("too far from ball")
StrikerAction.FacingOpponentsGoal = Action("facing opponents goal")
StrikerAction.LostBall = Action("lost ball")
StrikerAction.FoundBall = Action("found ball")
StrikerAction.CloseToBall = Action("close to ball")


class TurnForOpponentGoal(State):

    def run(self):
        # turn the robot to opponents goal
        State.name = "TurnForOpponentGoal"
        print("turning")

    def next(self, input):
        if input == StrikerAction.ReadyToShoot:
            return Striker.Shoot
        if input == StrikerAction.TooFarFromBall:
            return Striker.GoToBall
        if input == StrikerAction.FacingOpponentsGoal:
            return Striker.Dribble
        return Striker.TurnForOpponentGoal


class Shoot(State):

    def run(self):
        # shoot the ball
        State.name = "Shoot"
        print("shooting")

    def next(self, input):
        if input == StrikerAction.LostBall:
            return Striker.SearchBall
        if input == StrikerAction.TooFarFromBall:
            return Striker.GoToBall
        return Striker.TurnForOpponentGoal


class Dribble(State):

    def run(self):
        # shoot the ball
        State.name = "Dribble"
        print("dribbling")

    def next(self, input):
        return Striker.GoToBall


class GoToBall(State):

    def run(self):
        # go to the ball
        State.name = "GoToBall"
        print("going to the Ball")

    def next(self, input):
        if input == StrikerAction.LostBall:
            return Striker.SearchBall
        if input == StrikerAction.CloseToBall:
            return Striker.TurnForOpponentGoal
        return Striker.GoToBall


class SearchBall(State):

    def run(self):
        if Striker.SearchForBall is None:
            Striker.SearchForBall = SearchForBall()
        State.name = Striker.SearchForBall.currentState.name

    def next(self, input):
        if input == LookingAction.FoundBall:
            Striker.SearchForBall = None
            return Striker.GoToBall
        if Striker.SearchForBall is not None:
            Striker.SearchForBall.run(input)
        return Striker.SearchBall


class Striker(StateMachine):
    def __init__(self):
        # Initial state
        StateMachine.__init__(self, Striker.SearchBall)


# Static variable initialization:
Striker.SearchForBall = None
Striker.TurnForOpponentGoal = TurnForOpponentGoal()
Striker.Shoot = Shoot()
Striker.Dribble = Dribble()
Striker.SearchBall = SearchBall()
Striker.GoToBall = GoToBall()

if __name__ == '__main__':
    s = Striker()
    s.run("ey")
    s.run(StrikerAction.LostBall)
    s.run(Action("cant find ball"))
    s.run(Action("found ball"))
