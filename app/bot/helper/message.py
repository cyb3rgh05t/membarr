import discord

# these were copied from the app object. They could be made static instead but I'm lazy.
async def embederror(recipient, message, ephemeral=True):
    embed1 = discord.Embed(title="",description=message, color=0xf50000)
    await send_embed(recipient, embed1, ephemeral)

async def embedinfo(recipient, message, ephemeral=True):
    embed1 = discord.Embed(title="",description=message, color=0x171717)
    await send_embed(recipient, embed1, ephemeral)

async def embedtitle(recipient, message, ephemeral=True):
        embed1 = discord.Embed(title=message, color=0x171717)
        await send_embed(recipient, embed1, ephemeral)

async def embedemail(recipient, message, ephemeral=True):
        time = (datetime.now() + timedelta(hours=24)).strftime("%d. %B %Y | %H:%M:%S")
        embed1 = discord.Embed(title='**'+ PLEX_SERVER_NAME +' Invite**  🎟️',description=message, color=0x171717)
        embed1.add_field(name="Gültig bis:", value='``'+ time +'``', inline=False)
        await send_embed(recipient, embed1, ephemeral)

async def embederroremail(recipient, message, ephemeral=True):
        embed1 = discord.Embed(title="",description=message, color=0xf50000)
        embed1.add_field(name="Mögliche Fehler:", value='``•`` Fehlerhaftes **EMail**-Format.\n``•`` Du bist schon bei **StreamNet** angemeldet.\n``•`` Die angegebene Email ist nicht bei **Plex** registriert.\n``•`` Username anstadt **EMail** angegeben', inline=False)
        await send_embed(recipient, embed1, ephemeral)

async def embedinfoaccept(recipient, message, ephemeral=True):
        embed1 = discord.Embed(title="",description=message, color=0x171717)
        #embed1.add_field(name="Plex Mail:", value=''+ email +'', inline=False)
        await send_embed(recipient, embed1, ephemeral)
        
async def embedcustom(recipient, title, fields, ephemeral=True):
    embed = discord.Embed(title=title)
    for k in fields:
        embed.add_field(name=str(k), value=str(fields[k]), inline=True)
    await send_embed(recipient, embed, ephemeral)

async def send_info(recipient, message, ephemeral=True):
    if isinstance(recipient, discord.InteractionResponse):
        await recipient.send_message(message, ephemeral=ephemeral)
    elif isinstance(recipient, discord.User) or isinstance(recipient, discord.member.Member) or isinstance(recipient, discord.Webhook):
        await recipient.send(message)

async def send_embed(recipient, embed, ephemeral=True):
    if isinstance(recipient, discord.User) or isinstance(recipient, discord.member.Member) or isinstance(recipient, discord.Webhook):
        await recipient.send(embed=embed)
    elif isinstance(recipient, discord.InteractionResponse):
        await recipient.send_message(embed=embed, ephemeral = ephemeral)


        
