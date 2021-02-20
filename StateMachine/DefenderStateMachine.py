from State import State
from StateMachine import StateMachine
from Action import Action
from SearchForBall import SearchForBall

class DefenderAction(Action):

    name = "DefenderAction"


# Definition of all Defender Actions
DefenderAction.LostBall = Action("lost ball")
DefenderAction.FoundBall = Action("found ball")
DefenderAction.HasBall = Action("has ball")
DefenderAction.BallApproachesGoal = Action("Ball approaches goal")
DefenderAction.BallIsOnYourHalf = Action("Ball is on your half")
DefenderAction.BallIsOnOpponentsHalf = Action("Ball is on opponents half")

class StayPut(State):

    def run(self):
        # TODO wait for instructions
        State.name = "StayPut"
        print("staying put")
        return True

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
        #TODO step to the left
        State.name = "GoToAttackPosition"
        print("going to attack position")
        return True

    def next(self, input):
        if input == DefenderAction.LostBall:
            return Defender.SearchBall
        if input == DefenderAction.HasBall:
            return Defender.PassToNearestStriker
        if input == DefenderAction.BallIsOnYourHalf:
            return Defender.StayPut
        return Defender.GoToAttackPosition


class GoToDefendPosition(State):

    def run(self):
        # TODO step to the right
        State.name = "GoToDefendPosition"
        print("going to defend position")
        return True

    def next(self, input):
        if input == DefenderAction.LostBall:
            return Defender.SearchBall
        if input == DefenderAction.BallIsOnOpponentsHalf:
            return Defender.StayPut
        if input == DefenderAction.BallApproachesGoal:
            return Defender.GoToBall
        return Defender.GoToDefendPosition


class SearchBall(State):

    def run(self):
        State.name = "SearchBall"
        print("searching")
        search = SearchForBall()
        search.run()
        return DefenderAction.FoundBall

    def next(self, input):
        if input == DefenderAction.FoundBall:
            return Defender.StayPut
        return Defender.SearchBall


class GoToBall(State):

    def run(self):
        State.name = "GoToBall"
        print("going to the ball")
        return True

    def next(self, input):
        if input == DefenderAction.LostBall:
            return Defender.SearchBall
        if input == DefenderAction.BallIsOnOpponentsHalf:
            return Defender.StayPut
        if input == DefenderAction.HasBall:
            return Defender.PassToNearestStriker
        return Defender.GoToGoal


class PassToNearestStriker(State):

    def run(self):
        # TODO pass to striker (create a state machine)
        State.name = "Pass"
        print("Passing to nearest striker")
        return True

    def next(self, input):
        return Defender.StayPut


class Defender(StateMachine):
    def __init__(self):
        # Initial state
        StateMachine.__init__(self, Defender.StayPut)


# Static variable initialization:
Defender.StayPut = StayPut()
Defender.GoToAttackPosition = GoToAttackPosition()
Defender.GoToDefendPosition = GoToDefendPosition()
Defender.PassToNearestStriker = PassToNearestStriker()
Defender.GoToBall = GoToBall()
Defender.SearchBall = SearchBall()

