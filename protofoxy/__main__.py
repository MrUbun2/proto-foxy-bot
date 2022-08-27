#! /usr/bin/env python3.9
from discord.ext import commands
from discord import Option
import subprocess, discord, asyncio, sys, os

TIMES = [30,20,15,10,3,2,1,0]
RESTART = False
bot = discord.Bot(auto_sync_commands=True)

class TTT(discord.ui.View):
    def __init__(self, p):
        super().__init__(timeout=60)
        self.t=False
        self.p=p
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
    async def check(self):
        c=[]
        for child in self.children:
            c.append(child.label)
        g=[
            [1,1,1,0,0,0,0,0,0],
            [0,0,0,1,1,1,0,0,0],
            [0,0,0,0,0,0,1,1,1],
            [1,0,0,1,0,0,1,0,0],
            [0,1,0,0,1,0,0,1,0],
            [0,0,1,0,0,1,0,0,1],
            [1,0,0,0,1,0,0,0,1],
            [0,0,1,0,1,0,1,0,0]
        ]
        for l in ["X","O"]:
            for w in g:
                t=0
                b=0
                for i,a in enumerate(w):
                    if a==1:
                        t+=1
                        if c[i]==l:
                            b+=1
                if t==b:
                    return l
        return False
    async def m(self, button, interaction):
        if interaction.user == self.p[self.t]:
            self.t=not self.t
            button.disabled=True
            button.style=[discord.ButtonStyle.green,discord.ButtonStyle.red][self.t]
            button.label=["X","O"][self.t]
            b=await self.check()
            if b:
                for child in self.children:
                    child.disabled=True
                if b=="X":
                    w=self.p[1]
                else:
                    w=self.p[0]
                await interaction.response.edit_message(content=f"<@{w.id}> won!", view=self)
            else:
                await interaction.response.edit_message(view=self)
        else:
            await interaction.response.send_message("It's not your turn!", ephemeral=True)

    @discord.ui.button(label="\u200b", row=0, style=discord.ButtonStyle.gray)
    async def a(self, button, interaction): await self.m(button, interaction)
    @discord.ui.button(label="\u200b", row=0, style=discord.ButtonStyle.gray)
    async def b(self, button, interaction): await self.m(button, interaction)
    @discord.ui.button(label="\u200b", row=0, style=discord.ButtonStyle.gray)
    async def c(self, button, interaction): await self.m(button, interaction)

    @discord.ui.button(label="\u200b", row=1, style=discord.ButtonStyle.gray)
    async def d(self, button, interaction): await self.m(button, interaction)
    @discord.ui.button(label="\u200b", row=1, style=discord.ButtonStyle.gray)
    async def e(self, button, interaction): await self.m(button, interaction)
    @discord.ui.button(label="\u200b", row=1, style=discord.ButtonStyle.gray)
    async def f(self, button, interaction): await self.m(button, interaction)

    @discord.ui.button(label="\u200b", row=2, style=discord.ButtonStyle.gray)
    async def g(self, button, interaction): await self.m(button, interaction)
    @discord.ui.button(label="\u200b", row=2, style=discord.ButtonStyle.gray)
    async def h(self, button, interaction): await self.m(button, interaction)
    @discord.ui.button(label="\u200b", row=2, style=discord.ButtonStyle.gray)
    async def i(self, button, interaction): await self.m(button, interaction)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command(description="Help!")
async def help(ctx):
    await ctx.respond(f"Hi there, this is a simple bot that has (currently) a few moderation commands and some other fun stuff.\nCommands:\n/help: shows this page\n/ping: shows the bot\'s latency\n/tictactoe: tic tac toe\n/kick: kicks a user\n/ban: bans a user", ephemeral=True)

@bot.command(description="Sends the bot's latency.")
async def ping(ctx):
    await ctx.respond(f"Pong! Latency is {bot.latency}")

@bot.user_command(name="Tic Tac Toe")
@bot.command(description="Simple Tic Tac Toe game")
async def tictactoe(ctx, member: Option(discord.Member, "The member you want to play against")):
    await ctx.respond(f"<@{ctx.author.id}> vs <@{member.id}> tic tac toe", view=TTT([ctx.author,member]))

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

@bot.command(description="Shuts down the bot")
@commands.is_owner()
async def shutdown(ctx):
    await ctx.respond("bot is shutting down aahhhhh")
    print("--- SHUTDOWN INITIATED ---")
    for k, i in enumerate(TIMES):
        await bot.change_presence(status=discord.Status.dnd,activity=discord.Activity(type=3, name=f"shutting down in {i}"))
        print(i)
        if i!=0: await asyncio.sleep(TIMES[k]-TIMES[k+1])
    print("--- SHUTDOWN COMPLETE ---")
    await bot.close()

@bot.command(description="Restarts down the bot")
@commands.is_owner()
async def restart(ctx):
    global RESTART
    await ctx.respond("bot is restarting aahhhhh")
    RESTART = True
    print("--- RESTART INITIATED ---")
    for k, i in enumerate(TIMES):
        await bot.change_presence(status=discord.Status.dnd,activity=discord.Activity(type=3, name=f"restarting in {i}"))
        print(i)
        if i!=0: await asyncio.sleep(TIMES[k]-TIMES[k+1])
    print("--- RESTART COMPLETE ---")
    await bot.close()

@bot.command(description="Git pull command")
@commands.is_owner()
async def gitpull(ctx):
    p=subprocess.Popen(['git','pull'], stdout=subprocess.PIPE)
    o=p.stdout.read().decode('ascii')
    await ctx.respond(o)

if __name__ == "__main__":
    bot.run(os.getenv("TOKEN"))
    print(RESTART)
    if RESTART:
        print('resrar')
        os.execv(__file__, sys.argv)
