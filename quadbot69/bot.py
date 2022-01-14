import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import json
import threading
import plotter
import pyrebase
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='nig ',intents=intents)

firebaseConfig = {
    "apiKey": "AIzaSyBXj2Dwqz6wNBtij8FPP8godgqoWGAgKG4",
    "authDomain": "graphwork-91423.firebaseapp.com",
    "databaseURL": "https://graphwork-91423-default-rtdb.firebaseio.com",
    "projectId": "graphwork-91423",
    "storageBucket": "graphwork-91423.appspot.com",
    "messagingSenderId": "988895520746",
    "appId": "1:988895520746:web:e3f93dd84c35c67ef53493",
    "measurementId": "G-89DJSNSYJ8"
  }

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
completed = 0
if db.get().val() == None:
    db.child("ids").set({0:[0]})
    db.child("time").set({'current':''})
def find_member(ctx,member:str):
    try:
        id = int([i.id for i in ctx.message.guild.members if member.lower() in i.name.lower() + '#' + i.discriminator][0])
    except IndexError:
        id = 69
    finally:
        memberobj = get(client.get_all_members(), id=id)
        return memberobj

def form(min):
    day = min//1440
    hour = (min-day*1440)//60
    mins = min-(day*1440+hour*60)
    return day, hour, mins

def landlord():
    threading.Timer(600, landlord).start()
    global completed
    for i in db.child("ids").get():
        if len(i.val()) >= 31:
            i.val().pop(0)
        i.val().append(0)
        db.child("ids").update({i.key(): i.val()})
    completed += 10
    x = form(completed - 10)
    db.child("time").update({"current":f"{x[0]}d {x[1]}h {x[2]}m"})
landlord()


@client.event
async def on_ready():
    print('bot is ready enjoy')
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    else:
        db.child("ids").child("0").remove()
        data = db.child("ids").child(str(message.author.id)).get().val()
        if data == None:
            data = [0]
        data[-1] += 1
        db.child("ids").update({str(message.author.id): data})
        await client.process_commands(message)

@client.command()
async def stat(ctx, member:discord.Member):
    try:
        data = db.child("ids").child(str(member.id)).get().val()
        if data == None:
            await ctx.send("Member has not registered yet.")
        else:
            embed = discord.Embed(title=member.name + "'s Chat Statistics",
                                  description="Completed: "+db.child("time").child("current").get().val(),
                                  color=discord.colour.Colour.from_rgb(89, 179, 105))
            plotter.graph(*data)
            embed.set_image(url="attachment://processed.png")
            file = discord.File(r'processed.png')
            await ctx.send(file=file, embed=embed)
    except AttributeError:
        await ctx.send('Member not found.')


@stat.error
async def stat_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await stat(ctx,ctx.message.author)
    if isinstance(error,commands.MemberNotFound):
        member = find_member(ctx,error.argument)
        await stat(ctx,member)
client.run('TOKEN REMOVED FOR SECURITY REASONS')



