import discord
from discord.ext import commands
import keep_alive
import os

intents = discord.Intents.default()
intents.message_content = True  # To read message content (required for commands)

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')


@bot.command(name="help")
async def help_menu(ctx):
    help_text = ("# Help Menu:\n"
                 "## Available Commands:\n"
                 "- !help - Brings up this menu.\n"
                 "- !profile - Brings up your profile.\n"
                 "- !vote - Vote in an active election.\n"
                 "- !elec-register - Register for an election.\n"
                 "- !party-register - Register a party.\n"
                 "- !business-register - Register a business.\n")
    await ctx.send(help_text)


@bot.command(name="profile")
async def profile(ctx):
    member = ctx.author
    nickname = member.nick if member.nick else member.name
    user_party = "N/A"
    join_date = member.joined_at.strftime("%B %d, %Y")

    # Finds the players region
    if any(role.name == "Ashcomber" for role in member.roles):
        region = "Ashcombe"
    elif any(role.name == "Dunbridger" for role in member.roles):
        region = "Dunbridger"
    elif any(role.name == "Kenwooder" for role in member.roles):
        region = "Kenwood"
    elif any(role.name == "Fairbournian" for role in member.roles):
        region = "Fairbourne"
    elif any(role.name == "Cranlian" for role in member.roles):
        region = "Cranley"
    else:
        region = "N/A"

    profile_msg = f"# {nickname}'s Profile \nJoined Server on: {join_date} \nRegion: {region}\nParty: {user_party}"
    await ctx.send(profile_msg)


election_active = False

candidates = [""]
@bot.command(name="vote")
async def vote(ctx, candidate: str):
    if election_active:
        if int(candidate) > 0:
            user_ID = ctx.author.id
            choice = candidates[candidate]
            elections_admin = await bot.fetch_user(1103001028946837586)
            await elections_admin.send(f"# Vote Filed:\nUserID: {user_ID}\nChoice: {choice}")
        else:
            await ctx.send("Invalid candidate number.")
    else:
        await ctx.send("There is no elections currently.")


election_keys = []
party_keys = ["IND"]


@bot.command(name="elec-register")
async def elec_register(ctx, elec_key: str, party_key: str):
    if len(election_keys) == 0:
        await ctx.send("There is no elections currently.")
    else:
        if elec_key in election_keys:
            if party_key in party_keys:
                user_id = ctx.author.id
                nickname = ctx.author.nick or ctx.author.name
                elec_reg_msg = (
                    f"# New Election Candidate Registered\nUsername: {nickname}\nUserID: {user_id}\nElection Key: {elec_key}\nParty Key: {party_key}"
                )
                elections_admin = await bot.fetch_user(1103001028946837586)
                await elections_admin.send(elec_reg_msg)
                await ctx.send("Registration Submitted.")
            else:
                await ctx.send("Invalid Party Key.")
        else:
            await ctx.send("Invalid Election Key.")


parties = ["INDEPENDANT"]


@bot.command(name="party-register")
async def party_register(ctx, party_name: str, party_hex: str):
    if party_name not in parties:
        if len(party_hex) == 7:
            user_id = ctx.author.id
            nickname = ctx.author.nick or ctx.author.name
            party_reg_msg = (
                f"# New Party Registration Application:\nFounderID: {user_id}\nFounder: {nickname}\nParty Name: {party_name}\nParty Hex: {party_hex}"
            )
            elections_admin = await bot.fetch_user(1103001028946837586)
            await elections_admin.send(party_reg_msg)
        else:
            await ctx.send("Invalid Hex Code.")
    else:
        await ctx.send("Invalid Party Name")

@bot.command(name="business-register")
async def business_register(ctx, business_name: str, business_hex: str)
    if len(party_hex) == 7:
        user_id = ctx.author.id
        nickname = ctx.author.nick or ctx.author.name
        business_reg_msg = (
        f"# New Business Registration Application:\nFounderID: {user_id}\nFounder: {nickname}\nBusiness Name: {business_name}\nBusiness Hex: {business_hex}"
        )
        business_admin = await bot.fetch_user(1103001028946837586)
        await business_admin.send(business_reg_msg)
    else:
        await ctx.send("Invalid Hex Code.")

keep_alive.keep_alive()

bot.run(os.getenv("TOKEN"))
