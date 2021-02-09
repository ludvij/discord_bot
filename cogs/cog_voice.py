import discord
from discord.utils import get
from discord.ext import commands

# this Cog will handle the radio stuff
def setup(bot):
	bot.add_cog(GeneralVoice())
	bot.add_cog(RadioConnect())


class RadioConnect(commands.Cog):
	def __init__(self):
		pass

	# it's a mixture of join and play audio
	@commands.command(aliases=["plr"])
	async def playradio(self, ctx, url = "http://radio3.rtveradio.cires21.com/radio3.mp3"):
		voice = get(ctx.bot.voice_clients, guild=ctx.guild)
		channel = ctx.author.voice.channel

		if voice == None:
			await channel.connect()
			voice = get(ctx.bot.voice_clients, guild=ctx.guild)
		elif channel == None:
			await ctx.send("You are not in a voice chat")
			return
		else: 
			await voice.move_to(channel)

		ff = discord.FFmpegPCMAudio(url)

		voice.play(ff)

		

# This Cog has the most common voice commands
class GeneralVoice(commands.Cog):
	def __init__(self):
		pass

	@commands.command()
	async def join(self, ctx):
		voice = get(ctx.bot.voice_clients, guild=ctx.guild)
		channel = ctx.author.voice.channel

		if voice == None:
			await channel.connect()
		elif channel == None:
			await ctx.send("You are not in a voice chat")
		else: 
			await voice.move_to(channel)

	@commands.command(aliases=['d'])
	async def disconnect(self, ctx):
		voice = get(ctx.bot.voice_clients, guild=ctx.guild)

		if voice == None:
			await ctx.send("El bot no está conectado a un chat de voz")
		else:
			await voice.disconnect()


	@commands.command()
	async def pause(self, ctx):
		voice = get(ctx.bot.voice_clients, guild=ctx.guild)
		if voice == None:
			await ctx.send("El bot no está conectado a un chat de voz")
		elif not voice.is_playing():
			await ctx.send("El bot no está reproduciendo sonido")
		else:
			voice.pause()
	
	@commands.command()
	async def resume(self, ctx):
		voice = get(ctx.bot.voice_clients, guild=ctx.guild)

		if voice == None:
			await ctx.send("El bot no está conectado a un chat de voz")
		elif voice.is_playing():
			await ctx.send("El bot ya está reproduciendo sonido")
		else:
			voice.resume()

	@commands.command()
	async def stop(self, ctx):
		voice = get(ctx.bot.voice_clients, guild=ctx.guild)
		voice.stop()