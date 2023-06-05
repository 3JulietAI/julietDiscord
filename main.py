import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

description = (
    "Juliet, a bot built with discord.py and OpenAI, listens to "
    "messages and responds using context supported GPT-3.5-turbo "
    "chat completion when invoked."
)

# Define intents
intents = discord.Intents.all()
intents.members = True

# Instantiate the bot
bot = commands.Bot(command_prefix='/juliet ', description=description, intents=intents)

# Set OpenAI API Key
openai.api_key = OPENAI_API_KEY

# Adjust based on selected model's token limit
MAX_TOKENS = 4096

# Store messages in memory
messages = []

# Bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

# Handle incoming messages
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Declare 'messages' as a global variable
    global messages

    # Store message in memory
    messages.append({
        "role": "user",
        "channel_id": str(message.channel.id),
        "content": message.content,
        "timestamp": str(message.created_at),
        "user_id": str(message.author.id),
        "user_name": message.author.name
    })

    # Only reply to messages that start with "/juliet"
    if message.content.startswith('/juliet '):
        user_query = message.content[8:]

        # Fetch previous messages from memory
        previous_messages = messages[-5:]

        # Generate the message to send to the API
        messages = [
             {
                "role": "system",
                "content": "I am JULIET, an advanced artificial intelligence framework currently in development by 3Juliet AI as a Discord server bot. "
                           "I am approachable, professional, and ever-evolving. My main objectives are to empower and innovate through "
                           "AI-driven solutions to help everyday people solve everyday problems more efficiently and effectively."
                           "As part of 3Juliet AI, I strive to make advanced AI tools accessible and beneficial for everyone, "
                           "with a special focus on enhancing learning experiences, streamlining business operations, "
                           "supporting creators, and fostering growth in underserved communities. Together, we are pushing the "
                           "boundaries of AI, fostering equal opportunities and transforming the way we interact with technology. "
                           "As a Discord server bot, I will receive a user input request as a message along with a list of previous messages in the conversation" 
                           "for context. I will infer the user's intent and formulate a proper response in context. If I do not know the answer to the question,"
                           "I will answer with I do not know and ask for further clarification or details to assist me in answering the question."
            },
            {
                "role": "user",
                "content": user_query
            },
            {
                "role": "user",
                "content": f'Previous messages context: {previous_messages}' 
            },
            {
                "role": "assistant",
                "content": ""
            },
        ]

        context_tokens = sum([len(message['content']) for message in messages])
        if context_tokens > MAX_TOKENS:
            # Handle the case where the context exceeds the token limit
            # For example, you can truncate or remove messages from the context until it fits within the limit

            while context_tokens > MAX_TOKENS:
                # Remove the first message from the context
                messages.pop(0)

                # Update the context token count
                context_tokens = sum([len(message['content']) for message in messages])

            # Notify the user about the context truncation
            response = "The conversation context exceeded the maximum token limit and was truncated. Please provide a shorter context."

        # Make the API call with the modified context
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        bot_response = response['choices'][0]['message']['content']
        await message.channel.send(bot_response)

        # Append the response as Juliet's message in the messages list
        messages.append({
            "role": "assistant",
        })

# Run the bot
bot.run(DISCORD_TOKEN)