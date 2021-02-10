import discord
from discord.ext import commands
from os import getenv, remove
import log.logger as log
# scripts
from cogs.__command_utils import add_text_to_image


def setup(bot):
	log.warn(f"Loading extension: {__name__}")

	bot.add_cog(MemeCommands())
	log.notice("Loaded cog: MemeCommands",1)
	bot.add_cog(Commands())
	log.notice("Loaded cog: Commands",1)

	log.confirm(f"Loaded extension: {__name__}")

def teardown(bot):
	log.warn(f"Unloading extension: {__name__}")

	log.notice("Unloaded cog: MemeCommands",1)
	log.notice("Unloaded cog: Commands",1)
	
	log.confirm(f"Unloaded extension: {__name__}")


class Commands(commands.Cog):
	def __init__(self):
		pass

	# command to delete a specified number of commands in a text channel
	@commands.command(
		name='bulkdelete',
		aliases=['bulk_delete', 'bdel'],
		help="""
		Borra x mensajes en el canal en el que se escribe el comando.
		Solo puede utilizarse por admins.
		IMPORTANTE: El mensaje del comando no se cuenta en el numero de mensajes
		"""
	)
	@commands.has_role('admin')
	async def bulk_delete(self, ctx, n : int):
		channel = ctx.channel
		log.notice(f"Deleting {n} messages in [{channel.guild}:{channel}]")
		# A better way of bulk deleting since the older one was quite slow
		await channel.purge(limit=n+1)
		# async for message in channel.history(limit=n+1):
		# 	log.notice(f"Deleted message: [{message.content}:{message.author}]", 1)
		# 	await message.delete()
		log.confirm("Finished bulk deletion")

	# TODO: add command to delete all messages between 2 messages
	# messages will be passed through id, so
	# $bdel 93810310801 1230918301 will remove between 
	# 93810310801 and 1230918301
	# restrictions: both messages should be in the same channel
	# order should not matter
	@commands.has_role('admin')
	@commands.command(
		name='bulkdeleterange',
		aliases=['bulk_delete_range', 'bdelr'],
		help="""
		Borra todos los mensajes entre dos mensakes,
		los mensajes se pasan por id y tiene que estar en 
		el mismo canal.
		Solo puede utilizarse por admins.
		"""
	)
	async def bulk_delete_range(self, ctx, id1, id2):
		pass

class MemeCommands(commands.Cog):
	def __init__(self):
		pass

	# mentions the role assigned to lol and puts an image in chat
	@commands.command(
		help="menciona a los jugadores del lol"
	)
	async def lol(self, ctx):
		img = discord.File(getenv("IMG_SUMMON"))
		await ctx.send(getenv("MENTION_LOL"), file=img) 

	# MEME command, puts whatever text inputted as the parameter in 
	# the image Simón meme image
	@commands.command(
		aliases=["Simón, Simon"],
		help="coge la foto de simon y modifica el texto a el parametro"
	)
	async def simon(self, ctx, *args):
		# the coordinates of the upper left corner of the rectangel
		# where the text will be
		coords = (365, 1350)
		# the dimensions of the rectangle where the text will be
		dims = (230, 125)
		# convert the args array into a string
		text = " ".join(args)

		path = getenv("IMG_SIMON")
		# the out path of the image will be in rcs/img and the image will be called <name>.del.jpg
		out_path = path.split(".")[0] + ".del." + path.split(".")[1]

		await add_text_to_image(text, path, coords, dims, out_path)

		await ctx.send(text, file=discord.File(out_path))
		remove(out_path)