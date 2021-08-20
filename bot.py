# bot.py
import os
import random
import json
import pytesseract
import cv2
from PIL import Image
import googleapiclient.discovery
from urllib.parse import parse_qs, urlparse

# pylint: disable=E1101
import discord
from dotenv import load_dotenv
isitalib = False


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

def nudes():
    with open(__file__) as f:
        return f.read()

def textfromimage(image_path):
    path_to_tesseract = 'r'+ os.getenv('TESSERACT_PATH')
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ksize = (30, 30)
    blur = cv2.blur(gray, ksize, cv2.BORDER_DEFAULT)
    mean = cv2.mean(blur)[0]
    if  mean < 127:
        gray = cv2.bitwise_not(gray)
    pytesseract.tesseract_cmd = path_to_tesseract
    text = pytesseract.image_to_string(gray)
    return(text[:-1])
def youtubelinkfromlist():

    #url-ből playlist id kinyerése
    url = 'https://www.youtube.com/playlist?list=PLjtdIihFSPBOCe6XCWaCyBd_uvRQd5Jk4'
    query = parse_qs(urlparse(url).query, keep_blank_values=True)
    playlist_id = query["list"][0]
    api_key= str(os.getenv('GOOGLE_API'))
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey = api_key)
    request = youtube.playlistItems().list(
    part = "snippet",
    playlistId = playlist_id,
    maxResults = 50
    )
    response = request.execute()
    playlist_items = []
    while request is not None:
        response = request.execute()
        playlist_items += response["items"]
        request = youtube.playlistItems().list_next(request, response)
    linklist=[]
    for t in playlist_items:
        linklist.append(f'https://www.youtube.com/watch?v={t["snippet"]["resourceId"]["videoId"]}&list={playlist_id}&t=0s')
    return linklist

def rollfunction(input):
    input= input[5:]
    sum=0
    if 'd' in input:
        if input.startswith('d'):
            dicenumber=1
        else:
            dicenumber=int(input[:input.index('d')])
        dicesize=int(input[input.index('d')+1:])

        if dicesize==0:
            return -1
        for _ in range (dicenumber):
            sum+=random.randint(1,dicesize)
    else:
        dicesize=int(input)
        if dicesize==0:
            return -1
        sum+=random.randint(1,dicesize)
    return sum

def dadjoke(input):
    joke=''
    if 'vagyok' in input:
        wrd_list=input[:input.index('vagyok')].split()
        joke='Szia '+wrd_list[-1]+'!'
    return joke

    #main
linklist=[]
linklist=youtubelinkfromlist()
#print(linklist[0])
gamelist = {}
curruser = ""



client = discord.Client()
image_types = ["png", "jpeg", "gif", "jpg"]


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    global isitalib
    msg = message.content.lower()
    if 'malzorbot' in msg:
        await message.channel.send('Fuck off')
        if message.author.name == "vacfornothing":
            await message.channel.send('shut up Zétény')

    if msg.startswith('roll'):
        result = rollfunction(msg)
        if result == -1:
            await message.channel.send(file=discord.File("C:/Users/User/Documents/memes/howdareyou.jpg"))
        else:
            await message.channel.send(result)
            if result == 1:
                await message.channel.send('gratulálok, 1est dobtál.Itt a jutalmad:')
                await message.channel.send(file=discord.File("C:/Users/User/Documents/memes/reactions/you lost.jpg"))
    if msg == 'malzorbot vagyok':
        await message.channel.send(file=discord.File("C:/Users/User/Documents/memes/reactions/crossover episode.jpg"))
    if 'vagyok' in msg and not msg.startswith('vagyok'):
        await message.channel.send(dadjoke(msg))
    if msg == '!send meme':
        rand = random.randint(0, 1)
        if (rand):
            fp = random.choice(os.listdir("C:/Users/User/Documents/memes/"))
            await message.channel.send(file=discord.File("C:/Users/User/Documents/memes/{}".format(fp)))
        else:
            fp = random.choice(linklist)
            await message.channel.send(fp)
    if msg == 'hit it':
        await message.channel.send('Hey, Péter Kecskés.Ez ment a fejedben?')
        await message.channel.send(f'https://youtu.be/u6LahTuw02c')
    if msg == "!send nudes":
        rand = random.randint(0, 2)
        if rand == 0:
            message.channel.send('( . Y . )')
        elif rand == 1:
            fp = random.choice(os.listdir("C:/Users/User/Documents/memes/nudes"))
            await message.channel.send(file=discord.File("C:/Users/User/Documents/memes/nudes/{}".format(fp)))
        elif rand == 2:
            await message.channel.send('╰⋃╯')
    if msg.startswith("!games"):
        if msg[6:] == " add":
            isitalib = True
            gamelist[message.author.name] = message.author.name
            print(gamelist[message.author.name])
        for attachment in message.attachments:
            if any(attachment.filename.lower().endswith(image) for image in image_types) and isitalib:  #
                await attachment.save(attachment.filename)
                raw = textfromimage(attachment.filename)
                raw = raw.replace("\n", ", ")
                raw = raw.replace(" - Update Queued", "")
                raw = raw.replace(" - Update Paused", "")
                raw = raw.replace("  ", " ")
                raw = raw.replace(",,", ",")
                gamelist[message.author.name] = raw
        if msg[6:] == " players":
            items = "current players: "
            playerlist = gamelist.keys()
            for item in playerlist:
                items += item + " "
            await message.channel.send(items)
            print(items)
        if msg[6:] == " show":
            await message.channel.send(gamelist.items())
        # code=nudes()
        # await message.channel.send(code[:2000])


client.run(TOKEN)