import discord
from discord.ext import commands
from discord.utils import get
import threading
import plotter
import pyrebase
import googletrans
from googletrans import Translator
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='>',intents=intents,case_insensitive=True)
firebaseConfig = {
    #database credentials
  }
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
if db.get().val() == None:
    db.child("ids").set({0:[0]})
    db.child("time").set({'current':0})
def find_member(ctx,member:str):
    try:
        id = [i.id for i in ctx.message.guild.members if any([member.lower() in i.name.lower()+'#'+i.discriminator,False if i.nick is None else member.lower() in str(i.nick).lower()])][0]
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
    for i in db.child("ids").get():
        if len(i.val()) >= 31:
            i.val().pop(0)
        i.val().append(0)
        db.child("ids").update({i.key(): i.val()})
    time = db.child("time").child("current").get().val()+10
    db.child("time").update({"current":time})
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
            time = db.child("time").child("current").get().val()
            format = form(int(time))
            embed = discord.Embed(title=member.name + "'s Chat Statistics",
                                  description="Completed: "+f"{format[0]}d {format[1]}h {format[2]}m",
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


@client.command()
async def translate(ctx,*,msg_to_be_translated:str=None):
    def trans(msg):
        languages = googletrans.LANGUAGES
        try:
            t = Translator().translate(msg)
            return f'**Language:** {languages[t.src]}\n**Translation:** {t.text}'
        except Exception:
            return 'An error occured.'
    if msg_to_be_translated is None:
        reply_msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        await ctx.send(trans(reply_msg.content))
    else:
        await ctx.send(trans(msg_to_be_translated))



if __name__ == '__main__':
    client.run('CENSORED TOKEN')



