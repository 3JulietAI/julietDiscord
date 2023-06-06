import json
from datetime import datetime as dt
import openai
import re

def get_current_datetime_string():
    now = dt.now()
    return now.strftime("%Y-%m-%d %H:%M:%S.%f")

def get_timestamp():
    timestamp = dt.now().timestamp()
    return timestamp * 1000

def gpt_embedding(content, engine='text-embedding-ada-002'):
    # fix any UNICODE errors
    content = content.encode(encoding='ASCII', errors='ignore').decode()
    # create the embedding
    response = openai.Embedding.create(input=content, engine=engine)
    # vectorize the embedding and return it
    vector = response['data'][0]['embedding']
    return vector

def sanitize_text(text: str) -> str:
    # Add sanitizing rules here
    text = re.sub(r'<[^>]+>', '', text)  # Remove content between < and >
    text = text.replace("@", "")  # Remove @ symbols
    text = text.replace("#", "")  # Remove # symbols
    return text