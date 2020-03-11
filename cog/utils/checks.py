from discord.ext import commands

def is_admin():
    async def predicate(ctx):
        if ctx.author.id not in [259932683206000651, 577724543469092874]:
            raise commands.CheckFailure(f"You do not have permission to use **{ctx.command}**")
        else:
            return True
    return commands.check(predicate)