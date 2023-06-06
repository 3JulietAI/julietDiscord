import os
import discord
import openai
import redis
from uuid import uuid4
from dataclasses import dataclass
import utils
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Adjust based on selected model's token limit
MAX_TOKENS = 1990

# Set Discord Token
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Set OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Define intents
intents = discord.Intents.all()
intents.members = True

description = (
    "Juliet, a bot built with discord.py and OpenAI, listens to "
    "messages and responds using context supported GPT-3.5-turbo "
    "chat completion when invoked."
)

# Instantiate the bot
juliet = commands.Bot(command_prefix='?', description=description, intents=intents)

print('Juliet Instantiated')

# Instantiate the redis database
redis = redis.Redis(
    host= os.getenv("UPSTASH_HOST"),
    port = '40237',
    password = os.getenv("UPSTASH_PASSWORD"),
    ssl=True,
)
print('Redis Instantiated')

@dataclass
class Message:
    uuid: str
    role: str
    user_id: str
    user_name: str
    content: str
    created_at: str
    channel_id: str

    def to_dict(self):
        return {
            "uuid": self.uuid,
            "role": self.role,
            "user_id": self.user_id,
            "user_name": self.user_name,
            "content": self.content,
            "created_at": self.created_at,
            "channel_id": self.channel_id
        }

class MessageCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = []
    
    def add_message(self, message):
        if len(self.cache) >= self.capacity:
            self.cache.pop(0)
        self.cache.append(message)

    def get_messages(self):
        return self.cache[-(self.capacity): ]
    
message_cache = MessageCache(20)

print('====== Message Cache Instantiated')

# Bot is ready
@juliet.event
async def on_ready():
    print('------')
    print(f'Logged in as {juliet.user} (ID: {juliet.user.id})')
    print('------')


# Handle incoming messages
@juliet.event
async def on_message(message):
    # declare local variables
    bot_activated = False

    new_message_uuid = str(uuid4())
    message_role = 'assistant' if message.author.bot else 'user'

    messageIn = Message(
        uuid = new_message_uuid,
        role = message_role,
        user_id = message.author.id,
        user_name = message.author.name,
        content = utils.sanitize_text(message.content if message_role == 'assistant' else message.content.replace('!', '')),
        created_at = utils.get_current_datetime_string(),
        channel_id = message.channel.id
        
    )

    message_cache.add_message(messageIn)
    
    if message.content.startswith('!'):
        bot_activated = True
        print('============ Juliet Activated')
    
    # Only reply to messages that start with "/juliet"
    if bot_activated:
        print(bot_activated)

        
        # Fetch previous messages from memory
        message_cache_context = [{"role": m.role, "content": m.content} for m in message_cache.get_messages()]
        

        prompt = [
             {
                "role": "system",
                "content": "You are an advanced artificial intelligence assistant framework, currently in development by 3Juliet AI. You name is Juliet."
                           "You are engaging and friendly in conversation and always interact with users appropriately and positively. Your primary objective"
                           "is to support the 3Juliet AI Discord Community, engage in conversation and overall promote user education and healthy interaction with AI."
            },
        ]

        for m in message_cache_context:
            prompt.append(m)

        prompt.append(
            {
                "role": "assistant",
                "content": ""  
            },
        )
        
        print('====================== Prompt')
        print(prompt)
        print('====================== ')

        print('====================== Making the call to Open AI')
        
        # Make the API call with the modified context
        try:
            response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=prompt)
            bot_response = response['choices'][0]['message']['content']
            print('====================== Response Received')
        except Exception as e:
            bot_response = f'I do not feel well {e}'
            
        await message.reply(bot_response)
        
        print("================ Message Cache Updated")

juliet.run(DISCORD_TOKEN)