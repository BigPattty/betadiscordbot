import discord
from discord.ext import commands
import os

intents = discord.Intents.all()
client = commands.Bot(command_prefix = commands.when_mentioned_or("!"), intents = intents, help_command = None)

class Dropdown(discord.ui.Select):
  def __init__(self, cog_names):
    for cog_name in cog_names:
      options = [
        discord.SelectOption(label = cog_name, value = f'{cog_name}', description = f'{client.get_cog(cog_name).description}')
      ]
    super().__init__(placeholder = "Click here!", max_values = 1, min_values = 1, options = options)

  async def callback(self, interaction: discord.Interaction):
    cog_name = self.values[0][4:]
    cog = client.get_cog(cog_name)
    if cog:
      embed = discord.Embed(
        title = f"Help Menu: {cog_name}",
        description = 'Here are your commands!',
        color = 0x79FCBB)

      commands_list = cog.get_commands()
      for command in commands_list:
        embed.add_field(
          name = "`!" + f"{command.name}`\n",
          value = command.help or "A description so good, not even I know it\n",
          inline = False)
        embed.set_footer("Designed by TPK")

      await interaction.response.edit_message(embed = embed, view = DropView(self.cog_names))

class DropView(discord.ui.View):
  def __init__(self, cog_names, *, timeout = 180):
    super().__init__(timeout = timeout)
    self.cog_names = cog_names
    self.add_selmenu()
    


  def add_selmenu():
    self.add_item(Dropdown(self.cog_names))


@client.command(name = "help")
async def command_help(ctx):
  cog_names = [cog_name for cog_name, cog in client.cogs.items() if cog.get_commands()]

  if not cog_names:
    await ctx.send("It appears I dont have any commands, *or TPK fucked up the code*")

  helpembed = discord.Embed(
    title = "Help Menu",
    description = "Select a catergory to get more help!",
    color = 0x79FCBB
  )

  await ctx.send(embed = helpembed, view = DropView(cog_names))


async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandNotFound):
    print(f"Command run by {ctx.author.id} not found!\nCommand: {ctx.author.message}")

  else:
    print(f"An error has occur when running {ctx.author.message}: {error}") 

@client.event
async def on_ready():
  print("\n"f'Logged in through terminal to {client.user.name}  ID: {client.user.id}')

  for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
      try:
        await client.load_extension(f"cogs.{filename[:-3]}")
        print("\n"f'Loaded: {filename[:-3]}')

      except Exception as e:
        print('\n'f"Failed to load extension {filename[:-3]}: *** {e} ***")

client.run("")
