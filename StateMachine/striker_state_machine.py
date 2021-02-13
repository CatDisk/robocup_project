from State import State
from StateMachine import StateMachine
from Action import Action
from SearchForBall import SearchForBall

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
        State.name = "TurnForOpponentGoal"
        print("turning")
        return True

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
        State.name = "Shoot"
        print("shooting")
        return True

    def next(self, input):
        if input == StrikerAction.LostBall:
            return Striker.SearchBall
        if input == StrikerAction.TooFarFromBall:
            return Striker.GoToBall
        return Striker.TurnForOpponentGoal


class Dribble(State):

    def run(self):
        State.name = "Dribble"
        print("dribbling")
        return True

    def next(self, input):
        return Striker.GoToBall


class SearchBall(State):

    def run(self):
        # TODO start new state machine SearchForBall
        State.name = "SearchBall"
        print("searching")
        return True

    def next(self, input):
        if input == StrikerAction.FoundBall:
            return Striker.GoToBall
        return Striker.SearchBall


class GoToBall(State):

    def run(self):
        State.name = "GoToBall"
        print("going to the Ball")
        return True


    def next(self, input):
        if input == StrikerAction.LostBall:
            return Striker.SearchBall
        if input == StrikerAction.CloseToBall:
            return Striker.TurnForOpponentGoal
        return Striker.GoToBall


class Striker(StateMachine):
    def __init__(self):
        # Initial state
        StateMachine.__init__(self, Striker.TurnForOpponentGoal)


# Static variable initialization:
Striker.TurnForOpponentGoal = TurnForOpponentGoal()
Striker.Shoot = Shoot()
Striker.Dribble = Dribble()
Striker.SearchBall = SearchBall()
Striker.GoToBall = GoToBall()

if __name__ == '__main__':
    s = Striker()
    print(s)
    s.run()
    print(s)
