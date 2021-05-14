import a2s
from discord.ext import commands, tasks
import config
import db

#Command Prefix
client = commands.Bot(command_prefix = '.')


 #Start Bot 
@client.event
async def on_ready():
    print("Bot Online")
    checkup.start()
 
 #Gets Player Count 
@client.command()
async def getplayercount(ctx):
    playerdata = a2s.info(config.Server)
    await ctx.send("There are " + str(playerdata.player_count) + " Players Connected To " + playerdata.server_name)

 #Gets Players On Server
@client.command()
async def players(ctx):
    players = a2s.players(config.Server)
    playerdata = a2s.info(config.Server)
    my_list = []
    for name in players:
        my_list.append(name.name)

    await ctx.send("Here are Players That are Currently Connected to " +str(playerdata.server_name) + " " + str(my_list))

 #Adds A Enemy to DB
@client.command()
async def addenemy(ctx,*arg):
    #format the arg
    formatted  = ' '.join(arg)
    db.add_enemy(formatted)
    await ctx.send(formatted + " Is Now Being Watched Use Command .enemys to see the full list of watched enemys.")

#Remove Enemy From DB
@client.command()
async def removeenemy(ctx,*arg):
    #format the arg
    formatted  = ' '.join(arg)
    db.remove_enemy(formatted)
    await ctx.send(formatted + " Is Now removed use .enemys to see the full list of watched enemys.")

#Handle Error
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please Add a Player To Watch/Delete")

#Returns Enemy List
@client.command()
async def enemys(ctx):
    playerList = db.enemy_list()
    await ctx.send(str(playerList))

#Gives Update Of the Server with enemys
@client.command()
async def checkEnemys(ctx):
    channel = client.get_channel(config.channelNumber)
    players = a2s.players(config.Server)
    serverdata = a2s.info(config.Server)
    enemysOnServer = []
    watchedEnemys = db.enemy_list()


    #Search for Enemys On The Server
    for name in players:
        #Removes Epic Games Players For Ark Servers
        if len(name.name) > 0:
            if name.name in str(watchedEnemys):
             enemysOnServer.append(name.name)

    formmated = ', '.join(enemysOnServer)

    if len(enemysOnServer) > 0:
        await channel.send("Here are the Connected Enemys " + str(formmated) )
    else:
        await channel.send( "No Enemys Connected")


#Gives Update On Server Every 10 Minutes
@tasks.loop(seconds = 600)
async def checkup():
    channel = client.get_channel(config.channelNumber)
    players = a2s.players(config.Server)
    serverdata = a2s.info(config.Server)
    enemysOnServer = []
    watchedEnemys = db.enemy_list()


    #Search for Enemys On The Server
    for name in players:
        #Removes Epic Games Players For Ark Servers
        if len(name.name) > 0:
            if name.name in str(watchedEnemys):
             enemysOnServer.append(name.name)

    formmated = ', '.join(enemysOnServer)

    if len(enemysOnServer) > 0:
        await channel.send("This is " + str(serverdata.server_name) + " 10 Minute Update There is " + str(serverdata.player_count) + " Players Online with these enemys connected " + str(formmated))
    else:
        await channel.send("This is " + str(serverdata.server_name) + " 10 Minute Update There is " + str(serverdata.player_count) + " Players Online with no enemys Connected")



client.run(config.botKey)







