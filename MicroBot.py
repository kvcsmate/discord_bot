import random

class MicroBot:

    def __init__ (self):
        self.players = set()

    def SetMessage (self, message):
        print(message.content)
        message.content = message.content[7:]
        print(message.content)
        message.content = message.content.lower()
        print(message.content)
        self.message  = message

    async def WriteToChannel (self,  msg):
        await self.message.channel.send(msg)

    async def EventJoin (self):
        self.players.add (self.message.author.name)
        await self.WriteToChannel(self.message.author.name + ' added to the game.')

    async def EventQuit (self):
        self.players.discard (self.message.author.name)
        await self.WriteToChannel(self.message.author.name + ' removed from the game.')

    async def EventStart (self):
        winner = random.choice(tuple(self.players))
        self.players = set ()
        await self.WriteToChannel('The winner is: ' + winner)

    async def HandleMessage (self):
        print("self.message.content: " + self.message.content)
        content = self.message.content
        if content == "join":
            await self.EventJoin ()
        elif content == "quit":
            await self.EventQuit ()
        elif content == "start":
            await self.EventStart ()

microBot = MicroBot ()

async def Micro (message):
    microBot.SetMessage (message)
    await microBot.HandleMessage ()
        