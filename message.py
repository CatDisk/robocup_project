class Message():
    def __init__(self, func, args):
        self.func = func
        self.args = []
        for arg in args:
            self.args.append(arg)