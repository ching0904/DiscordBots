import discord
from discord.ext import commands, tasks
import requests
from requests import get
from bs4 import BeautifulSoup
from datetime import datetime
import os
# import keep_alive
# 設置 Discord 機器人
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='$', intents=intents)


# 搜尋當天的文章並返回結果，僅限標題中包含 "line" 或 "LP" 的文章
def find_articles_on_date(target_date):
    url = 'https://www.ptt.cc/'
    web = requests.get('https://www.ptt.cc/bbs/Lifeismoney/index.html')
    web.encoding='utf-8'       # 避免中文亂碼
    soup = BeautifulSoup(web.text, "html.parser")
    titles = soup.find_all('div', class_='title')
    output = ''           # 建立 output 變數

    try:
        found = False
        for i in titles:
            if i.find('a') is not None:
                title_text = i.find('a').get_text()
                link = url + i.find('a')['href']
                if ('line' in title_text.lower() and 'point' in title_text.lower()) or 'lp' in title_text.lower():  # 搜索標題中包含 "line" 或 "lp" 的文章 不分大小寫
                    output += title_text + '\n' + link + '\n'
                    found = True
        # print(output)
    except:
        print(f"General error: {e}")

    return output

# 每天定時抓取並發布文章
@tasks.loop(hours=8)
async def daily_article_task():
    channel = bot.get_channel(int(YOUR_CHANNEL_ID))  # 用你的頻道ID替換
    today = datetime.now()
    now_str = today.strftime("%m/%d").lstrip('0')  # 移除月份中的前導0
    print(f"今天是{now_str}\n")
    results = find_articles_on_date(now_str)

    if results:
        await channel.send(f"這是今天 ({now_str}) 的文章：\n{results}")
    else:
        await channel.send(f"今天 ({now_str}) 沒有找到相關文章:(")

@bot.event
# 當機器人完成啟動
async def on_ready():
    print(f"目前登入身份 --> {bot.user}")
    game = discord.Game('爬省錢板')
    await bot.change_presence(status=discord.Status.online, activity=game)
    daily_article_task.start()  # 啟動定時任務

# 手動觸發抓取指令
@bot.command()
async def points(ctx):
    today = datetime.now()
    now_str = today.strftime("%m/%d").lstrip('0')
    print(f"今天是{now_str}\n")
    results = find_articles_on_date(now_str)

    if results:
        await ctx.send(f"這是今天 ({now_str}) 含有 'line' 或 'LP' 的文章：\n{results}")
    else:
        await ctx.send(f"今天 ({now_str}) 沒有找到含有 'line' 或 'LP' 的相關文章。")

# 設置機器人 token
TOKEN = os.environ['TOKEN'] # 用你的 Discord 機器人 token 替換
YOUR_CHANNEL_ID = os.environ['CHANNEL_ID'] # 用你的頻道ID替換
#keep_alive.keep_alive()
bot.run(TOKEN)
