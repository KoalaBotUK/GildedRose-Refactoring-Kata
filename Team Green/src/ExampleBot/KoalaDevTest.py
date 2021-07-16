# Imports
import pytest
import discord
import discord.ext.test as dpytest
from discord.ext import commands
import random
import mock

#Custom Imports
import KoalaDevJoe

BOT_PREFIX = "kJ!"
FAKE_USER = "fakeUser#0000"
CHOICES = ["bus", "car", "train", "bike", "20", "<>", "//£&^:@)", "24562754"]

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.messages = True

@pytest.fixture(autouse=True)
def bot(event_loop):
  bot = commands.Bot(BOT_PREFIX, intents=intents)
  for com in KoalaDevJoe.bot.commands:
    if com.name != "help":
      bot.add_command(com)
  dpytest.configure(bot)
  print("Starting bot tests")
  return bot

@mock.patch("discord.client.Client.latency", mock.MagicMock(return_value=float(1)))
@pytest.mark.asyncio
async def test_ping(bot):
  m = await dpytest.message(BOT_PREFIX + "ping")
  assert dpytest.verify().message().content(f"Pong! ({float(1):.3f}ms)")

@pytest.mark.asyncio
async def test_greet(bot):
  await dpytest.message(BOT_PREFIX + "greet " + FAKE_USER)
  assert dpytest.verify().message().content(f"Welcome to the server {FAKE_USER}! Have a great time while you're here!")

@pytest.mark.asyncio
async def test_choose(bot):
  choice = random.choice(CHOICES)
  await dpytest.message(BOT_PREFIX + "choose " + choice)
  assert dpytest.verify().message().content(choice)

@pytest.mark.asyncio
async def test_clear(bot):
  with mock.patch.object(discord.channel.TextChannel, "purge") as mock1:
    await dpytest.message(BOT_PREFIX + "clear 4")
    mock1.assert_called_with(limit=4)