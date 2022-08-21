from discord.ext import commands
from discord import Option
import discord, os

bot = discord.Bot(auto_sync_commands=True)

@bot.command(description="Help!")
async def help(ctx):
    await ctx.respond(f"Hi there, this is a simple bot that has (currently) a few moderation commands and some other fun stuff.\nCommands:\n/help: shows this page\n/ping: shows the bot\'s latency\n/kick: kicks a user\n/ban: bans a user", ephemeral=True)

@bot.command(description="Sends the bot's latency.")
async def ping(ctx):
    await ctx.respond(f"Pong! Latency is {bot.latency}")

@bot.command(description="Kicks a member")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: Option(discord.Member, "The member you want to kick"), reason:Option(str, "The reason to kick (will show in audit logs)")="No reason provided", silent:Option(bool,"Shows the message to other users (default is silent)")=True):
    r=f"{ctx.author.name}#{ctx.author.discriminator} kicked {member.name}#{member.discriminator} for: {reason}"
    await member.kick(reason=r)
    if silent:
        await ctx.respond(f"You kicked {member.name}#{member.discriminator} for: {reason}", ephemeral=True)
    else:
        await ctx.respond(r)

@bot.command(description="Bans a member")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: Option(discord.Member, "The member you want to ban"), reason:Option(str, "The reason to ban (will show in audit logs)")="No reason provided", silent:Option(bool,"Shows the message to other users (default is silent)")=True):
    r=f"{ctx.author.name}#{ctx.author.discriminator} yeeted the ban hammer on {member.name}#{member.discriminator} for: {reason}"
    await member.ban(reason=r)
    if silent:
        await ctx.respond(f"You banned {member.name}#{member.discriminator} for: {reason}", ephemeral=True)
    else:
        await ctx.respond(r)

bot.run(os.getenv("TOKEN"))
