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



The completed code is both powerful and flexible. You can modify it to suit your needs, whether you want to change the bot's behaviors, add new commands, or adjust its interactions.

Good luck with your coding journey, and have fun building with AI!
