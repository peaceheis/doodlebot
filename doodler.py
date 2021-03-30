import discord
from discord.ext import commands, tasks 
import datetime, random, asyncio 

TOKEN = ""

promptlist = []

bot = commands.Bot(command_prefix='?')

async def send_prompts():
    global promptlist
    await bot.wait_until_ready()
    rn = datetime.datetime.now()
    channel = bot.get_channel(818546231868391454)
    good_times = [0, 2, 4]
    while True : 
        if rn.hour == 18 and rn.min <= 50 and len(promptlist) > 0 :
            random_num = random.randint(0, len(promptlist) - 1)
            channel = bot.get_channel(816135387339685930)
            await channel.send(promptlist[random_num])
            del promptlist[random_num]
            if len(promptlist) <= 10 and len(promptlist) != 1 : 
                await ctx.send(f"**Warning!** Only **{len(promptlist)}** prompts left!")
            elif len(promptlist) == 1 : 
                await ctx.send(f"**Strong Warning!** Only 1 prompt left!")
            elif len(promptlist) == 0 : 
                await ctx.send(f"**CRITICAL WARNING!** 0 prompts left!!")
            del promptlist[random_num]
            time.sleep(10)
        if rn.weekday in good_times and rn.hour == 18 and rn.minute <= 50 : 
            channel = bot.get_channel(818546231868391454)
            await back_up(ctx)
            time.sleep(15)
        
        
@bot.command(name = 'add')
async def add(ctx, prompt) :
    global promptlist
    promptlist.append(prompt) 
    response = "Added " + prompt + "!"
    await ctx.send(response)

@bot.command(name = 'remove_multiple') 
async def remove_multiple(ctx, *args) :
    global promptlist
    for arg in args: 
        try :
            del promptlist[int(arg)]
        except : 
            pass
    await ctx.send("Cleared requested prompts!")
    
@bot.command(name = 'clear_prompts')
async def clear_prompts(ctx) : 
    global promptlist
    promplist = []
    await ctx.send("Cleared all prompts!")
    
@bot.command(name = 'prompt')
async def prompt(ctx, num) : 
    global promptlist
    if num < len(promptlist) : 
        response = f"Prompt {num}: {promptlist[num]}"
    else : 
        response = f"{num} is out of range!"
    await ctx.send(response)
    
@bot.command(name='prompts')
async def prompts(ctx) :
    global promptlist
    if len(promptlist) == 0 : 
        await ctx.send("None!")
        return
    response = "**Prompts**: \n" + str(promptlist).replace('[', '').replace(']', '')
    if False :
        pass
    else : 
        response_list = promptlist
        current_char = 0 
        count = 0
        count1 = 0 
        should_continue = True
        while should_continue :
            current_response = ""         
            for i in range(25) :
                try :
                    current_response += str(count1) + ": "                    
                    current_response += response_list[count1].replace('\'', "")
                    current_response += " "
                    count1 += 1
                except : 
                    await ctx.send(current_response)
                    return
            count += 1
            current_response = current_response + "(" + str(count) + ")"
            await ctx.send(current_response)

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
    if len(response) <= 2000 :
        await ctx.send(response)
    else : 
        response = "I can't show you the whole list, but you can rest assured everything went well. Feel free to use ?prompts! :wink:"
        await ctx.send(response)
        
@bot.command(name = 'num_prompts')
async def num_prompts(ctx) :
    global promptlist
    await ctx.send("There are " + str(len(promptlist)) + " prompts!")
                  
           
@bot.command(name = 'back_up') 
async def back_up(ctx) : 
    channel = bot.get_channel(818546231868391454)
    global promptlist
    if len(promptlist) == 0 : 
        await channel.send("Nothing to back up!")
        return
    response = "**Backup**: \n" + str(promptlist).replace('[', '').replace(']', '')
    if len(response) <= 1980 :
        await channel.send(response) 
    else : 
        response_list = promptlist
        current_char = 0 
        count = 0
        count1 = 0 
        should_continue = True
        while should_continue :
            current_response = ""         
            for i in range(25) :
                try :
                    current_response += '\"'
                    current_response += response_list[count1].replace('\'', "")
                    current_response += '\" '
                    count1 += 1
                except : 
                    await channel.send(current_response)
                    return
            count += 1
            current_response = current_response + "(" + str(count) + ")"
            await channel.send(current_response)           
            
 
 

bot.loop.create_task(send_prompts())
bot.run(TOKEN)

