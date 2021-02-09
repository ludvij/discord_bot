from discord.ext import commands
import log.logger as log

#! I didn't find a way of doing this
_DEBUG = False
	
def debug():
	async def wrapper(ctx):
		global _DEBUG
		print(_DEBUG)
		if _DEBUG != True:
			log.warn("Not in debug mode")
		return _DEBUG
	return commands.check(wrapper)

#! DEBUG STUFF
# This Cog is used to manage extensions without stopping the bot
# This Cog can only be used by the owner of the bot
class Debug(commands.Cog):
	def __init__(self, bot, extension_list):
		self.bot = bot
		self.extension_list = extension_list

	
	@commands.command(hidden=True)
	@commands.is_owner()
	async def _enabledebug(self, ctx, arg : bool):
		global _DEBUG
		_DEBUG = bool(arg)
		log.warn(f"DEBUG mode set to {_DEBUG}")


	# Stops execution, not really needed now
	@commands.command(hidden=True)
	@commands.is_owner()
	@debug()
	async def _kill(self, ctx):
		log.warn("The bot is logging out")
		await self.bot.close()

	# loads a new extension in the bot, a extension is a py module with a 
	# global setup(bot : discord.ext.commands.Bot) method that will 
	# configure what is done with the extension
	@commands.command(hidden=True)
	@commands.is_owner()
	@debug()
	async def _loadextension(self, ctx, module : str):
		self.bot.load_extension(module)
		if module not in self.extension_list:
			self.extension_list.append(module)
		log.notice(f"Loaded module {module}")

	# unloads an extension from the bot
	# if the extension is not in the bot the stack trace is something that exists
	@commands.command(hidden=True)
	@commands.is_owner()
	@debug()
	async def _unloadextension(self, ctx, module : str):
		self.bot.unload_extension(module)
		log.notice(f"Unloaded module {module}")


	# reloads all the extensions
	@commands.command(hidden=True)
	@commands.is_owner()
	@debug()
	async def _reload(self, ctx):
		for s in self.extension_list:
			self.bot.reload_extension(s)
			log.notice(f"Reloaded module {s}")
