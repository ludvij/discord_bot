import os
import asyncio
import discord
import youtube_dl
from io import BufferedWriter
import log.logger as log
from os import getenv, remove
from discord.ext import commands
# scripts
from scripts import ascii_video
from scripts import image_text


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
		self.video_play = False

	# TODO: join these two commands
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
		await ctx.message.delete()
		
		channel = ctx.channel
		log.notice(f"Deleting {n} messages in [{channel.guild}:{channel}]")
		# A better way of bulk deleting since the older one was quite slow
		await channel.purge(limit=n)
		# async for message in channel.history(limit=n+1):
		# 	log.notice(f"Deleted message: [{message.content}:{message.author}]", 1)
		# 	await message.delete()
		log.confirm("Finished bulk deletion", 1)

	# messages will be passed through id, so
	# $bdelr 93810310801 1230918301 will remove between 
	# 93810310801 and 1230918301
	# restrictions: both messages should be in the same channel
	# order should not matter
	@commands.has_role('admin')
	@commands.command(
		name='bulkdeleterange',
		aliases=['bulk_delete_range', 'bdelr'],
		help="""
		Borra todos los mensajes entre dos mensajes,
		los mensajes se pasan por id y tiene que estar en 
		el mismo canal.
		Solo puede utilizarse por admins.
		"""
	)
	async def bulk_delete_range(self, ctx, id1 : int, id2 : int):
		# delete command message
		await ctx.message.delete()

		m1 = await ctx.fetch_message(id1)
		m2 = await ctx.fetch_message(id2)

		# since the messages to delete must be between m1 and m2, that is
		# after m1 before m2. So m1 must be the lower one
		if m1.created_at > m2.created_at:
			m1, m2 = m2, m1
		
		log.notice(f"removing from {m1.id}:{m1.created_at} to {m2.id}:{m2.created_at}")
		await ctx.channel.purge(before=m2.created_at, after=m1.created_at)
		log.confirm("Finished bulk deletion", 1)


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

	@commands.command(
		aliases=['showv'],
		help="""
		Convierte un video a ASCII
		"""
	)
	async def showvideo(self, ctx, URL : str):
		# stuff to download the video
		# no audio, worst quality possible
		vid_path = fr"rcs\video\ascii.mp4"
		ydl_opts = {
			"format" : '160',
			"outtmpl" : vid_path,
		}
		# download the video
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			ydl.download([URL])
		# asynchronous generator, I have no idea what i'm doing
		# but I think this will make the bot run better
		generator = ascii_video.process(vid_path, 60, 33)
		self.video_play = True
		c = 0
		# turning off the listener cog momentarily
		while self.video_play:
			try:
				res = await generator.__anext__()
				#log.log(f"\n{res}")
				await ctx.send(res)
				c += 1
			except StopAsyncIteration:
				log.notice(f"stopped at frame {c}", 1)
				self.video_play = False

	@commands.command(
		aliases=['stopv'],
		help="""
		Para la ejecución de showvideo
		"""
	)
	async def stopvideo(self, ctx):
		self.video_play = False
		ctx.send("stopped reproduction")
		log.confirm("stopped reproduction", 1)

	@commands.command(
		aliases=['showa'],
		help="""
		Convierte una imagen a ASCII, se tiene que pasar la id
		del mensaje que tiene la imagen para convertirse a ASCII.
		Devuelve el resultado como un .txt.
		Si se añade reverse al final se invertiran blancos por negros.
		"""
	)
	async def showascii(self, ctx, id : int, reverse=""):
		# first check if the command is in reverse mode

		message = await ctx.fetch_message(id) 
		# check if message has attachments
		if len(message.attachments) == 0:
			log.error("$showascii message doesn't hava attachments")
			return
		img = message.attachments[0]
		# check if attachment is an image
		valid_ext = ['jpg', 'jpeg', 'png']
		if not any(img.filename.lower().endswith(image) for image in valid_ext):
			log.error(f"$showascii attachment {img.filename} is not supported")
			return
		# save the image to apply the algorithm
		await img.save(img.filename)
		# apply algorithm
		reverse = reverse == 'reverse' 
		res = ascii_video.image_to_ascii(img.filename, pheight=720, reverse=reverse)
		# save result in text
		out_path = 'res.txt'
		with open(out_path, 'w') as f:
			f.write(res)
		await ctx.channel.send("ASCII art",file=discord.File(out_path))
		# delete filename
		os.remove(img.filename)
		os.remove(out_path)

		

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

		await image_text.add_text(text, path, coords, dims, out_path)

		await ctx.send(text, file=discord.File(out_path))
		remove(out_path)