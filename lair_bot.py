import discord
import json
import subprocess

CONFIG_FILE_NAME = 'config.json'

# Load parameters set in config.json
with open(CONFIG_FILE_NAME, 'r') as config_file:
    config = json.loads(config_file.read())

# Configure permissions
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

def cmd_docker_ps():
    short = 'docker ps'
    cmd = 'docker ps --format "table {{.Image}}\\t{{.Names}}\\t{{.RunningFor}}\\t{{.Status}}"'
    ret = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read().decode("utf-8")

    return f'```bash\n$ {short}\n{ret}```'

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='your webcam'))
    print(f'\n[!] Initialized as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    msg = ''

    match message.content:
        case '?ping':
            msg = 'Pong'
        case '?status':
            msg = cmd_docker_ps()
        case '?help':
            msg = '`?status` returns `docker ps`'

    if msg:
        await message.channel.send(msg)

bot.run(config['token'])
