import discord
from dotenv import load_dotenv
import os, asyncio
from discord.ext import commands, tasks 
from itertools import cycle
import threading, time, random

load_dotenv()
TOKEN = "ODIwNzg2NzI2NTA3MjQ5NzE1.YE6PNQ.z3nA_QTxdAKENs5yMAJYDgkOD8k"
lock = threading.Lock()

promptlist = []
bot = commands.Bot(command_prefix='?')
@bot.command(name = 'add')
async def add(ctx, prompt) :
    global promptlist
    promptlist.append(prompt) 
    response = "Added " + prompt + "!"
    await ctx.send(response)

@bot.command(name='prompts')
async def prompts(ctx) :
    global promptlist
    if len(promptlist) == 0 : 
        await ctx.send("None!")
    else : 
        response = "0: \"" + promptlist[0] + "\". "
        for i in range(len(promptlist) - 1):
            response += str(i + 1) + ": " 
            response += promptlist[i+1] + " "
        await ctx.send(response)

@bot.command(name = 'remove')
async def remove(ctx, arg) : 
    if int(arg) <= len(promptlist) -1 :
        removed_prompt = promptlist[int(arg)]
        del promptlist[int(arg)]
        response = "Removed " + removed_prompt + "!" 
        await ctx.send(response)
    else : 
        response = "Nothing at position " + arg + "!"
        await ctx.send(response)

@bot.command(name = 'load_prompts')
async def load_prompts(ctx, *args) : 
    global promptlist
    for arg in args: 
        promptlist.append(arg)
    response = "Updated promptlist to " + str(promptlist) + "!"
    await ctx.send(response)

def remove_item(arg) : 
    global promptlist 
    promptlist = promptlist.pop(arg)
    return promptlist 

@bot.command(name = 'commence')
async def commence(ctx): 
    global promptlist 
    while True :
        good_times = [0,3,6]
        if time.gmtime().tm_hour == 11 and time.gmtime().tm_min <= 29 and time.gmtime().tm_hr /2:
            random_num = random.randint(0, len(promptlist) - 1)
            channel = bot.get_channel(816135387339685930)
            await channel.send(promptlist[random_num])
            del promptlist[random_num]
            time.sleep(1800)
        if time.gmtime().tm_day in good_times and time.gmtime().tm_hour == 1 and time.gmtime().min == 0 and time.gmtime.sec == 0 : 
            channel = bot.get_channel(818546231868391454)
            await channel.send(str(promptlist).replace('[', '').replace(']', '').replace(',', '')) 
            time.sleep(60)

    
bot.run(TOKEN)
print("something")
