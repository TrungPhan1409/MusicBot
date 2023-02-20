import discord
import youtube_dlc

from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.messages = True
client = commands.Bot(command_prefix='$', intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    print('-----')
    
@client.command()
async def play(ctx, *, query):
    voice_channel = ctx.author.voice.channel
    if voice_channel is None:
        await ctx.send("You need to be in a voice channel to use this command.")
        return

    vc = await voice_channel.connect()

    ydl_opts = {
        'format': 'bestaudio',
        'noplaylist': True,
        'no-cache-dir': True
    }
    with youtube_dlc.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(query, download=True)
            if 'entries' in info:
                info = info['entries'][0]
            url = info['url']
            title = info['title']
        except Exception as e:
            await ctx.send("An error occurred while trying to get the song. Please try again.")
            print(f"An error occurred while trying to get the song: {e}")
            return

    vc.play(discord.FFmpegPCMAudio(url), after=lambda e: print('done', e))
    await ctx.send(f"Now playing: {title}")

client.run('MTA3MzM3MzE5MDI3NDk1MzI4Nw.GsJBHY.Q_nrAwns62arVoWRak_aPWF_bjewijWRx5jnNQ')
