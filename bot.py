import discord
import os
import requests
import json
from discord import client
from discord.ext import commands
from dotenv import load_dotenv
from requests.models import Response
import time
import random
import scrape

load_dotenv()
TOKEN = os.getenv('TOKEN')

client = commands.Bot(command_prefix="!", help_command=None)

#get ratings
def get_rating(handle):
    try:
        response = requests.get(f"https://codeforces.com/api/user.rating?handle={handle}")
        
    except requests.exceptions.RequestException as e:
        print(e)

    json_data = json.loads(response.text)

    if( json_data['status'] == "FAILED" or len(json_data["result"]) == 0):
        return (f"```{handle} is not a codeforces handle, please enter the correct username!```")

    name = json_data["result"][0]["handle"]
    rating = str(json_data["result"][-1]["newRating"])
    ans = "```"+ name + " : " + rating + "```"
    return(ans)


#get cf upcoming contests
def get_contestlist_cf():
    try:
        response = requests.get("https://codeforces.com/api/contest.list?gym=false")
    except requests.exceptions.RequestException as e:
        print(e)
        ans = "Try Again After Some Time"
        return(ans)

    json_data = json.loads(response.text)
    s = ""
    for i in range(100):
        contest = json_data["result"][i]

        if contest["phase"] == "BEFORE":
            duration = (contest["durationSeconds"])/3600
            durationInHour = int(duration)
            durationInMin  = int((duration - durationInHour)*60)

            contestTime = contest["startTimeSeconds"]
            t = time.ctime(contestTime)
            id_contest = contest["id"]
            if durationInMin == 0:
                dur = f"({durationInHour}h)\n"
            else:
                dur = f"({durationInHour}h {durationInMin}m)\n"
            
            s= s+ f'```{contest["name"]} ```' + "```"+ dur + "```\n" + f'```{t}```\n'+ f'https://codeforces.com/contests/{id_contest}' +'''\n\n'''

        else:
            break 
        
    
    return(s)

    
def getQuestions(tag):
    try:
        response = requests.get(f"https://codeforces.com/api/problemset.problems?tags={tag}")
    
    except requests.exceptions.RequestException as e:
        print(e)
        

    json_data = json.loads(response.text)
    newtag = tag.replace('+', " ")
    if(json_data['status'] == "FAILED"):
        return (f"```{newtag} is not a codeforces valid Tag!```")

    length= len(json_data['result']['problems'])
    if(length == 0):
        return (f"```{newtag} is not a codeforces valid Tag!```")

    p_no = random.randint(0,length-1)
    problem = json_data['result']['problems'][p_no]
    contestId = problem['contestId']
    index = problem['index']

    question = f"https://codeforces.com/contest/{contestId}/problem/{index}"
    return question

def getInfo(handle):
    try:
        response = requests.get(f"https://codeforces.com/api/user.info?handles={handle}")

    except requests.exceptions.RequestException as e:
        print(e)
        
    json_data = json.loads(response.text)

    if( json_data['status'] == "FAILED"):
        return (f"```{handle} is not a codeforces handle, please enter the correct username!```")

    if 'rating'in json_data["result"][0]:

        json_data = json.loads(response.text)['result'][0]
        rating = json_data['rating']
        max_rating = json_data['maxRating']
        pic = json_data['titlePhoto']
        rank = json_data['rank']
        contributions = json_data['contribution']
        friends = json_data['friendOfCount']
        s = "```Current Rating : " + str(rating) + "\nMaximum Rating : " + str(max_rating) +"\nRank : "+ rank + "\ncontributions : " + str(contributions) + "\nFriends : " + str(friends) +"```\n"+ pic

    else :
        return f"```{handle} has not participated in any rated contest.```"



    return s



@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.command()
async def rating(ctx, arg):
    ans = get_rating(arg)
    await ctx.send(ans)

@client.command()
async def getcontests(ctx):
    contests_cf = get_contestlist_cf()
    await ctx.send(contests_cf)

@client.command()
async def question(ctx, *args):
    s = '{}'.format('+'.join(args))
    ans = getQuestions(s)
    await ctx.send(ans)

    if not ans:
        await ctx.send("something went wrong")

@client.command()
async def topDTU(ctx):
    users = scrape.top10()
    user_stats = ""
    i=1
    for user in users:
        user_name = user
        user_rating = get_rating(user_name)
        user_stats += f"```{i}```" +". " + user_rating + "```(Current Rating)```\n\n"
        i=i+1

    await ctx.send(user_stats)

@client.command()
async def info(ctx, arg):
    s = getInfo(arg)
    await ctx.send(s)

@client.command()
async def help(ctx):
    await ctx.send(f'Hello {ctx.message.author.mention}!, Here are some things you can try')
    await ctx.send("```Hello, I am CodeForces Bot :) , I help you folks maintain a healthy coding competition and practice competitive programming together."
                
                   +"\n\nYou can control me by sending these commands :\n\n" 
                   +"!getcontests : Returns list of upcoming codeforces contests.\n\n"
                   +"!rating {user_name} : Returns the current codeforces rating of the user.\n\n"
                   +"!question {tag_name(s)} : Returns a random question filtered by the tag name(s) you mention.\n\n"
                   +"!topDTU : Returns the top 10 competitive programmers of Delhi Technological University on codeforces.\n\n"
                   +"!info {user_name} : Returns information about the user you mentioned.\n\n"
                   +"!help : shows this help message.\n\n"
                   "Happy Coding!```")


client.run(TOKEN)