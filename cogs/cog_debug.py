from discord.ext import commands
import log.logger as log

#! DEBUG STUFF
# This Cog is used to manage extensions without stopping the bot
# This Cog can only be used by the owner of the bot
class ExtensionManager(commands.Cog):
	def __init__(self):
		pass

	# Stops execution, not really needed now
	@commands.command(hidden=True)
	@commands.is_owner()
	async def _kill(self, ctx):
		log.warn("The bot is logging out")
		await ctx.bot.close()

	# loads a new extension in the bot, a extension is a py module with a 
	# global setup(bot : discord.ext.commands.Bot) method that will 
	# configure what is done with the extension
	@commands.command(hidden=True)
	@commands.is_owner()
	async def _load(self, ctx, module : str):
		if module in ctx.bot.extensions:
			log.warn(f"Extension: {module} is loaded")
			return;
		self.bot.load_extension(module)

	# unloads an extension from the bot
	# if the extension is not in the bot the stack trace is something that exists
	@commands.command(hidden=True)
	@commands.is_owner()
	async def _unload(self, ctx, module : str):
		if module not in ctx.bot.extensions:
			log.error(f"Extension: {module} is not loaded")
			return;
		self.bot.unload_extension(module)


	# reloads all the extensions
	@commands.command(hidden=True)
	@commands.is_owner()
	async def _reload(self, ctx):
		log.warn("Reloading:")
		for s in ctx.bot.extensions:
			ctx.bot.reload_extension(s)
		await ctx.send(f"Reload ended")
