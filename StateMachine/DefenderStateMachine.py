from .State import State
from .StateMachine import StateMachine
from .Action import Action
from .SearchForBall import *

class DefenderAction(Action):

    name = "DefenderAction"


# Definition of all Defender Actions
DefenderAction.LostBall = Action("lost ball")
DefenderAction.FoundBall = Action("found ball")
DefenderAction.HasBall = Action("has ball")
DefenderAction.BallApproachesGoal = Action("Ball approaches goal")
DefenderAction.BallIsOnYourHalf = Action("Ball is on your half")
DefenderAction.BallIsOnOpponentsHalf = Action("Ball is on opponents half")
DefenderAction.Collision = Action("collision")

class StayPut(State):

    def run(self):
        #wait for instructions
        State.name = "StayPut"
        print("staying put")

    def next(self, input):
        if input == DefenderAction.LostBall:
            return Defender.SearchBall
        if input == DefenderAction.BallIsOnYourHalf:
            return Defender.GoToDefendPosition
        if input == DefenderAction.BallIsOnOpponentsHalf:
            return Defender.GoToAttackPosition
        return Defender.StayPut


class GoToAttackPosition(State):

    def run(self):
        State.name = "GoToAttackPosition"
        print("going to attack position")

    def next(self, input):
        if input == DefenderAction.LostBall:
            return Defender.SearchBall
        if input == DefenderAction.HasBall:
            return Defender.Pass
        if input == DefenderAction.BallIsOnYourHalf:
            return Defender.StayPut
        if input == DefenderAction.Collision:
            return Defender.StepBack
        return Defender.GoToAttackPosition


class GoToDefendPosition(State):

    def run(self):
        State.name = "GoToDefendPosition"
        print("going to defend position")


    def next(self, input):
        if input == DefenderAction.LostBall:
            return Defender.SearchBall
        if input == DefenderAction.BallIsOnOpponentsHalf:
            return Defender.StayPut
        if input == DefenderAction.BallApproachesGoal:
            return Defender.GoToBall
        if input == DefenderAction.Collision:
            return Defender.StepBack
        return Defender.GoToDefendPosition


class StepBack(State):

    def run(self):
        #take a few steps back
        State.name = "StepBack"
        print("ouch!")

    def next(self, input):
        return Defender.SearchBall


class SearchBall(State):

    def run(self):
        if Defender.SearchForBall is None:
            Defender.SearchForBall = SearchForBall()
        State.name = Defender.SearchForBall.currentState.name

    def next(self, input):
        if input == LookingAction.FoundBall:
            Defender.SearchForBall = None
            return Defender.StayPut
        if Defender.SearchForBall is not None:
            Defender.SearchForBall.run(input)
        return Defender.SearchBall


class GoToBall(State):

    def run(self):
        State.name = "GoToBall"
        print("going to the ball")

    def next(self, input):
        if input == DefenderAction.LostBall:
            return Defender.SearchBall
        if input == DefenderAction.BallIsOnOpponentsHalf:
            return Defender.StayPut
        if input == DefenderAction.HasBall:
            return Defender.Pass
        if input == DefenderAction.Collision:
            return Defender.StepBack
        return Defender.GoToBall


class Pass(State):

    def run(self):
        # pass to striker
        State.name = "Pass"
        print("Passing to nearest Defender")
        return True

    def next(self, input):
        return Defender.StayPut


class Defender(StateMachine):
    def __init__(self):
        # Initial state
        StateMachine.__init__(self, Defender.StayPut)


# Static variable initialization:
Defender.SearchForBall = None
Defender.StayPut = StayPut()
Defender.GoToAttackPosition = GoToAttackPosition()
Defender.GoToDefendPosition = GoToDefendPosition()
Defender.Pass = Pass()
Defender.GoToBall = GoToBall()
Defender.StepBack = StepBack()
Defender.SearchBall = SearchBall()

