class StrikerAction:
    def __init__(self, action):
        self.action = action

    def __str__(self): return self.action

    def __cmp__(self, other):
        return cmp(self.action, other.action)
    # Necessary when __cmp__ or __eq__ is defined
    # in order to make this class usable as a
    # dictionary key:
    def __hash__(self):
        return hash(self.action)


# Static fields; an enumeration of instances:
StrikerAction.ReadyToShoot = StrikerAction("ready to shoot")
StrikerAction.TooFarFromBall = StrikerAction("too far from ball")
StrikerAction.FacingOpponentsGoal = StrikerAction("facing opponents goal")
StrikerAction.LostBall = StrikerAction("lost ball")
StrikerAction.FoundBall = StrikerAction("found ball")
StrikerAction.CloseToBall = StrikerAction("close to ball")