import discord
from discord_slash import SlashCommand,SlashContext
from discord.ext import commands
from Designer import Designer
from PIL import Image
from io import BytesIO
import requests
import json
import asyncio
import pyrebase
bot = commands.Bot(command_prefix=["find ","find"])
slash = SlashCommand(bot,sync_commands=True)
bot.remove_command("help")

with open("credential.json",'r') as f:
    creds = json.load(f)
    p_path,apikey,ownerids,token = creds["poster_path"],creds["_apiKey"],creds["owners"],creds["token"]


movie_url = f"https://api.themoviedb.org/3/search/movie?api_key={apikey}&language=en-US&page=1&include_adult=false&query="
tv_url = f"https://api.themoviedb.org/3/search/tv?api_key={apikey}&language=en-US&page=1&include_adult=false&query="
elements = ["title","release_date","overview","vote_average","poster_path","genre_ids","original_language","backdrop_path"]
elements2 = ["name","first_air_date","overview","vote_average","poster_path","genre_ids","original_language","backdrop_path"]
async def get_data(url,query):
    data = requests.Session().get(url=url+query)
    return data.json()
async def genre_generator(ids):
    with open("genre.json","r") as file:
        data = json.load(file)
    return (i.get("name") for i in data["genres"] if i.get("id") in ids.get("genre_ids"))

async def lang_gen(code):
    with open("lang.json","r",encoding="utf8") as lang:
        data = json.load(lang)
    if data.get(code) is not None: return data.get(code).get("name")

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




@bot.event
async def on_ready():
    print(bot.user.name+" is ready to go.")
    with open("credential.json",'r') as f:
        status = json.load(f)['status']
    await bot.change_presence(activity=discord.Game(name=status))

@bot.event
async def on_message(message):
    ctx = await bot.get_context(message)
    if str(bot.user.id) in message.content:
        await help(ctx)
    if db.child("img").child(ctx.message.guild.id).get().val() is None:
        db.child("img").update({ctx.message.guild.id:3})
    await bot.process_commands(message)


@bot.event
async def on_guild_join(guild):
    db.child("img").update({guild.id:4})


@bot.command(brief="Sends Movie Details related to the query provided.")
async def movie(ctx,*,movie,url=movie_url,elem=None,page=0,guild_id=None,msg=None):
    if guild_id is None:
        guild_id=ctx.message.guild.id
    if elem is None:
        elem = elements
    mov = await get_data(url,"%20".join(movie.split()))
    mov = mov.get("results")
    if len(mov) != 0:
        if db.child("img").child(guild_id).get().val() is None:
            db.child("img").update({guild_id:2})
        datas = [db.child("img").child(guild_id).get().val()]
        for i in elem:
            if all((i=="poster_path",mov[page].get(i) != None)):
                datas.append(p_path+mov[page].get(i))
            elif all((i=="backdrop_path",mov[page].get(i) != None)):
                datas.append(p_path+mov[page].get(i))
            elif all((i=="genre_ids",mov[page].get(i) != None)):
                datas.append([*await genre_generator(mov[page])])
            elif all((i=="original_language",mov[page].get(i) != None)):
                datas.append(await lang_gen(mov[page].get(i)))
            else:
                datas.append(mov[page].get(i))
        movie_info = Designer(*datas)
        image = await movie_info.design()
        with BytesIO() as binary:
            image.save(binary,'JPEG')
            binary.seek(0)
            if msg is None:
                msg = await ctx.send(file=discord.File(fp=binary,filename=datas[1].replace(' ','_')+'.jpg'))
                return
            await msg.edit(content=None,file=discord.File(fp=binary,filename=datas[1].replace(' ','_')+'.jpg'))
            return 
    if msg is None:
        await ctx.send("No results Found.")
        return
    await msg.edit(content="No results found.")

@slash.slash(
    name="movie",
    description="Sends Movie Details related to the query provided.",
    guild_ids=[i.id for i in bot.guilds]
)
async def _movie(ctx:SlashContext,query:str):
    msg = await ctx.send("Searching in progress...")
    await movie(ctx,movie=query,guild_id=ctx.guild_id,msg=msg)


@bot.command(brief="Sends Show details related to the query provided.")
async def show(ctx,*,show):
    await movie(ctx,movie=show,url=tv_url,elem=elements2)
@slash.slash(
    name="show",
    description="Sends TV Show/Series Details related to the query provided.",
    guild_ids=[i.id for i in bot.guilds]
)
async def _show(ctx:SlashContext,query:str):
    msg = await ctx.send("Searching in progress...")
    await movie(ctx,movie=query,url=tv_url,elem=elements2,guild_id=ctx.guild_id,msg=msg)


@bot.command(brief="Shows Credits of the Bot.")
async def credits(ctx):
    embed = discord.Embed(
        title = "Credits",
        description="**Developer:** Sauce\n**API Service:** The Movies Database(TMDB)"
    )
    embed.set_image(url="https://i.imgur.com/06TN43J.png")
    await ctx.send(embed=embed)



@bot.command(brief="Sends this Message.")
async def help(ctx):
    plshelp = discord.Embed(
        title="Help",
        description="Hello, my prefix is `find`.",
        color = discord.Colour.from_rgb(255, 175, 30)
        )
    for command in bot.commands:
        if command.name is not None and command.brief is not None:
            plshelp.add_field(name=f"`{command.name}`",value=command.brief,inline=False)
    await ctx.send(embed=plshelp)





@bot.command(brief="Configures Image Resolution.")
async def setres(ctx):
    emojis = ('<:one:869230816377569350>','<:two:869230887676571688>','<:three:869230949676761198>','<:four:869231009596588103>')
    resemb = discord.Embed(
        title="Set your Favourable Resolution",
        description="""
        :one: - **Lowest** [Fastest]\n
        :two: - **Low** [Fast]\n
        :three: - **High** [Slow]\n
        :four: - **Highest** [Slowest]
        """,
        color=discord.Colour.from_rgb(125,250,175)
        )
    async def reactions(message:discord.Message):
        for i in emojis:
            await message.add_reaction(i)
    beginem = discord.Embed(title="Loading...",color=discord.Colour.from_rgb(125,250,175))
    msg = await ctx.send(embed=beginem)
    #await asyncio.wait([reactions(msg)])
    await asyncio.wait([asyncio.create_task(reactions(msg))])
    await msg.edit(embed=resemb)
    try:
        react,user = await bot.wait_for("reaction_add",timeout=20,check=lambda react,user:user == ctx.message.author and str(react.emoji) in emojis)
    except asyncio.TimeoutError:
        beginem.title = "Timed out"
        beginem.color = discord.Colour.from_rgb(255,0,0)
        await msg.edit(embed=beginem)
    else:
        if str(react) == emojis[0]:
            db.child("img").update({ctx.message.guild.id:1})
        elif str(react) == emojis[1]:
            db.child("img").update({ctx.message.guild.id:2})
        elif str(react) == emojis[2]:
            db.child("img").update({ctx.message.guild.id:3})
        elif str(react) == emojis[3]:
            db.child("img").update({ctx.message.guild.id:4})
        beginem.title = "Success"
        beginem.description = "Image was set to specified resolution successfully."
        beginem.color = discord.Colour.from_rgb(0,255,0)
        await msg.edit(embed=beginem)

@bot.command(brief="Shows the current resolution of the image in Server.")
async def currentres(ctx):
    await ctx.send("Current Resolution: "+ str(db.child("img").child(ctx.message.guild.id).get().val()))



@bot.command(name = None,brief=None)
async def status(ctx,*,stat:str):
    if ctx.message.author.id not in ownerids:
        return 
    with open('credential.json','r') as file:
        await bot.change_presence(activity=discord.Game(name=stat))
        data = json.load(file)
        data['status'] = stat
    with open('credential.json','w') as file:
        json.dump(data,file)
    await ctx.send("Success.")

@bot.command(name=None,brief=None)
async def servers(ctx):
    for i in bot.guilds:
        await ctx.send(i.name)


@bot.command(name="invite",brief="Generates an invite bot.")
async def invite(ctx):
    emb = discord.Embed(
        title="Invite Film Buddy",
        description='[Invite Bot](https://discord.com/oauth2/authorize?client_id=844062118620823593&permissions=51200&scope=bot)',
        color=discord.Colour.from_rgb(125,250,175)
        )
    await ctx.send(embed=emb)

@slash.slash(
    name="invite",
    description="Sends an invite link of Film Buddy.",
    guild_ids = [i.id for i in bot.guilds]
)
async def _invite(ctx:SlashContext):
    await invite(ctx)


if __name__ == '__main__':
    bot.run(token)















