# imports
from os import getenv
from dotenv import load_dotenv
from discord.ext import commands
# scripts
import bot_commands

class Bot(commands.Bot):
	def __init__(self):
		super().__init__(command_prefix='$')
		load_dotenv(dotenv_path=r'rcs\bot.env')
		# Load the commands in the bot
		self.add_cog(bot_commands.Commands())

	def run(self):
		super().run(getenv("TOKEN"))

	# decorator @bot.event not needed since we are in a class
	async def on_ready(self):
		print("bot is ready")

	async def on_message(self, message):
		author = message.author
		content = message.content
		guild = message.guild
		channel = message.channel
		time = message.created_at

		text = f"{author} said: [{content}] in [{guild}:{channel}] at {time}"
		print(text)
		await self.process_commands(message)



if __name__ == '__main__':
	bot = Bot()
	bot.run()