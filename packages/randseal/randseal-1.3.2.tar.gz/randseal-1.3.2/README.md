# randseal
Simple package that produces a seal image. The image is then output as a `discord.File` for Pycord.

### Usage examples
```py
import randseal
import discord

bot = discord.Bot(intents=discord.Intents.default())

@bot.slash_command(description="Gets a random seal image")
async def sealimg(ctx):
	await ctx.respond(file=ranseal.file())

@bot.slash_command(description="Gets a random seal image")
async def sealembed(ctx):
	await ctx.respond(embed=ranseal.embed(title="Here is your seal!"))

bot.run("token")
```