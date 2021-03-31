import discord
from discord.ext import commands, tasks 
import datetime, random, asyncio 

bot = commands.Bot(command_prefix='?')
bot.promptlist = []
bot.hour = 6
bot.game = discord.Game("Driving Snooze Crazy")

@tasks.loop(seconds = 3600 )
async def send_prompts():
    await bot.wait_until_ready()
    rn = datetime.datetime.now()
    good_times = [0, 2, 4]
    if rn.hour == bot.hour and len(bot.promptlist) > 0 : 
        send_prompt()
    elif len(bot.promptlist) == 0 :
        channel = bot.get_channel(820804818045239367)
        await channel.send("**NO PROMPTS LEFT**")
    if rn.weekday in good_times and rn.hour == 18 :
        backup = bot.get_channel(818546231868391454)
        await back_up(ctx)
        
@bot.command(name = 'force_prompt') 
async def send_prompt(ctx) : 
        random_num = random.randint(0, len(bot.promptlist) - 1)
        channel = bot.get_channel(820804818045239367)
        output = bot.get_channel(816135387339685930)
        await output.send(bot.promptlist[random_num])
        del bot.promptlist[random_num]
        if len(bot.promptlist) <= 10 and len(bot.promptlist) != 1 : 
            await channel.send(f"**Warning!** Only **{len(bot.promptlist)}** prompts left!")
        elif len(bot.promptlist) == 1 : 
            await channel.send(f"**Strong Warning!** Only **1** prompt left!")
        elif len(bot.promptlist) == 0 : 
            await channel.send(f"**CRITICAL WARNING!** 0 prompts left!!")

def are_numbers(x) : 
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    return all(c in numbers for c in x)

@bot.command(name = 'set_hour')
async def set_hour(ctx, arg) :
    if 0 <= int(arg) and int(arg) <= 23 and are_numbers(arg) : 
        bot.hour = arg
        await ctx.send(f"Set output hour to {arg} CST!")
    elif are_numbers(arg) == False : 
        await ctx.send(f"**Error!** Use only numbers in hour setting, please!")
    else : 
        await ctx.send(f"**Out of range!** Use numbers 0 - 23, with 0 being midnight.")
        
@bot.command(name = 'set_status')
async def set_status(ctx, arg) : 
    bot.game = discord.Game(arg)
    await bot.change_presence(activity=bot.game)
    await ctx.send(f"Changed status to {arg}!")
        
@bot.command(name = 'set_prefix') 
async def set_prefix(ctx, arg) : 
    bot.command_prefix = arg                                
    await ctx.send(f"Prefix changed to {prefix}!")
                   
@bot.command(name = 'add')
async def add(ctx, prompt) :
    bot.promptlist.append(prompt) 
    response = "Added " + prompt + "!"
    await ctx.send(response)

@bot.command(name = 'remove_multiple') 
async def remove_multiple(ctx, *args) :
    
    for arg in args: 
        try :
            del bot.promptlist[int(arg)]
        except : 
            pass
    await ctx.send("Cleared requested prompts!")
    
@bot.command(name = 'clear_prompts')
async def clear_prompts(ctx) : 
    
    promplist = []
    await ctx.send("Cleared all prompts!")
    
@bot.command(name = 'prompt')
async def prompt(ctx, num) : 
    
    if num < len(bot.promptlist) : 
        response = f"Prompt {num}: {bot.promptlist[num]}"
    else : 
        response = f"{num} is out of range!"
    await ctx.send(response)
    
@bot.command(name='prompts')
async def prompts(ctx) :
    
    if len(bot.promptlist) == 0 : 
        await ctx.send("None!")
        return
    response = "**Prompts**: \n" + str(bot.promptlist).replace('[', '').replace(']', '')
    if False :
        pass
    else : 
        response_list = bot.promptlist
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
    if int(arg) <= len(bot.promptlist) -1 :
        removed_prompt = bot.promptlist[int(arg)]
        del bot.promptlist[int(arg)]
        response = "Removed " + removed_prompt + "!" 
        await ctx.send(response)
    else : 
        response = "Nothing at position " + arg + "!"
        await ctx.send(response)

@bot.command(name = 'load_prompts')
async def load_prompts(ctx, *args) : 
    
    for arg in args: 
        bot.promptlist.append(arg)    
    response = "Updated bot.promptlist to " + str(bot.promptlist) + "!"
    if len(response) <= 2000 :
        await ctx.send(response)
    else : 
        response = "I can't show you the whole list, but you can rest assured everything went well. Feel free to use ?prompts! :wink:"
        await ctx.send(response)
        
@bot.command(name = 'num_prompts')
async def num_prompts(ctx) :
    
    await ctx.send("There are " + str(len(bot.promptlist)) + " prompts!")
                  
           
@bot.command(name = 'back_up') 
async def back_up(ctx) : 
    channel = bot.get_channel(818546231868391454)
    
    if len(bot.promptlist) == 0 : 
        await channel.send("Nothing to back up!")
        return
    response = "**Backup**: \n" + str(bot.promptlist).replace('[', '').replace(']', '')
    if len(response) <= 1980 :
        await channel.send(response) 
    else : 
        response_list = bot.promptlist
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
            
send_prompts.start()
bot.run("ODIwNzg2NzI2NTA3MjQ5NzE1.YE6PNQ.eUPz98ua2cGzDW3RG29kecGN9iA")
 


