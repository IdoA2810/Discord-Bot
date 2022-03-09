import discord
from discord.ext import commands
import LeagueDataBase

TOKEN = "OTMyNjQ4NDg0MjAzNTQ4NzEz.YeWClg.oUO7MG4DhW1a6usSPUxMJTqGy8I"

DB = LeagueDataBase.ORM()
client = commands.Bot(command_prefix='!')
game = False
player1 = None
player2 = None
player1_move = None
player2_move = None

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.command()
async def hello(ctx):
    await ctx.send('Hello!')


@client.command(pass_context=True)
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        player = voice.play()
    else:
        await ctx.send("You are not in a voice channel")

@client.command(pass_context=True)
async def leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
        await ctx.send("I left the voice channel")
    else:
        await ctx.send("I am not in a voice channel")

@client.command(pass_context=True)
async def GetAll(ctx):
    table = DB.get_all()
    await ctx.send(table)

@client.command(pass_context=True)
async def GetTeam(ctx, arg):
    table = DB.get_team(arg)
    await ctx.send(table)

@client.command(pass_context=True)
async def GetPlayer(ctx, arg):
    table = DB.get_player(arg)
    await ctx.send(table)

@client.command(pass_context=True)
async def columns(ctx):
    await ctx.send("(Team, Player, Opponent, Position, Champion, Kills, Deaths, Assists, Creep Score, " \
              "Gold Earned, Champion Damage Share, Kill Participation, Wards Placed, Wards Destroyed, Ward Interactions, " \
              "Dragons For, Dragons Against, Barons For, Barons Against, Result)")

@client.command(pass_context=True)
async def RockPaperScissors(ctx):
    global game
    global player1
    global player2
    if not game:
        game = True
        player1 = ctx.author
        ctx.send(ctx.author + "Started a game of Rock Paper Scissors started, waiting for another player")
    if game and player2 is None and ctx.author != player1:
        player2 = ctx.author
        ctx.send(ctx.author + "has joined the game, please choose, rock, paper, or scissors")

@client.event
async def on_message(message):
    global player1_move
    global player2_move

    msg = message.content.lower()
    if game and (msg == "rock" or message == "paper" or message == "scissors"):
        if message.author == player1 and player1_move is None:
            player1_move = msg


client.run(TOKEN)


