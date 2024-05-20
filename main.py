import discord
import os
import requests
import json
import random
from discord.ext import commands
from replit import db
import numpy as np
import pandas as pd
from keep_alive import keep_alive

client = discord.Client()

bot = commands.Bot(command_prefix='$')

global shingWaiPoints
shingWaiPoints = 0


@client.event
async def on_ready():
  print("Chun Yin point system running.")


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('$help'):
    await message.channel.send(
        'Commands:.\n$add = register yourself as member.\n$check = check your chunyin points.\n$leaderboards = check chunyin points leaderboards.\n$shop = Check shop.\n$buy = buy off shop.\n$give = give others chunyin points'
    )

  @client.event
  async def on_reaction_add(reaction, user):
    if (user.id == 133910998607200256
        and reaction.emoji.id == 853303973460967424):
      df = pd.read_csv('userInfo.csv', index_col=[0])
      row = df[df['name'] == reaction.message.author.name].index[0]
      iniVal = float(df.iloc[row]['points'])
      finalVal = iniVal + 1
      df.at[row, 'points'] = finalVal
      df.to_csv('userInfo.csv', )
      await message.channel.send("1 point added to " +
                                 reaction.message.author.name)
    else:
      return

  if message.content.startswith('$add'):
    temp_dict = {'name': message.author.name, 'points': 0}
    try:
      df = pd.read_csv('userInfo.csv', index_col=[0])
      if ((df['name'] == message.author.name).any() == True):
        await message.channel.send('Already in the Database')
      else:
        df = df.append(temp_dict, ignore_index=True)
        await message.channel.send('Added to Database')
      df.to_csv('userInfo.csv')

    except:
      df = pd.DataFrame([temp_dict])
      df = df[['name', 'points']]
      df.to_csv('userInfo.csv')
      await message.channel.send('Added to Database')

  if message.content.startswith('$check'):
    df = pd.read_csv('userInfo.csv', index_col=[0])
    row = df[df['name'] == message.author.name].index[0]
    await message.channel.send(
        f"{df.iloc[row]['name']}, you have {df.iloc[row]['points']} points")

  if message.content.startswith('$leaderboard'):
    df = pd.read_csv('userInfo.csv', index_col=0)
    df = df.sort_values('points', ascending=False)
    users = df['name'].to_string(index=False)
    points = df['points'].to_string(index=False)
    embed = discord.Embed(title="Leaderboard")
    embed.add_field(name="Name", value=users)
    embed.add_field(name="Points", value=points)
    await message.channel.send(embed=embed)

  if message.content.startswith('$give'):
    if message.author.name == 'Chunyink':
      content = message.content
      contentArray = content.split(" ")
      if (len(contentArray) > 3):
        contentArray[1:-1] = [' '.join(contentArray[1:-1])]
        print(contentArray)
      if (len(contentArray) == 3):
        print(contentArray)
        userName = contentArray[1]
        pointsGiven = float(contentArray[2])
        df = pd.read_csv('userInfo.csv', index_col=[0])
        if userName in df.values:
          row = df[df['name'] == userName].index[0]
          iniVal = int(df.iloc[row]['points'])
          finalVal = iniVal + pointsGiven
          df.at[row, 'points'] = finalVal
          df.to_csv('userInfo.csv', )
          await message.channel.send(
              f"{pointsGiven} points added to {userName}")
        else:
          await message.channel.send(f"{userName} not found")
          return
      else:
        await message.channel.send("Format is: $give USERNAME #POINTS")
        return
    else:
      return

  if message.content.startswith('$shop'):
    await message.channel.send('It does not work yet')

  if message.content.startswith('$buy'):
    await message.channel.send('It does not work yet')


keep_alive()

