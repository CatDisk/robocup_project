from State import State
from StateMachine import StateMachine


class TurnForOpponentGoal(State):

    def run(self):
        print("turning")

    def next(self, input):
        if input == Striker.ReadyToShoot:
            return Striker.Shoot
        if input == Striker.TooFarFromBall:
            return Striker.GoToBall
        if input == Striker.FacingOpponentsGoal:
            return Striker.Dribble
        return Striker.TurnForOpponentGoal


class Shoot(State):

    def run(self):
        print("shooting")

    def next(self, input):
        if input == Striker.LostBall:
            return Striker.SearchBall
        if input == Striker.TooFarFromBall:
            return Striker.GoToBall
        return Striker.TurnForOpponentGoal


class Dribble(State):

    def run(self):
        print("dribbling")

    def next(self, input):
        return Striker.GoToBall


class SearchBall(State):

    def run(self):
        print("searching")

    def next(self, input):
        if input == Striker.FoundBall:
            return Striker.GoToBall
        return Striker.SearchBall


class GoToBall(State):

    def run(self):
        print("going to the Ball")

    def next(self, input):
        if input == Striker.LostBall:
            return Striker.SearchBall
        if input == Striker.CloseToBall:
            return Striker.TurnForOpponentGoal
        return Striker.GoToBall


class Striker(StateMachine):
    def __init__(self):
        # Initial state
        StateMachine.__init__(self, Striker.TurnForOpponentGoal)


Striker.TurnForOpponentGoal = TurnForOpponentGoal()
Striker.Shoot = Shoot()
Striker.Dribble = Dribble()
Striker.SearchBall = SearcgBall()
Striker.GoToBall = GoToBall()
