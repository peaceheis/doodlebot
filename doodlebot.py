import datetime
import random
import asyncio

import discord
from discord.ext import commands, tasks

bot = commands.Bot(command_prefix='?')

bot.hour = 7
bot.promptlist = []
bot.pause = False

DOODLES_ID: int = 811769854817337345


async def load_in_prompts():
    f = open("prompts.txt", "r")
    bot.promptlist = f.read().split("\n")
    del bot.promptlist[len(bot.promptlist) - 1]
    f.close()


@bot.command(name="save")
async def save_to_file(ctx):
    f = open("prompts.txt", "w")
    for prompt in bot.promptlist:
        f.write(prompt + "\n")
    await ctx.send("Saved!")


@tasks.loop(hours=1)
async def send_prompts() -> None:
    input_channel = await bot.fetch_channel(820804818045239367)
    rn = datetime.datetime.now()
    if rn.hour == bot.hour and bot.pause is False:
        await send_prompt()


@send_prompts.before_loop
async def before():
    await bot.wait_until_ready()
    await load_in_prompts()


@bot.command(name='pause')
async def pause(ctx):
    bot.pause = True
    await ctx.send("Paused prompt sending!")


@bot.command(name='unpause')
async def unpause(ctx):
    bot.pause = False
    await ctx.send("Resumed prompt sending!")


@bot.command(name='pause_status')
async def status_of_pause(ctx):
    if bot.pause:
        string = "paused"
    else:
        string = "unpaused"
    await ctx.send(f"The prompt sending loop is currently {string}!")


@bot.command(name='force_prompt')
async def force_prompt(ctx):
    await send_prompt(ctx)


async def send_prompt(ctx=None):
    input_channel = await bot.fetch_channel(820804818045239367)
    prompt_channel = await bot.fetch_channel(816135387339685930)
    try:
        random_num = random.randint(0, len(bot.promptlist) - 1)
        await prompt_channel.send(bot.promptlist[random_num])
        del bot.promptlist[random_num]
    except ValueError:
        await input_channel.send("No prompts left! How you let it get this bad, I don't know. :person_shrugging:")
        return
    return


def are_numbers(x):
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    return all(c in numbers for c in x)


@bot.command(name='set_hour')
async def set_hour(ctx, arg):
    if not are_numbers(arg):
        await ctx.send(f"**Error!** Use only numbers in hour setting, please!")
    elif int(arg) > 23 or int(arg) < 0:
        await ctx.send(f"**Out of range!** Use numbers 0 - 23, with 0 being midnight.")
    elif 0 <= int(arg) <= 23 and are_numbers(arg):
        bot.hour = arg
        await ctx.send(f"Set output hour to {arg} CST!")


@bot.command(name='set_status')
async def set_status(ctx, arg):
    bot.game = discord.Game(arg)
    await bot.change_presence(activity=bot.game)
    await ctx.send(f"Changed status to {arg}!")


@bot.command(name='force')
async def force(ctx, arg):
    prompt_channel = await bot.fetch_channel(816135387339685930)
    if bot.promptlist[arg] is not None:
        await prompt_channel.send(bot.promptlist[arg])
    else:
        await ctx.send("That is not in the promptlist!")


@bot.command(name='set_prefix')
async def set_prefix(ctx, arg):
    bot.command_prefix = arg
    await ctx.send(f"Prefix changed to {arg}!")


@bot.command(name='add')
async def add(ctx, prompt):
    bot.promptlist.append(prompt)
    response = "Added " + prompt + "!"
    await ctx.send(response)


@bot.command(name='remove_multiple')
async def remove_multiple(ctx, *args):
    for arg in args:
        try:
            del bot.promptlist[int(arg)]
        except:
            pass
    await ctx.send("Cleared requested prompts!")


@bot.command(name='clear_prompts')
async def clear_prompts(ctx):
    bot.promptlist = []
    await ctx.send("Cleared all prompts!")


@bot.command(name='prompt')
async def prompt(ctx, num):
    if num < len(bot.promptlist):
        response = f"Prompt {num}: {bot.promptlist[num]}"
    else:
        response = f"{num} is out of range!"
    await ctx.send(response)


@bot.command(name='prompts')
async def prompts(ctx):
    if len(bot.promptlist) == 0:
        await ctx.send("None!")
        return
    response = "**Prompts**: \n" + str(bot.promptlist).replace('[', '').replace(']', '')
    if False:
        pass
    else:
        response_list = bot.promptlist
        current_char = 0
        count = 0
        count1 = 0
        should_continue = True
        while should_continue:
            current_response = ""
            for i in range(25):
                try:
                    current_response += str(count1) + ": "
                    current_response += response_list[count1].replace('\'', "")
                    current_response += " "
                    count1 += 1
                except:
                    await ctx.send(current_response)
                    return
            count += 1
            current_response = current_response + "(" + str(count) + ")"
            await ctx.send(current_response)


@bot.command(name='remove')
async def remove(ctx, arg):
    if int(arg) <= len(bot.promptlist) - 1:
        removed_prompt = bot.promptlist[int(arg)]
        del bot.promptlist[int(arg)]
        response = "Removed " + removed_prompt + "!"
        await ctx.send(response)
    else:
        response = "Nothing at position " + arg + "!"
        await ctx.send(response)


@bot.command(name='load_prompts')
async def load_prompts(ctx, *args):
    for arg in args:
        bot.promptlist.append(arg)
    response = "Updated bot.promptlist to " + str(bot.promptlist) + "!"
    if len(response) <= 2000:
        await ctx.send(response)
    else:
        response = "I can't show you the whole list, but you can rest assured everything went well. Feel free to use " \
                   "?prompts! :wink: "
        await ctx.send(response)


@bot.command(name='back_up')
async def back_up(ctx):
    channel = await bot.fetch_channel(818546231868391454)

    if len(bot.promptlist) == 0:
        await channel.send("Nothing to back up!")
        return
    response = "**Backup**: \n" + str(bot.promptlist).replace('[', '').replace(']', '')
    if len(response) <= 1980:
        await channel.send(response)
    else:
        response_list = bot.promptlist
        current_char = 0
        count = 0
        count1 = 0
        should_continue = True
        while should_continue:
            current_response = ""
            for i in range(25):
                try:
                    current_response += '\"'
                    current_response += response_list[count1].replace('\'', "")
                    current_response += '\" '
                    count1 += 1
                except:
                    await channel.send(current_response)
                    return
            count += 1
            current_response = current_response + "(" + str(count) + ")"
            await channel.send(current_response)


@bot.command(name='num_prompts')
async def num_prompts(ctx):
    await ctx.send("There are " + str(len(bot.promptlist)) + " prompts!")


@bot.group()
async def say(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("Invalid subcommand passed.")


@say.command(name="by_channel", aliases=["in_channel", "in"])
async def by_channel(ctx, channel: discord.TextChannel, *, message):
    await (await bot.fetch_channel(channel.id)).send(message)


@say.command(name="inc")
async def in_channel(ctx, channel_name: str, *, message: str):
    channel_id = 0
    match channel_name:
        case "introductions-optional":
            channel_id = 811773988254384149
        case "ask-a-mod":
            channel_id = 816424705560674356
        case "general":
            channel_id = 811769855246204950

        case "memes":
            channel_id = 811776900484956181
        case "the-love-of-pets":
            channel_id = 811804039699234887
        case "daily-doodle-prompt":
            channel_id = 816135387339685930
        case "art-hobby-lobby":
            channel_id = 816174920010039296
        case "shareable-content":
            channel_id = 817265697394393088
        case "food":
            channel_id = 816181542036176927
        case "storytime-restaurant":
            channel_id = 816204766005952513
        case "events-and-self-promos":
            channel_id = 816193452937052190
        case "wip-help-2d":
            channel_id = 811809216716603392
        case "critique-this-2d":
            channel_id = 811809333267791872
        case "awesome-2d-artists":
            channel_id = 811810102897016863
        case "tutorials-and-references-2d":
            channel_id = 816145719601397770
        case "nsfw-work-2d":
            channel_id = 816145719601397770
        case "wip-help-3d":
            channel_id = 816145433893404733
        case "critique-this-3d":
            channel_id = 816145550373421057
        case "awesome-3d-artists":
            channel_id = 816145599656099902
        case "tutorials-and-references-3d":
            channel_id = 816146146035630080
        case "nfsw-work-3d":
            channel_id = 816800059688484885
        case "wip-help-4d":
            channel_id = 816134695787298876
        case "critique-this-4d":
            channel_id = 816141849546063902
        case "awesome-4d-artists":
            channel_id = 816142051217113138
        case "nsfw-work-4d":
            channel_id = 816800178823757884
        case "battle-ground":
            channel_id = 835963086036533268
        case "karaoke-night":
            channel_id = 825846039520346142
        case "muted-in-vc":
            channel_id = 811810399502073857
        case "using-mono":
            channel_id = 819418277855100948
        case "using-cmyk":
            channel_id = 821202757171675176
        case "cmyk-levels":
            channel_id = 818288491280203806
        case "z-fight-arena":
            channel_id = 819423449922666527
    try:
        channel = await bot.fetch_channel(channel_id)
    except (discord.NotFound, discord.InvalidData):
        await ctx.send("improper channel!")


send_prompts.start()
bot.run("")
