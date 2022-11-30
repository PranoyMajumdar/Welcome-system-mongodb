import discord
from discord.ext import commands
from config import TOKEN
from mongo import welcome_db

intents = discord.Intents.default()
intents.message_content = True # For the message content intent
class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=intents)

    async def on_ready(self) -> None:
        print("Subscribe to CodeWithPranoy")

    
    async def on_member_join(self, member: discord.Member):
        if not (find:=welcome_db.find_one({"_id": str(member.guild.id)})):
            return

        channel = self.get_channel(find['channel']) or await self.fetch_channel(find['channel'])
        message = welcome_formatter(find['message'], member)
        if channel:
            await channel.send(message)


bot = MyBot()


# Welcome Message Formatter
def welcome_formatter(message: str, member: discord.Member):
    formats = {
        "[user]": member.name,
        "[user_mention]": member.mention,
        "[guild]": member.guild.name,
        "[member_avatar]": member.display_avatar.url
    }
    formated_message = message
    for key, value in formats.items():
        formated_message = formated_message.replace(key, value)

    return formated_message


@bot.group(name='welcome', invoke_without_subcommand=True)
async def welcome(ctx: commands.Context):
    return


@welcome.command(name='enable')
async def enable(ctx: commands.Context):
    if (find := welcome_db.find_one({"_id": str(ctx.guild.id)})):
        return await ctx.send("Welcome already enabled.")

    welcome_db.insert_one({
        "_id": str(ctx.guild.id),
        "channel": None,
        "message": 'Welcome [user] to [guild]!'
    })
    await ctx.send("Welcome module is successfully enabled.")


@welcome.command(name='disable')
async def disable(ctx: commands.Context):
    if not (find := welcome_db.find_one({"_id": str(ctx.guild.id)})):
        return await ctx.send("Welcome module is not enabled!")

    welcome_db.delete_one({"_id": str(ctx.guild.id)})
    await ctx.send("Welcome module is successfully disabled!")


@welcome.command(name='message')
async def message(ctx: commands.Context, *, message: str):
    if not (find := welcome_db.find_one({"_id": str(ctx.guild.id)})):
        return await ctx.send("Welcome module is not enabled!")

    welcome_db.update_one({"_id": str(ctx.guild.id)}, {
                          "$set": {"message": message}})
    await ctx.send("Welcome message successfully updated!")


@welcome.command(name='channel')
async def channel(ctx: commands.Context, channel: discord.TextChannel):
    if not (find := welcome_db.find_one({"_id": str(ctx.guild.id)})):
        return await ctx.send("Welcome module is not enabled!")

    welcome_db.update_one({"_id": str(ctx.guild.id)}, {
                          "$set": {"channel": channel.id}})
    await ctx.send("Welcome channel successfully updated!")

@welcome.command(name='test')
async def test(ctx: commands.Context):
    await bot.on_member_join(ctx.author)

if __name__ == '__main__':
    bot.run(TOKEN)
