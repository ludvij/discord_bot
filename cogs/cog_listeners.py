from discord.ext import commands
import log.logger as log

def setup(bot):
	bot.add_cog(Listeners(bot))



class Listeners(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		log.log(f"Bot logged in as {self.bot.user.name}")

	@commands.Cog.listener()
	async def on_message(self, message):
		author = message.author
		content = message.content
		guild = message.guild
		channel = message.channel
		time = message.created_at

		text = f"\t{author} said: [{content}] in [{guild}:{channel}] at {time}"
		log.log(text)