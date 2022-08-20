import discord, os

bot = discord.Bot(auto_sync_commands=True)

@bot.command(description="Sends the bot's latency.")
async def ping(ctx):
    await ctx.respond(f"Pong! Latency is {bot.latency}")

bot.run(os.getenv("TOKEN"))
