import discord
from discord.ext import commands
from os import getenv, remove
# scripts
from image_utils import add_text_to_image

class Commands(commands.Cog):
	@commands.command()
	async def lol(self, ctx):
		img = discord.File(getenv("IMG_SUMMON"))
		await ctx.send(getenv("MENTION_LOL"), file=img)

	@commands.command()
	async def simon(self, ctx, *args):
	
		coords = (365, 1350)
		dims = (230, 125)
		
		text = " ".join(args)
		path = getenv("IMG_SIMON")
		out_path = path.split(".")[0] + ".del." + path.split(".")[1]

		await add_text_to_image(text, path, coords, dims, out_path)

		await ctx.send(text, file=discord.File(out_path))
		remove(out_path)