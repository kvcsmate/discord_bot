import random

class MicroBot:

    def __init__ (self):
        self.players = {}

    def SetMessage (self, message):
        message.content = message.content[7:] 
        message.content = message.content.lower()
        self.message  = message

    def WriteToChannel (self,  msg):
        self.message.channel.send(msg)

    def EventJoin (self):
        self.players.add (self.message.author.name)
        self.WriteToChannel(self.message.author.name + ' added to the game.')

    def EventQuit (self):
        self.players.discard (self.message.author.name)
        self.WriteToChannel(self.message.author.name + ' removed from the game.')

    def EventStart (self):
        winner = random.choice(tuple(self.players))
        self.players = {}
        self.WriteToChannel('The winner is: ' + winner)

    def HandleMessage (self):
        content = self.message.content
        if content == "join":
            self.EventJoin ()
        elif content == "quit":
            self.EventQuit ()
        elif content == "start":
            self.EventStart ()

microBot = MicroBot()

def Micro (message):
    microBot.SetMessage (message)
    microBot.HandleMessage ()
        