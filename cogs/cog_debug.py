from discord.ext import commands

#! DEBUG STUFF
# This Cog is used to manage extensions without stopping the bot
# This Cog can only be used by the owner of the bot
class Debug(commands.Cog):
	def __init__(self, bot, extension_list):
		self.bot = bot
		self.extension_list = extension_list

	# Stops execution, not really needed now
	@commands.command(hidden=True)
	@commands.is_owner()
	async def _kill(self, ctx):
		warn("The bot is logging out")
		await self.bot.close()

	# loads a new extension in the bot, a extension is a py module with a 
	# global setup(bot : discord.ext.commands.Bot) method that will 
	# configure what is done with the extension
	@commands.command(hidden=True)
	@commands.is_owner()
	async def _loadextension(self, ctx, module : str):
		self.bot.load_extension(module)
		if module not in self.extension_list:
			self.extension_list.append(module)
		notice(f"Loaded module {module}")

	# unloads an extension from the bot
	# if the extension is not in the bot the stack trace is something that exists
	@commands.command(hidden=True)
	@commands.is_owner()
	async def _unloadextension(self, ctx, module : str):
		self.bot.unload_extension(module)
		notice(f"Unloaded module {module}")

	# reloads all the extensions
	@commands.command(hidden=True)
	@commands.is_owner()
	async def _reload(self, ctx):
		for s in self.extension_list:
			self.bot.reload_extension(s)
			notice(f"Reloaded module {s}")

# TODO: move this to a log module or something like that
def notice(msg):
	print(f"{bcolors.OKCYAN}[NOTICE]: {msg}{bcolors.ENDC}")

def warn(msg):
	print(f"{bcolors.WARN}[WARN]: {msg}{bcolors.ENDC}")

def error(msg):
	print(f"{bcolors.FAIL}[ERROR]: {msg}{bcolors.ENDC}")
	
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'