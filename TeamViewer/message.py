class Message():
    def __init__(self, msg_type, payload):
        self.msg_type = msg_type
        #msg_type is "data", "order" or "quit" 
        self.payload = payload
    
    def __repr__(self) -> str:
        return "Message(\"{}\", \"{}\")".format(self.msg_type, self.payload)