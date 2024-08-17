import discord
from discord.ext import commands, tasks
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from datetime import datetime
import os

# 設置 Discord 機器人
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='$', intents=intents)

# 設置 ChromeDriver 路徑
CHROMEDRIVER_PATH = 'your_path'  # 更新為你的 chromedriver 路徑

# 搜尋當天的文章並返回結果，僅限標題中包含 "line" 或 "LP" 的文章
def find_articles_on_date(target_date):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 在背景運行
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    url = 'https://www.ptt.cc/bbs/Lifeismoney/index.html'
    driver.get(url)
    
    output = ''
    
    try:
        # 等待頁面加載完成，等待標題元素出現
        WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.title a')))
        
        # 獲取當前頁面上的所有文章
        titles = driver.find_elements(By.CSS_SELECTOR, 'div.title a')
        
        found = False
        for title in titles:
            try:
                # 確保找到的元素能夠被正確處理
                parent_element = title.find_element(By.XPATH, '../..')  # 調整選擇器到正確層級
                article_date = parent_element.find_element(By.CSS_SELECTOR, 'div.date').text.strip()
                
                # 篩選包含 "line" 或 "LP" 且日期為今天的文章
                if article_date == target_date and ('line' in title.text.lower() or 'lp' in title.text.lower()):
                    output += f"{title.text}\n"
                    output += f"https://www.ptt.cc{title.get_attribute('href')}\n\n"
                    found = True

            except NoSuchElementException as e:
                print(f"Error finding date element: {e}")
        
    except TimeoutException as e:
        print(f"Timeout while waiting for elements: {e}")
    except Exception as e:
        print(f"General error: {e}")
    finally:
        driver.quit()
    
    return output

# 每天定時抓取並發布文章
@tasks.loop(hours=8)
async def daily_article_task():
    channel = bot.get_channel(YOUR_CHANNEL_ID)  # 用你的頻道ID替換
    today = datetime.now()
    #now_str = today.strftime("%m/%d").lstrip('0')  # 移除月份中的前導0
    now_str = '8/16'
    print(f"今天是{now_str}\n")
    results = find_articles_on_date(now_str)
    
    if results:
        await channel.send(f"這是今天 ({now_str}) 含有 'line' 或 'LP' 的文章：\n{results}")
    else:
        await channel.send(f"今天 ({now_str}) 沒有找到含有 'line' 或 'LP' 的相關文章。")

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
    #now_str = today.strftime("%m/%d").lstrip('0')
    now_str = '8/16'
    print(f"今天是{now_str}\n")
    results = find_articles_on_date(now_str)
    
    if results:
        await ctx.send(f"這是今天 ({now_str}) 含有 'line' 或 'LP' 的文章：\n{results}")
    else:
        await ctx.send(f"今天 ({now_str}) 沒有找到含有 'line' 或 'LP' 的相關文章。")

# 設置機器人 token
TOKEN = 'your_token'  # 用你的 Discord 機器人 token 替換
YOUR_CHANNEL_ID = 'your_id'  # 用你的頻道ID替換

bot.run(TOKEN)
