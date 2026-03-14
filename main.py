import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import sqlite3

# 環境変数の読み込み
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN or TOKEN == "YOUR_BOT_TOKEN_HERE":
    print("Error: DISCORD_TOKEN が設定されていません。 .env ファイルを確認してください。")
    exit(1)

# SQLiteデータベースの初期化
def init_db():
    conn = sqlite3.connect('bot_data.db')
    c = conn.cursor()
    # リマインド用テーブル
    c.execute('''CREATE TABLE IF NOT EXISTS reminders
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  channel_id INTEGER, 
                  user_id INTEGER, 
                  message TEXT, 
                  target_time REAL)''')
    # アンケート用テーブル
    c.execute('''CREATE TABLE IF NOT EXISTS polls
                 (message_id INTEGER PRIMARY KEY, 
                  channel_id INTEGER,
                  question TEXT, 
                  choices TEXT)''')
    # 匿名目安箱用テーブル (サーバーごとの転送先チャンネル設定)
    c.execute('''CREATE TABLE IF NOT EXISTS anonymous_config
                 (guild_id INTEGER PRIMARY KEY, 
                  target_channel_id INTEGER)''')
    # FAQ用テーブル
    c.execute('''CREATE TABLE IF NOT EXISTS faqs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  guild_id INTEGER, 
                  keyword TEXT, 
                  response TEXT)''')
    conn.commit()
    conn.close()

# Botの準備
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and not filename.startswith('__'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

@bot.event
async def setup_hook():
    init_db()
    await load_cogs()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')
    # スラッシュコマンドを同期する
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

# テスト用のPingコマンド
@bot.tree.command(name="ping", description="Botの応答速度をテストします")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! {round(bot.latency * 1000)}ms")

if __name__ == "__main__":
    bot.run(TOKEN)
