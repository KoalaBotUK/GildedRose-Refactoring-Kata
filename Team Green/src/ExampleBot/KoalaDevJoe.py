import os
import sqlite3
from dotenv import load_dotenv
import discord
import random
from discord.ext import commands

from DatabaseManager import DatabaseManager
from TwitterTools import TwitterTools

bot = commands.Bot(command_prefix='kJ!')

load_dotenv()
TOKEN = os.getenv("TOKEN")
TWITTER_TOKEN = os.getenv("TWITTER_TOKEN")
TWITTER_KEY = os.getenv("TWITTER_KEY")
TWITTER_SECRET = os.getenv("TWITTER_SECRET")

DBManager = DatabaseManager()
TwitterTools = TwitterTools(TWITTER_TOKEN, TWITTER_KEY, TWITTER_SECRET)

@bot.event
async def on_ready():
  print(f"Bot user {bot.user} is ready.")

@bot.command()
async def ping(ctx):
  """
  Provides the user with the latency of the bot in [ms].
  """
  if ctx.author == bot.user:
    return
  await ctx.send(f"Pong! ({bot.latency():.3f}ms)")

@bot.command()
async def choose(ctx, *args):
  if ctx.author == bot.user:
    return
  await ctx.send(random.choice(args))

@bot.command()
async def clear(ctx, num: int):
  if ctx.author == bot.user:
    return
  await ctx.channel.purge(limit=num+1)

@bot.command()
async def greet(ctx, user):
  if ctx.author == bot.user:
    return
  if user == None:
    user = ctx.author
  await ctx.send(f"Welcome to the server {user}! Have a great time while you're here!")

@bot.command()
async def thanks(ctx):
  if ctx.author == bot.user:
    return
  await ctx.send("No problem!")

# DATABASE COMMANDS

@bot.command()
async def get_item_amount(ctx, item_name):
  """Bot command that lets a user retrieve the amount of a certain item
  :param ctx: message context
  :param item_name: Name of the item to get
  :return:
  """
  if item_name in DBManager.get_item_names():
    item_amount = DBManager.get_item_amount(item_name)
    await ctx.send(item_amount)
  else:
    await ctx.send("That item doesn't exist")

@bot.command(name="add")
async def add_item(ctx, item_name, description, amount: int):
  """Bot command that lets a user add an item to the database
  :param ctx: message context
  :param item_name: Name of the item to add
  :param description: A brief description of the item
  :param amount: Total amount of the item
  :return:
  """
  if item_name not in DBManager.get_item_names():
    DBManager.add_item(item_name, description, amount)
    await ctx.send(f"{item_name} successfully added!")
  else:
    await ctx.send(f"That item has already been added!")

@bot.command(name="take")
async def take_item(ctx, item_name: str, amount=1):
  """Bot command that lets a user take an amount of an item
  :param ctx: message context
  :param item_name: Name of the item to take
  :param amount: Amount of items being taken
  :return:
  """
  if item_name in DBManager.get_item_names():
    stock = int(DBManager.get_item_amount(item_name))
    if amount <= stock:
      user = ctx.author.id
      DBManager.add_item_take_record(item_name,amount,user)
      new_amount = stock - amount
      DBManager.update_item_amount(item_name, new_amount)
      await ctx.send(f'Successfully took {amount} of {item_name}')
    else:
      await ctx.send(f'Cannot take {amount} {item_name}, only {stock} in stock')
  else:
    await ctx.send(f'Cannot find item {item_name}')

@bot.command()
async def return_item(ctx, item_name, amount=1):
  # Delete record in Transactions, add amount back to Items:ItemAmount
  pass

@bot.command(name="list")
async def list_items(ctx):
  """Bot command that lists all the items in the database
  :return:
  """
  embed=discord.Embed(color=0xff00ff, title="Item list")
  items = DBManager.get_item_names()
  for item in items:
    embed.add_field(name=item, value=str(DBManager.get_item_amount(item)), inline=False)
  await ctx.send(embed=embed)

@bot.command(name="search")
async def search_items(ctx, item_name: str):
  """Bot command that gives a more detailed description of an item in the database
  :param item_name: Name of the item to search for
  :return:
  """
  if item_name in DBManager.get_item_names():
    stock = int(DBManager.get_item_amount(item_name))
    embed=discord.Embed(color=0xff00ff, title="Item Lookup")
    embed.add_field(
      name=item_name,
      value=f"Description: {DBManager.get_item_description(item_name)}\n Quantity: {DBManager.get_item_amount(item_name)}",
      inline=False
    )
    await ctx.send(embed=embed)
  else:
    await ctx.send("Item doesn't exist! Try `kJ!list` to find the item.")

@bot.command(name="createDB")
async def createDB(ctx, *args):
  """Bot command that inputs data using a .csv file as an attachment
  :return:
  """
  if str(ctx.message.attachments) == "[]":
    await ctx.send("There this no attachment attached to this command")
  else:
    filename= str(ctx.message.attachments).split("filename='")[1]
    filename= str(filename).split("' ")[0]
    if filename.endswith(".csv"):
      await ctx.send("ends with csv")
    else: 
      await ctx.send("not a csv")

# Twitter API

@bot.command(name="getid")
async def get_twitter_userid(ctx, name: str):
  """Command that sends the id of a twitter username
  :param name: username to fetch twitter id of
  :return:
  """
  await ctx.send(str(TwitterTools.get_twitter_id(name)))
  
@bot.command(name="recent")
async def get_twitter_recent_tweet(ctx, name: str):
  """Command that sends the most recent tweet of a twitter username
  :param name: username to fetch twitter id of
  :return:
  """
  # try:
  json = TwitterTools.get_recent_tweet(name)
  embed=discord.Embed(color=0xff00ff)
  embed.set_author(name=name,icon_url=str(TwitterTools.get_profile_image(name)))
  embed.add_field(name=f'https://twitter.com/twitter/status/{json["id_str"]}',value=str(json["full_text"]))
  embed.set_footer(text=f'Tweeted on: {json["created_at"]}')
  await ctx.send(embed=embed)
  # except LookupError as e:
  #   print(e)


@bot.command(name="profilepic")
async def get_profile_pic(ctx, name: str):
  """Semds the profile picture of the given twitter
  :param name: username of the twitter user
  :return:"""
  await ctx.send(TwitterTools.get_profile_image(name))


@bot.command(name="post")
async def post_new_status(ctx, *, text):
  request = TwitterTools.post_new_status(text)
  if request.status_code > 399:
    await ctx.send("Failed to post tweet!")
  else:
    await ctx.send("Posted!")

if __name__ == "__main__":
  bot.run(TOKEN)