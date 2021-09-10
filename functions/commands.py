'''
Code written by Ryan Helgoth, references I used have been cited in the comments.

This is file contains code for commands used by the bot.
'''

''' 
Link: https://stackoverflow.com/a/27365730
Author: Kevin
Date: Dec 8 '14 at 19:50
License: SA 3.0

I used this post to help fix an issue 
I had with importing "commandHelpers".
'''
from . import commandHelpers as ch
import discord 
import random

'''
Displays help embed which contains a link explaining how to use the bot's commands.
'''
async def help(ctx):
    ''' 
    Link: https://stackoverflow.com/a/64529788
    Author: stijndcl
    Date: Oct 25 '20 at 23:17
    License: SA 4.0

    I used this post to learn how to send
    hyperlinks with the bot.
    '''
    embed = discord.Embed()

    embed = discord.Embed(title="Cần sự giúp đỡ? Yên tâm tao không phải là Fong!",
                          description=":keyboard: Đây là các lệnh cơ bản cho chúng mày!")
    embed.set_author(name=" From Cụ with Love <3", url="https://facebook.com/quanghuy205")
    embed.add_field(name=":small_blue_diamond: !showteams ", value="Hiển thị cụ và 9 thằng ngu", inline=False)
    embed.add_field(name=":small_blue_diamond: !setmainchat", value="Chỉ định kênh voice chính", inline=False)
    embed.add_field(name=":small_blue_diamond: !setteamchat1", value="Chỉ định kênh voice team 1", inline=False)
    embed.add_field(name=":small_blue_diamond: !setteamchat2", value="Chỉ định kênh voice team 2", inline=False)
    embed.add_field(name=":small_blue_diamond: !maketeam1", value="Tạo team 1. Tag tên chúng nó vào và cách nhau bởi 1 dấu cách",
                    inline=False)
    embed.add_field(name=":small_blue_diamond: !maketeam2", value="Như trên", inline=False)
    embed.add_field(name=":small_blue_diamond: !randomize", value="Random ra 2 team, lấy người ở kênh voice chính!", inline=False)
    embed.add_field(name=":small_blue_diamond: !randomizeExculde", value="Random ra 2 team, lấy người ở kênh voice chính trừ những thằng được tag!",
                    inline=False)
    embed.add_field(name=":small_blue_diamond: !movetoteams", value="Chuyển 2 team về các kênh voice", inline=False)
    embed.add_field(name=":small_blue_diamond: !movetomain", value="Chuyển hết về kênh voice chính", inline=False)
    await ctx.send(embed=embed)


'''
This function displays the members in team 1 and 2.
'''


async def printTeams(ctx, db):
    userID = ctx.message.author.id
    teams = {"team1" : [], "team2" : []} #Keys are db vars and values are for holding user ids.
    docRef = ch.getDocRef(ctx, db)
    doc = docRef.get()

    if doc.exists:
        data = doc.to_dict()
        for team in teams:
            error = False
            teamName = "T" + team[1:4] + " " + team[-1] #Gets "Team X" string from "teamX" string.
            if team in data:
                teamMembers = data[team]
                for memberID in teamMembers:
                    try:
                        memberID = int(memberID) 
                    except ValueError:
                        await ctx.send("Ngu: <@{0}>'s Lỗi mẹ rồi, tạo lại {1} đi!".format(userID, teamName.lower()))
                        error = True
                        break #Trys to show team 2 even if there is an error with team 1
                    
                    member = ctx.guild.get_member(memberID)
                    if member is None:
                        await ctx.send("<@{0}> Ngu: Đéo tìm thấy ai ở {1}, tạo lại {1} đi!".format(userID, teamName.lower()))
                        error = True
                        break #Trys to show team 2 even if there is an error with team 1
                    else:
                        teams[team].append("<@" + str(memberID) + ">")
            if not error:
                await ctx.send(":video_game: {0}: {1}".format(teamName, ", ".join(map(str, teams[team]))))
    else:
        await ctx.send("Chưa tìm thấy team nào đã lưu. Tạo mới đi!.")

'''
Randomly splits users from the main channel into 2 teams and saves them
in the database for the user who entered the command.
'''


async def randomizeMainExclude(ctx, db, args):
    '''
    Randomization is done by shuffling the members in the main channel
    and then spliting the list of members in half to form two teams.
    '''
    userID = ctx.message.author.id
    docRef = ch.getDocRef(ctx, db)
    doc = docRef.get()
    exmembers = []

    #them exclude
    # Populates members list with user id's
    for arg in args:
        try:
            exmemberID = int(arg[3:-1])  # Strips away characters to get id from <@id>
        except ValueError:
            await ctx.send("Ngu: Nhập sai tên rồi. tag chúng nó vào bằng dấu \"@\".")
            return

        exmember = ctx.guild.get_member(exmemberID)
        if exmember is None:
            # await ctx.send("Error: could not find one or more selected users. Please tag users you want to add, " +
            # "by typing \"@\" and selecting users. Please also seperate each tagged user with 1 space.")
            await ctx.send("Ngu: đéo tìm thấy ai, tag chúng nó vào , " +
                           "bằng dấu \"@\". Thêm dấu cách vào giữa tên chúng nó.")
            return

        if not exmember in exmembers:
            exmembers.append(str(exmember.id))
        else:
            await ctx.send("Ngu: Đéo thể add 1 thằng vào 1 team 2 lần.")
            return
        print(exmembers)

    if doc.exists:
        data = doc.to_dict()
        if "voiceMain" in data:
            try:
                channelID = int(data["voiceMain"])
            except ValueError:
                await ctx.send("Ngu: <@{}>'s main channel lỗi mẹ rồi, set lại đi!".format(userID))
                return

            mainChannel = discord.utils.get(ctx.guild.channels, id=channelID)
            if mainChannel is None:
                await ctx.send("Ngu: Đéo tìm thấy main channel, Set lại đê!.")
            else:
                members = mainChannel.members

                #add them exclude



                memberIDS = [str(member.id) for member in members]
                print(memberIDS)

                memberIDS= [i for i in exmembers + memberIDS if i not in exmembers or i not in memberIDS]
                print(memberIDS)
                if len(memberIDS) > 1:
                    random.shuffle(memberIDS)
                    half = len(memberIDS) // 2
                    team1 = memberIDS[0:half]
                    team2 = memberIDS[half:len(memberIDS)]
                    data = {"team1": team1, "team2": team2}
                    docRef.set(data, merge=True)
                    await ctx.send("Đã random 2 teams trong kênh <#{}>:".format(channelID))
                    await printTeams(ctx, db)
                else:
                    await ctx.send(
                        "Phải có 2 người trở lên ở kênh <#{}> để sử dụng lệnh này.".format(channelID))
        else:
            await ctx.send("Set kênh voice chính đã trước khi sử dụng lệnh này.")
    else:
        await ctx.send("Set kênh voice chính đã trước khi sử dụng lệnh này.")


async def randomizeMain(ctx, db):
    '''
    Randomization is done by shuffling the members in the main channel
    and then spliting the list of members in half to form two teams.
    '''
    userID = ctx.message.author.id
    docRef = ch.getDocRef(ctx, db)
    doc = docRef.get()

    if doc.exists:
        data = doc.to_dict()
        if "voiceMain" in data:
            try:
                channelID = int(data["voiceMain"]) 
            except ValueError:
                await ctx.send("Ngu: <@{}>'s main channel lỗi mẹ rồi, set lại đi!".format(userID))
                return
            
            mainChannel = discord.utils.get(ctx.guild.channels, id = channelID) 
            if mainChannel is None:
                await ctx.send("Ngu: Đéo tìm thấy main channel, Set lại đê!.")
            else:
                members = mainChannel.members

                memberIDS = [str(member.id) for member in members]
                if len(memberIDS) > 1: 
                    random.shuffle(memberIDS)
                    half = len(memberIDS) // 2
                    team1 = memberIDS[0:half]
                    team2 = memberIDS[half:len(memberIDS)]
                    data = {"team1" : team1, "team2" : team2}
                    docRef.set(data, merge = True)
                    await ctx.send("Đã taọ 2 team với members từ kênh <#{}>:".format(channelID))
                    await printTeams(ctx, db)
                else:
                    await ctx.send("Phải có 2 người trở lên ở kênh <#{}> để sử dụng lệnh này.".format(channelID))
        else:
            await ctx.send("Set kênh voice chính đã trước khi sử dụng lệnh này.")
    else:
        await ctx.send("Set kênh voice chính đã trước khi sử dụng lệnh này.")

'''
This function lets the user pick a preference for their main
channel and then saves it in the database. 
'''


async def setChannel(ctx, db, args, chat):
    userID = ctx.message.author.id
    channelName = " ".join(args)
    docRef = ch.getDocRef(ctx, db)
    chats = {"Team 1" : "voice1", "Team 2" : "voice2", "Main" : "voiceMain"} #Values are the variable names in the db.
    channel = discord.utils.get(ctx.guild.channels, name = channelName)

    if channel is None:
        await ctx.send("Đéo tìm thấy kênh nào tên \"{}\", thử lại đi.".format(channelName))
    elif str(channel.type) != "voice":
        await ctx.send("Ngu vãi loz, <#{}> đéo phải kênh voice, set lại kênh voice đi.".format(channel.id))
    else:
        data = {chats[chat] : str(channel.id)}
        docRef.set(data, merge = True)
        await ctx.send("kênh {} đã được set vào <#{}>".format(chat.lower(), channel.id))

'''
This function lets the user make a team and then then saves the team 
in the database.
'''
async def makeTeam(ctx, db, args, teamName):
    userID = ctx.message.author.id
    docRef = ch.getDocRef(ctx, db)
    doc = docRef.get()
    members = [] #NOTE this list now contains user id strings and not member objects.
    teams = {"Team 1" : "team1", "Team 2" : "team2"}
    teamRef = teams[teamName]

    #Populates members list with user id's 
    for arg in args:
        try:
            memberID = int(arg[3:-1]) #Strips away characters to get id from <@id>
        except ValueError:
            await ctx.send("Ngu: Nhập sai tên rồi. tag chúng nó vào bằng dấu \"@\".")
            return
        
        member = ctx.guild.get_member(memberID)
        if member is None:
            # await ctx.send("Error: could not find one or more selected users. Please tag users you want to add, " +
            # "by typing \"@\" and selecting users. Please also seperate each tagged user with 1 space.")
            await ctx.send("Ngu: đéo tìm thấy ai, tag chúng nó vào , " +
                           "bằng dấu \"@\". Thêm dấu cách vào giữa tên chúng nó.")
            return

        if not member in members:
            members.append(str(member.id))
        else:
            await ctx.send("Ngu: Đéo thể add 1 thằng vào 1 team 2 lần.")
            return

    #Saves team to db
    if doc.exists:
        data = doc.to_dict()
        if teamRef in data:
            opposingTeamNum = str((int(teamRef[-1]) % 2) + 1) #Gets number of opposing team.
            opposingTeamName = "Team " + opposingTeamNum 
            opposingTeamRef = teams[opposingTeamName] #Gets db var name for opposing team
            opposingTeam = data[opposingTeamRef]
            if not set(members).isdisjoint(opposingTeam):
                #Removes members in the opposing team who are being added to team choosen by the user.
                opposingTeam = list(set(opposingTeam) - set(members))
                data = {opposingTeamRef : opposingTeam}
                docRef.set(data, merge = True)
                await ctx.send("Note: Một số thằng được move từ <@{0}>'s {1} tới <@{0}>'s {2}.".format(userID, opposingTeamName.lower(), teamName.lower()))
    
    data = {teamRef : members}
    docRef.set(data, merge = True)
    await ctx.send("Thêm người thành công: ")
    await printTeams(ctx, db)

'''
Moves users to a voice channel set by the user.
'''
async def moveToChannel(ctx, db, location):
    docRef = ch.getDocRef(ctx, db)
    doc = docRef.get()
    teams = {"team1" : "voice1", "team2" : "voice2"} #Keys are db var names for lists of member ids and values are db vars for channel ids.

    if location == "teams":
        await ch.sendToTeams(ctx, doc, teams)
    elif location == "main":
        await ch.sendToMain(ctx, doc, teams)

