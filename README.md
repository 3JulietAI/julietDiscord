# Building Juliet(d): A Step-by-Step Guide to Creating a Discord Bot Power by Chat GPT

Author: 3jDev  |  June 5, 2023


  This article is an in-depth guide to building your own Discord bot using Python, discord.py, [Open AI's](https://www.openai.com) powerful GPT-3.5-turbo model and deploying it on [Railway.app](https://railway.app/). This bot is an extension of an experimental AGI framework called Juliet that we are developing at [3Juliet AI](https://www.3juliet.ai).

  Before we dive in, this guide assumes a basic understanding of Python programming. If you're a beginner or intermediate Python developer, you're in the right place!

Here is a link to the GitHub repository: [3JulietAI/juliet-discord](https://github.com/3JulietAI/julietDiscord)


### Setting Up The Environment

Before we start coding, you need to set up your development environment. We'll be using Python, and we'll need to install a few packages. You can do this using pip:

```python
  pip install discord.py python-dotenv openai
```
These are the packages we'll be using:

-  "discord.py": A modern, easy-to-use, feature-rich, and async-ready API wrapper for Discord written in Python.
-  "python-dotenv": This allows us to utilize a .env file to load our environment variables.
-  "openai": The Open AI API client library.

  Next, create a .env file to store your environment variables. For this bot, we need two tokens: the Discord token for your bot and the Open AI API key.

```makefile
  DISCORD_TOKEN=your_discord_token
  OPENAI_API_KEY=your_openai_api_key
```
Don't forget to replace "your_discord_token" and "your_openai_api_key" with your actual token values.  


### The Bot Code

Now let's dive into the code. The first part of our script will import the necessary modules and load our environment variables.

```py
  import os
  import discord
  from discord.ext import commands
  from dotenv import load_dotenv
  import openai
  
  # Load environment variables
  load_dotenv()
  
  DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
  OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
```

  The "load_dotenv" function loads environment variables from a .env file, which we use to set the Discord token and Open AI API key.


#### Defining the Bot

Next, we're going to define our bot. We'll start with a brief description, and then we'll create an instance of "commands.Bot".

```python
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
```

  Here, `command_prefix` is set to "Juliet: ". This means that users will need to preface their commands with "Juliet: " to interact with the bot.

  We also set the maximum token limit to 4096 as per the selected model's limit. Tokens in GPT-3.5-turbo are chunks of text. Too much text can exceed the model's maximum limit.

  The messages list is an in-memory store that we use to keep track of the context of the conversation. This is an interim solution for a minimal viable product, and in upcoming versions, we plan to persist this data using a Redis JSON database for more efficient context recall and a more robust data persistence strategy.


#### Bot Events

With our bot defined, we can now add some event handlers:

```python
  @bot.event
  async def on_ready():
      print(f'Logged in as {bot.user} (ID: {bot.user.id})')
      print('------')
  
  # Handle incoming messages
  @bot.event
  async def on_message(message):
      # ...
```
  In the "on_ready" event handler, we print out the bot's username and ID when the bot is ready. The "on_message" event handler is where we handle each incoming message, check if it's a command for Juliet, and generate a response.

1. Ignores messages from the bot itself to prevent loops.
2. Stores the incoming message in a list for context, capturing details such as the content, timestamp, and author. Note that in future versions, we will use a Redis JSON database to provide a robust and scalable storage solution for these messages.
3. Checks if the message starts with 'Juliet: ', if so, it treats the rest of the message as a user query.
4. Generates a message context, including a system message, the user query, and the last few messages.
5. Calls the Open AI API with the constructed context, retrieves the assistant's message, and sends it back to the Discord channel.

  The system message is an introduction of Juliet, explaining her role, objectives, and approachability. It's the first message in the context and sets the stage for the conversation.

```python
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
```


#### Running the Bot

Finally, we just need to start the bot with our Discord token.

```python
  bot.run(DISCORD_TOKEN)
```

And that's it! Your AI-powered Discord bot is ready. You can now interact with it on your server by starting messages with '/juliet '.

The completed code is both powerful and flexible. You can modify it to suit your needs, whether you want to change the bot's behaviors, add new commands, or adjust its interactions.

Good luck with your coding journey, and have fun building with AI!
