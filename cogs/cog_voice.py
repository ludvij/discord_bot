import discord
from discord.utils import get
from discord.ext import commands
# log
import log.logger as log
# this Cog will handle the radio stuff
def setup(bot):
	log.warn(f"Loading extension: {__name__}")

	bot.add_cog(GeneralVoice())
	log.notice("Loaded cog: GeneralVoice",1)
	bot.add_cog(RadioConnect())
	log.notice("Loaded cog: RadioConnect",1)

	log.confirm(f"Loaded extension: {__name__}")

def teardown(bot):
	log.warn(f"Unloading extension: {__name__}")

	log.notice("Unloaded cog: GeneralVoice",1)
	log.notice(f"Unloaded cog: RadioConnect",1)
	
	log.confirm(f"Unloaded extension: {__name__}")

class RadioConnect(commands.Cog):
	def __init__(self):
		pass

	# it's a mixture of join and play audio
	@commands.command(
		aliases=["plr"], 
		help="""
		Se va a conectar a un mp3 o archivo de video valido en el internete.
		El uso general es para escuchar la radio.
		"""
	)
	async def playradio(self, ctx, url = "http://radio3.rtveradio.cires21.com/radio3.mp3"):
		voice = get(ctx.bot.voice_clients, guild=ctx.guild)

		if ctx.author.voice == None:
			raise commands.CommandError(f"User {ctx.author} is not connected to a voice channel")
		channel = ctx.author.voice.channel
		if voice == None:
			await channel.connect()
			voice = get(ctx.bot.voice_clients, guild=ctx.guild)
		else: 
			await voice.move_to(channel)

		ff = discord.FFmpegPCMAudio(url)
		if (voice.is_playing()):
			voice.stop()

		voice.play(ff)

		

# This Cog has the most common voice commands
class GeneralVoice(commands.Cog):
	def __init__(self):
		pass

	@commands.command(help="Se une al chat de voz donde está el usuario que lo llamó.")
	async def join(self, ctx):
		voice = get(ctx.bot.voice_clients, guild=ctx.guild)
		channel = ctx.author.voice.channel

		if voice == None:
			await channel.connect()
		elif channel == None:
			await ctx.send("You are not in a voice chat")
		else: 
			await voice.move_to(channel)

	@commands.command(aliases=['d'], help="El bot se desconecta del chat de voz.")
	async def disconnect(self, ctx):
		voice = get(ctx.bot.voice_clients, guild=ctx.guild)

		if voice == None:
			await ctx.send("El bot no está conectado a un chat de voz")
		else:
			await voice.disconnect()


	@commands.command(help="Se pausa la reproducción de audio, se puede retomar con $resume")
	async def pause(self, ctx):
		voice = get(ctx.bot.voice_clients, guild=ctx.guild)
		if voice == None:
			await ctx.send("El bot no está conectado a un chat de voz")
		elif not voice.is_playing():
			await ctx.send("El bot no está reproduciendo sonido")
		else:
			voice.pause()
	
	@commands.command(help="Se continua la reproducción de audio si fue pausada con $pause")
	async def resume(self, ctx):
		voice = get(ctx.bot.voice_clients, guild=ctx.guild)

		if voice == None:
			await ctx.send("El bot no está conectado a un chat de voz")
		elif voice.is_playing():
			await ctx.send("El bot ya está reproduciendo sonido")
		else:
			voice.resume()

	@commands.command(help="Se para totalmente la reproducción de audio, no se puede resumir")
	async def stop(self, ctx):
		voice = get(ctx.bot.voice_clients, guild=ctx.guild)
		voice.stop()