from discord.ext import commands
import log.logger as log

def setup(bot):
	log.warn(f"Unloading extension: {__name__}")
	bot.add_cog(Listeners(bot))
	log.notice(f"Unloaded cog: Listeners",1)
	log.confirm(f"Unloaded extension: {__name__}")

def teardown(bot):
	log.warn(f"Unloading extension: {__name__}")
	log.notice(f"Unloaded cog: Listeners",1)
	log.confirm(f"Unloaded extension: {__name__}")


class Listeners(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	# When the bot is ready to use it says hello in the command
	@commands.Cog.listener()
	async def on_ready(self):
		log.log(f"Bot logged in as {self.bot.user.name}")

	# Registers something each time a message is sent is the guild is in
	@commands.Cog.listener()
	async def on_message(self, message):
		author = message.author
		content = message.content
		guild = message.guild
		channel = message.channel
		time = message.created_at

		text = f"\t{author} said: [{content}] in [{guild}:{channel}] at {time}"
		log.log(text)