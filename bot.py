# command line arguments
from sys import argv
# env things
from os import getenv
from dotenv import load_dotenv
# discord
import discord
from discord.ext import commands
# log
import log.logger  as log
#!DEBUG
from cogs import cCommands, cDebug, cListeners, cVoice
# load the .env file
load_dotenv(dotenv_path=r'rcs\bot.env')
# instantiation of bot

class Bot(commands.Bot):
	def __init__(self):
		# set the rpefix to PREFIX insede the .env
		# or just mention the code
		super().__init__(
			command_prefix=commands.when_mentioned_or(getenv("PREFIX")), 
			intents=discord.Intents.all()
		)

		self.add_cog(cDebug.Debug_commands())

	# When the bot is ready to use it says hello in the command
	async def on_ready(self):
		log.internal(f"Bot logged in as {self.user.name}")
		await self.change_presence(activity=discord.Game('Gamin\''))

		
	def init_extensions(self, extension_list):
		for s in extension_list:
			self.load_extension(s)

	def run(self):
		super().run(getenv("TOKEN"))

	# loads everything
	def full_load(self):	
		extension_list = [
			"cogs.cListeners", 
			"cogs.cCommands", 
			"cogs.cVoice"
		]
		self.init_extensions(extension_list)
		
	# loads only cogs that doesn't requiere pip installed pkgs
	def half_load(self):	
		self.add_cog(cListeners.Listeners(self))
		self.add_cog(cVoice.General_voice())
		self.add_cog(cCommands.Commands())

	# error handler
	async def on_command_error(self, ctx, exception):
		await ctx.send(f"[Error] {exception.args[0]}")
		await ctx.send_help(ctx.invoked_with)
		log.error(f"Failed execution / parsing of {ctx.command}")
		log.error(f"Caused by {exception}", 1)
		
		
bot = Bot()

def main():
	if len(argv) == 1 or argv[1] == '-f':
		bot.full_load()
	elif argv[1] == '-h':
		bot.half_load()
	bot.run()

if __name__ == '__main__':
	main()