import random
import discord
from discord.ext import commands
from random import choice
# intents是要求機器人的權限
intents = discord.Intents.all()
# command_prefix是前綴符號，可以自由選擇($, #, &...)
bot = commands.Bot(command_prefix = "$", intents = intents)

@bot.event
# 當機器人完成啟動
async def on_ready():
    print(f"目前登入身份 --> {bot.user}")
    game = discord.Game('晴大師：世界征服')
    await bot.change_presence(status = discord.Status.online, activity = game)

food_list = ['麥當勞', '馬鈴薯']

@bot.command()
async def menu(ctx):
    embed = discord.Embed(title="簡介", description="機改馬鈴薯", color=0xfff2cb)
    embed.set_author(name="by maccaroni")
    embed.add_field(name="$add num1 num2", value="num1 + num2", inline=True)
    embed.add_field(name="$ping", value="就是ping", inline=True)
    embed.add_field(name="$上香", value="就是上香", inline=True)
    embed.add_field(name="$咩", value="咩", inline=True)
    embed.add_field(name="$貼圖", value="隨機貼圖", inline=True)
    embed.add_field(name="$吃什麼", value="抽一個吃", inline=True)
    embed.add_field(name="$有什麼能吃", value="列出清單", inline=True)
    embed.add_field(name="$好想吃 xx", value="加進隨機清單", inline=True)
    embed.add_field(name="$不想吃 xx", value="從隨機清單移除", inline=True)
    embed.set_footer(text="PotatoBot v3.0 last updated at 2024.03.31")
    await ctx.send(embed=embed)
@bot.command()
async def add(ctx, a: int, b: int):
    await ctx.send(a+b)
@bot.command()
async def ping(ctx):
    await ctx.send(f'{round(bot.latency*1000)}(ms)')
@bot.command()
async def 上香(ctx):
    await ctx.send("\\\|/")
@bot.command()
async def 超大上香(ctx):
    await ctx.send("# \\\|/")
@bot.command()
async def 咩(ctx):
    await ctx.send("咩")
@bot.command()
async def sticker_test(ctx):
    emoji = discord.utils.get(bot.emojis, name='MHRcat')
    await ctx.send(str(emoji))
@bot.command()
async def 貼圖(ctx):
    emoji_names = []
    for emoji in ctx.guild.emojis:
        emoji_names.append(emoji.name)
    print(len(emoji_names))
    emoji = discord.utils.get(bot.emojis, name=choice(emoji_names))
    await ctx.send(str(emoji))
@bot.command()
async def 吃什麼(ctx):
    if(len(food_list) == 0):
        await ctx.send("沒東西吃了 快想想")
    else:
        await ctx.send(choice(food_list))
@bot.command()
async def 有什麼能吃(ctx):
    await ctx.send("現在有"+str(len(food_list))+"個東西")
    await ctx.send(' '.join(food_list))
@bot.command()
async def 好想吃(ctx, food: str):
    if(food in food_list):
        await ctx.send("已經有了咩")
    else:
        food_list.append(food)
        await ctx.send("好的咩 已加上"+food+" 現在有"+str(len(food_list))+"個選擇")
@bot.command()
async def 不想吃(ctx, food: str):
    if (food in food_list):
        food_list.remove(food)
        await ctx.send("真的不吃嗎 好吧 移除"+food+"了咩 只剩下"+str(len(food_list))+"個選擇了哦")
    else:
        await ctx.send("本來就沒有咩")
TOKEN = "your_token" #記得改
bot.run(TOKEN)