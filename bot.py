# imports
from sys import argv
from os import getenv
from dotenv import load_dotenv
from discord.ext import commands
import log.logger  as log
#!DEBUG
from cogs import cog_commands, cog_debug, cog_listeners, cog_voice
# load the .env file
load_dotenv(dotenv_path=r'rcs\bot.env')
# instantiation of bot

class Bot(commands.Bot):
	def __init__(self):
		# set the rpefix to PREFIX insede the .env
		# or just mention the code
		super().__init__(command_prefix=commands.when_mentioned_or(getenv("PREFIX")))

		self.add_cog(cog_debug.ExtensionManager())

		
	def init_extensions(self, extension_list):
		for s in extension_list:
			self.load_extension(s)

	def run(self):
		super().run(getenv("TOKEN"))


	def full_load(self):	
		extension_list = [
			"cogs.cog_listeners", 
			"cogs.cog_commands", 
			"cogs.cog_voice"
			]
		self.init_extensions(extension_list)
		
		
	def half_load(self):	
		self.add_cog(cog_listeners.Listeners(self))
		self.add_cog(cog_voice.GeneralVoice())
		self.add_cog(cog_commands.Commands())

	# error handler
	async def on_command_error(self, ctx, exception):
		await ctx.send("Error")
		await ctx.send_help(ctx.invoked_with)
		log.error(f"Failed execution / parsing of {ctx.command}")
		log.error(f"Caused by {exception}", 1)
		
		
bot = Bot()

def main():
	print(argv)
	if len(argv) == 1 or argv[1] == '-f':
		bot.full_load()
	elif argv[1] == '-h':
		bot.half_load()
	bot.run()

if __name__ == '__main__':
	main()