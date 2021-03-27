import os
import discord
import youtube_dl
from os import getenv, remove
from discord.utils import get
from datetime import timedelta
from discord.ext import commands
from typing import Optional, Union
# log
import log.logger as log
# scripts
from scripts import image_text
from scripts import ascii_video


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

	@commands.command(
		aliases=['pfp'],
		help="""
		Muestra la imagen del usuario al que se ha mencionado.
		Si no se menciona a nadie se muestra la de la persona que invocó el comando.
		"""
	)
	async def profilepicture(self, ctx, user:Union[commands.MemberConverter, commands.RoleConverter]=None):
		if user is None:
			await ctx.send(ctx.author.avatar_url_as(format='png'))
		elif type(user) == discord.Role:
			[await ctx.send(member.avatar_url_as(format='png')) for member in user.members]
		else:
			await ctx.send(user.avatar_url_as(format='png'))

	# @commands.command(aliases=['chco'])
	# async def changeColor(self, ctx, colour):
	# 	colour = int(colour, 16)
	# 	if (colour > 0xffffff):
	# 		raise Exception("Invalid colour")
	# 	user = ctx.author
	# 	r_name = f'colour_{user}'
	# 	c_role = None
	# 	for r in user.roles:
	# 		if r.name == r_name: 
	# 			c_role = r		
	# 	if c_role == None:
	# 		for r in ctx.guild.roles:
	# 			if r.name == r_name:
	# 				c_role = r
	# 		if c_role == None:
	# 			c_role = await ctx.guild.create_role(name=r_name, colour=colour, mentionable=False)
	# 			pos = len(ctx.guild.roles) - 2
	# 			await c_role.edit(position=pos)
	# 		await user.add_roles(c_role)
	# 	else:
	# 		await c_role.edit(colour=colour)



	# command to delete a specified number of commands in a text channel
	# or betwen two commands
	@commands.command(
		name='clear',
		help="""
		Si se pasa solo un argument el bot borrará x mensaje en el canal del comando.
		Si se pasan dos argumentos, ambos tienen que ser ids de mensajes del mismo canal, 
		el bot borrará todos los mensajes entre ellos, ellos incluidos.
		Solo puede utilizarse por admins.
		"""
	)
	@commands.has_role('admin')
	async def bulk_delete(self, ctx, n_or_m1:Union[commands.MessageConverter, int], m2:commands.MessageConverter=None):
		await ctx.message.delete()
		if m2 == None:
			n = n_or_m1 
			channel = ctx.channel		
			log.notice(f"Deleting {n} messages in [{channel.guild}:{channel}]")
			# A better way of bulk deleting since the older one was quite slow
			await channel.purge(limit=n)
		else:
			m1 = n_or_m1
			if m1.channel != m2.channel:
				raise commands.CommandError(f"msg {m1.channel}:{m1.id} and msg {m2.channel}:{m2.id} are not in the same channel")
			if m1.created_at > m2.created_at:
				m1, m2 = m2, m1
		
			log.notice(f"removing from {m1.id}:{m1.created_at} to {m2.id}:{m2.created_at}")
			await ctx.channel.purge(before=m2.created_at + timedelta(0,1), after=m1.created_at - timedelta(0,1))
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


	#? should I move the ydl thing to a function later ?
	@commands.command(
		aliases=['showv'],
		help="""
		Convierte un video a ASCII
		"""
	)
	async def showvideo(self, ctx, URL:str):
		# stuff to download the video
		# no audio, worst quality possible
		vid_path = fr"rcs\video\ascii.mp4"
		if os.path.exists(vid_path):
			os.remove(vid_path)
		ydl_opts = {
			"format" : '160',
			"outtmpl" : vid_path,
		}
		# download the video
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			ydl.download([URL])
		# asynchronous generator, I have no idea what i'm doing
		# but I think this will make the bot run better
		agen = ascii_video.process(vid_path, 60, 33)
		self.video_play = True
		async for res in agen:
			await ctx.send(res, delete_after=10)
			if not self.video_play: break
		# TODO find a way to fix this
		agen = None
		try:
			os.remove(vid_path)
		except PermissionError:
			pass

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
	async def showascii(self, ctx, message:commands.MessageConverter, reverse:Optional[str]):
		# check if message has attachments
		if len(message.attachments) == 0:
			raise commands.CommandError(message=f"Message {message.id} doesn't have attachments")
		img = message.attachments[0]
		# check if attachment is an image
		valid_ext = ['jpg', 'jpeg', 'png']
		if not any(img.filename.lower().endswith(image) for image in valid_ext):
			raise commands.CommandError(message=f"Attachment {img.filename} is not supported")
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
		help="Coge la foto de simon y modifica el texto a el parametro"
	)
	async def simon(self, ctx, *text):
		print(text)
		coords = (365, 1350) # the coordinates of the upper left corner of the rectangle where the text will be
		dims = (230, 125) # the dimensions of the rectangle where the text will be
		# convert the args array into a string and stuff for teh default argument
		# because  I don't want to add "" in the command
		if (text != ()):
			text = " ".join(text)
		else: text = "Simón"

		path = getenv("IMG_SIMON")
		# the out path of the image will be in rcs/img and the image will be called <name>.del.jpg
		out_path = path.split(".")[0] + ".del." + path.split(".")[1]

		await image_text.add_text(text, path, coords, dims, out_path)

		await ctx.send(text, file=discord.File(out_path))
		remove(out_path)

	@commands.command(
		help="""
		Respondes a un mensaje y devuelve un mensaje cambiando todas las vocales por i
		"""
	)
	async def mimimi(self, ctx):#, opt:Optional[str]):
		msg = ctx.message.reference.resolved.content
		msg = msg.translate({ord(c): 'I' for c in 'AEOU'})
		msg = msg.translate({ord(c): 'Í' for c in 'ÁÉÓÚ'})
		msg = msg.translate({ord(c): 'Ì' for c in 'ÀÈÒÙ'})
		msg = msg.translate({ord(c): 'Ï' for c in 'ÄËÖÜ'})
		msg = msg.translate({ord(c): 'Î' for c in 'ÂÊÔÛ'})
		msg = msg.translate({ord(c): 'i' for c in 'aeou'})
		msg = msg.translate({ord(c): 'í' for c in 'áéóú'})
		msg = msg.translate({ord(c): 'ì' for c in 'àèòù'})
		msg = msg.translate({ord(c): 'ï' for c in 'äëöü'})
		msg = msg.translate({ord(c): 'î' for c in 'âêôû'})
		# if opt == 'tts':
		# 	msg = '/tts ' + msg
		await ctx.send(msg)

