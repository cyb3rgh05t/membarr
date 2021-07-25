import logging
import discord
from discord.ext import commands
import asyncio
from plexapi.myplex import MyPlexAccount
from discord import Webhook, AsyncWebhookAdapter
from app.bot.helper.confighelper import roles, PLEXUSER, PLEXPASS, PLEX_SERVER_NAME, Plex_LIBS
logging.basicConfig(filename="app/config/invitarr.log", filemode='a', level=logging.ERROR)
import app.bot.helper.db as db
import app.bot.helper.plexhelper as plexhelper
import texttable
import os 

try:
    account = MyPlexAccount(PLEXUSER, PLEXPASS)
    plex = account.resource(PLEX_SERVER_NAME).connect()  # returns a PlexServer instance
    logging.info('Logged into plex!')
except:
    logging.error('Error with plex login. Please check username and password and Plex server name.')

class app(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        logging.info('Made by Sleepingpirate https://github.com/Sleepingpirates/')
        logging.info(f'Logged in as {self.bot.user} (ID: {self.bot.user.id})')
        logging.info('------')
    
    async def embederror(self, author, message):
        embed1 = discord.Embed(title="ERROR",description=message, color=0xf50000)
        await author.send(embed=embed1)

    async def embedinfo(self, author, message):
        embed1 = discord.Embed(title=message, color=0x00F500)
        await author.send(embed=embed1)

    async def getemail(self, after):
        email = None
        await self.embedinfo(after,'Welcome To '+ PLEX_SERVER_NAME +'. Just reply with your email so we can add you to Plex!')
        await self.embedinfo(after,'I will wait 15 minutes for your message, if you do not send it by then I will cancel the command.')
        while(email == None):
            def check(m):
                return m.author == after and not m.guild
            try:
                email = await self.bot.wait_for('message', timeout=200, check=check)
                if(plexhelper.verifyemail(str(email.content))):
                    return str(email.content)
                else:
                    email = None
                    message = "Invalid email. Please just type in your email and nothing else."
                    await self.embederror(after, message)
                    continue
            except asyncio.TimeoutError:
                message = "Timed Out. Message Server Admin with your email so They Can Add You Manually."
                await self.embederror(after, message)
                return None

    async def addtoplex(self, email, channel):
        if(plexhelper.verifyemail(email)):
            if plexhelper.plexadd(plex,email):
                await self.embedinfo(channel, 'There was an error adding this email address. Message Server Admin.')
                return True
            else:
                await self.embederror(channel, 'There was an error adding this email address. Check logs.')
                return False
        else:
            await self.embederror(channel, 'Invalid email.')
            return False

    async def removefromplex(self, email, channel):
        if(plexhelper.verifyemail(email)):
            if plexhelper.plexadd(plex,email):
                await self.embedinfo(channel, 'There was an error removing this email address. Message Server Admin.')
                return True
            else:
                await self.embederror(channel, 'There was an error removing this email address. Check logs.')
                return False
        else:
            await self.embederror(channel, 'Invalid email.')
            return False
    
    #Auto add or remove user from plex if role is given or taken. 

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        roles_in_guild = after.guild.roles
        role = None
        for role_for_app in roles:
            for role_in_guild in roles_in_guild:
                if role_in_guild.name == role_for_app:
                    role = role_in_guild

                if role is not None and (role in after.roles and role not in before.roles):
                    email = await self.getemail(after)
                    if email is not None:
                        await self.embedinfo(after, "Got it we will be adding your email to plex shortly!")
                        if plexhelper.plexadd(plex,email):
                            db.save_user(str(after.id), email)
                            await asyncio.sleep(5)
                            await self.embedinfo(after, 'You have Been Added To Plex! Login to plex and accept the invite!')
                        else:
                            await self.embedinfo(after, 'There was an error adding this email address. Message Server Admin.')
                    return

                elif role is not None and (role not in after.roles and role in before.roles):
                    try:
                        user_id = after.id
                        email = db.get_useremail(user_id)
                        plexremove(email)
                        deleted = db.delete_user(user_id)
                        if deleted:
                            logging.info("Removed {} from db".format(email))
                            #await secure.send(plexname + ' ' + after.mention + ' was removed from plex')
                        else:
                            logging.error("Cannot remove this user from db.")
                    except:
                        logging.error("Cannot remove this user from plex.")
                    return


    @commands.has_permissions(administrator=True)
    @commands.command()
    async def plexinvite(self, ctx):
        email = str(ctx.content)
        await self.addtoplex(email, ctx.channel)
    
    @commands.has_permissions(administrator=True)
    @commands.command()
    async def plexremove(self, ctx):
        email = str(ctx.content)
        await self.removefromplex(email, ctx.channel)
        
    @commands.has_permissions(administrator=True)
    @commands.command()
    async def dbadd(self, ctx, email, member: discord.Member):
        #await self.addtoplex(email, ctx.channel)
        if plexhelper.verifyemail(email):
            try:
                db.save_user(str(member.id), email)
                await self.embedinfo(ctx.channel,'email and user were added to the database.')
            except Exception as e:
                await self.embedinfo(ctx.channel, 'There was an error adding this email address to database.')
                logging.error(e)
        else:
            await self.embederror(ctx.channel, 'Invalid email.')

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def dbls(self, ctx):

        embed = discord.Embed(title='Invitarr Database.')
        all = db.read_useremail()
        table = texttable.Texttable()
        table.set_cols_dtype(["t", "t", "t"])
        table.set_cols_align(["c", "c", "c"])
        header = ("#", "Name", "Email")
        table.add_row(header)
        for index, peoples in enumerate(all):
            index = index + 1
            id = int(peoples[1])
            dbuser = self.bot.get_user(id)
            dbemail = peoples[2]
            try:
                username = dbuser.name
            except:
                username = "User Not Found."
            embed.add_field(name=f"**{index}. {username}**", value=dbemail+'\n', inline=False)
            table.add_row((index, username, dbemail))
        
        total = str(len(all))
        if(len(all)>25):
            f = open("db.txt", "w")
            f.write(table.draw())
            f.close()
            await ctx.channel.send("Database too large! Total: {total}".format(total = total),file=discord.File('db.txt'))
        else:
            await ctx.channel.send(embed = embed)
        
            

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def dbrm(self, ctx, position):
        embed = discord.Embed(title='Invitarr Database.')
        all = db.read_useremail()
        table = texttable.Texttable()
        table.set_cols_dtype(["t", "t", "t"])
        table.set_cols_align(["c", "c", "c"])
        header = ("#", "Name", "Email")
        table.add_row(header)
        for index, peoples in enumerate(all):
            index = index + 1
            id = int(peoples[1])
            dbuser = self.bot.get_user(id)
            dbemail = peoples[2]
            try:
                username = dbuser.name
            except:
                username = "User Not Found."
            embed.add_field(name=f"**{index}. {username}**", value=dbemail+'\n', inline=False)
            table.add_row((index, username, dbemail))

        try:
            position = int(position) - 1
            id = all[position][1]
            email = db.get_useremail(id)
            deleted = db.delete_user(id)
            if deleted:
                logging.info("Removed {} from db".format(email))
                await self.embedinfo(ctx.channel,"Removed {} from db".format(email))
            else:
                await self.embederror(ctx.channel,"Cannot remove this user from db.")
        except Exception as e:
            logging.error(e)

def setup(bot):
    bot.add_cog(app(bot))