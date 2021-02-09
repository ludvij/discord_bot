# imports
from os import getenv
from dotenv import load_dotenv
from discord.ext import commands
#!DEBUG
from cogs import cog_debug

load_dotenv(dotenv_path=r'rcs\bot.env')

class Bot(commands.Bot):
	def __init__(self):
		super().__init__(command_prefix=getenv("PREFIX"))
		extension_list = [
			"cogs.cog_listeners", 
			"cogs.cog_commands", 
			"cogs.cog_voice"
			]

		self.add_cog(cog_debug.Debug(self, extension_list))

		self.init_extensions(extension_list)
		
	def init_extensions(self, extension_list):
		for s in extension_list:
			self.load_extension(s)

	def run(self):
		super().run(getenv("TOKEN"))




if __name__ == '__main__':
	bot = Bot()
	bot.run()