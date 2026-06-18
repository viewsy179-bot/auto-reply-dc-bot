import os
import random
from datetime import time
import discord
from discord.ext import commands, tasks
from zoneinfo import ZoneInfo
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

# Change this to your timezone, e.g. "Asia/Kathmandu", "America/New_York", "Europe/London"
TIMEZONE = ZoneInfo("Asia/Kathmandu")

MORNING_TIME = time(hour=7, minute=0, tzinfo=TIMEZONE)
NIGHT_TIME = time(hour=22, minute=0, tzinfo=TIMEZONE)

MORNING_MESSAGES = [
    "Good morning everyone! ☀️ Hope you have a great day ahead!",
    "Rise and shine! 🌅 Wishing you all an awesome day!",
    "Good morning! Let's make today count. 💪",
]

NIGHT_MESSAGES = [
    "Good night everyone! 🌙 Sleep well and sweet dreams!",
    "Time to rest. Good night and see you all tomorrow! ✨",
    "Good night! Take care and recharge for tomorrow. 😴",
]

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


@tasks.loop(time=MORNING_TIME)
async def morning_wish():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(random.choice(MORNING_MESSAGES))


@tasks.loop(time=NIGHT_TIME)
async def night_wish():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(random.choice(NIGHT_MESSAGES))


@morning_wish.before_loop
@night_wish.before_loop
async def before_loops():
    await bot.wait_until_ready()


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    if not morning_wish.is_running():
        morning_wish.start()
    if not night_wish.is_running():
        night_wish.start()


# Optional: manual test commands
@bot.command()
async def testmorning(ctx):
    await ctx.send(random.choice(MORNING_MESSAGES))


@bot.command()
async def testnight(ctx):
    await ctx.send(random.choice(NIGHT_MESSAGES))


bot.run(TOKEN)
