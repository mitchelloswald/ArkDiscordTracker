import a2s
import discord
from discord.ext import commands, tasks
import json

#Command Prefix
client = commands.Bot(command_prefix = '.')

#Server Ips To Watch, works for all games with 
CI803 = ("95.156.213.149", 27015)
FPE1 = ("149.56.106.59",28015)

#List To Store Enemy Players 
EnemyPlayers = []


 #Start Bot 
@client.event
async def on_ready():
    print("Bot Online")
    checkup.start()
 
 #Gets Player Count 
@client.command()
async def getplayercount(ctx):
    playerdata = a2s.info(CI803)
    await ctx.send("There are " + str(playerdata.player_count) + " Players Connected To " + playerdata.server_name)

 #Gets Players On Server
@client.command()
async def players(ctx):
    players = a2s.players(CI803)
    playerdata = a2s.info(CI803)
    my_list = []
    for name in players:
        my_list.append(name.name)

    await ctx.send("Here are Players That are Currently Connected to " +str(playerdata.server_name) + " " + str(my_list))

 #Adds A Enemy to Your List
@client.command()
async def addenemy(ctx,arg):
    EnemyPlayers.append(arg)
    await ctx.send(arg + " Is Now Being Watched Use Command .enemys to see the full list of watched enemys.")

 #Handle Error
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please Add a Player To Watch")

#Returns Enemy List
@client.command()
async def enemys(ctx):
    await ctx.send(str(EnemyPlayers))

#Gives Update Of the Server with enemys
@client.command()
async def enemyWatcher(ctx):
    players = a2s.players(CI803)
    currentPlayersList = []
    enemysOnServer = []
    for name in players:
        currentPlayersList.append(name.name)

    for i in EnemyPlayers:
        if i in currentPlayersList:
            enemysOnServer.append(i)
    print(str(enemysOnServer))

    if len(enemysOnServer) > 0:
        await ctx.send(str(EnemyPlayers) + " is all online watch out")
    else:
        await ctx.send("No Enemys Online")


@tasks.loop(seconds = 600)
async def checkup():
    channel = client.get_channel(839249727613960252)
    players = a2s.players(CI803)
    serverdata = a2s.info(CI803)
    currentPlayersList = []
    enemysOnServer = []
    for name in players:
        currentPlayersList.append(name.name)

    for i in EnemyPlayers:
        if i in currentPlayersList:
            enemysOnServer.append(i)

    if len(enemysOnServer) > 0:
        await channel.send("This is " + str(serverdata.server_name) + " 10 Minute Update There is " + str(serverdata.player_count) + " Players Online with these enemys connected " + str(enemysOnServer) )
    else:
        await channel.send("This is " + str(serverdata.server_name) + " 10 Minute Update There is " + str(serverdata.player_count) + " Players Online with no enemys Connected")




client.run('')







