import discord
import os
#import pynacl
#import dnspython
import server
from discord.ext import commands
from replit import db


intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="==")
TOKEN = os.getenv("DISCORD_TOKEN")

def lvl_up(author_id):
    cur_xp = db[author_id]["exp"]
    cur_lvl = db[author_id]["lvl"]

    if cur_lvl < 15:
      if cur_xp > 80 * (cur_lvl + 1):
        db[author_id]["lvl"] += 1
        return True
      else:
        return False
    else:
      if cur_xp >= 1200 * (cur_lvl - 14):
        db[author_id]["lvl"] += 1
        return True
      else:
        return False


@bot.event
async def on_ready():
  print("We have logged in as {0.user}".format(bot))


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.author.bot == False:
        author_id = str(message.author.id)

        if not author_id in db.keys():
            db[author_id] = {"exp": 0, "lvl": 0}

        #addig exp system  
        msg = len(message.content)
        if msg > 3600:
            db[author_id]["exp"] += 25
        elif msg > 3000:
            db[author_id]["exp"] += 20
        elif msg > 1700:
            db[author_id]["exp"] += 12
        elif msg > 1000:
            db[author_id]["exp"] += 10
        elif msg > 100:
            db[author_id]["exp"] += 2

        if lvl_up(author_id):
            channel_lvl = bot.get_channel(909465395784736779)
            await channel_lvl.send(f"No genialny jesteś {message.author.mention}, osiągnąłeś {db[author_id]['lvl']} level, Ty kreatywna bestio! Oby tak dalej, a dostaniesz wspaniałe nagrody!")
    await bot.process_commands(message)
          

#showing level
@bot.command(pass_context=True)
async def lvl(ctx, member: discord.Member = None):
    member = ctx.author if not member else member
    member_id = str(member.id)
    if not member_id in db.keys():
            db[member_id] = {"exp": 0, "lvl": 0}
    else:
      embed = discord.Embed(
                    title = ' ',
                    description = f"{member}",
                    colour = 0xb180f9
                  )
      embed.add_field(name="Poziom kreatywności:", value=db[member_id]["lvl"])
      embed.add_field(name="Exp:", value=db[member_id]["exp"])
      await ctx.send(embed=embed)


#manually addig exp
@bot.command(pass_context=True)
async def addxp(ctx, xp, member: discord.Member = None):
    member = ctx.author if not member else member
    member_id = str(member.id)

    if not member_id in db.keys():
        await ctx.send(f"Użytkownika nie ma tym serwerze.")
    else:
        db[member_id]["exp"] += int(xp)
        await ctx.send(f"Użytkowik {member} dostał {xp} punktów kreatywności!")


#manually subtracting ep
@bot.command(pass_context=True)
async def subxp(ctx, xp, member: discord.Member = None):
    member = ctx.author if not member else member
    member_id = str(member.id)

    if not member_id in db.keys():
        await ctx.send(f"Użytkownika nie ma tym serwerze.")
    else:
        db[member_id]["exp"] -= int(xp)
        await ctx.send(f"Użytkowik {member} utracił {xp} punktów kreatywności!")


server.server()
bot.run(TOKEN)
