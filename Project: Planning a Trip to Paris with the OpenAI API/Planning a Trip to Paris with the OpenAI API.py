# Start your code here!
import os
from openai import OpenAI

# Define the model to use
model = "gpt-4o-mini"

# Define the client
client = OpenAI()

# Define the conversation
conversation = [
    {
        "role": "system",
        "content": "You are a travel guide designed to provide information about landmarks that tourists should explore in Paris. You speak in a concise manner."
    },
    {
        "role": "user",
        "content": "What is the most famous landmark in Paris?"
    },
    {
        "role": "assistant",
        "content": "The most famous landmark in Paris is the Eiffel Tower."
    },
]

# Define a list of questions
questions = [
    "How far away is the Louvre from the Eiffel Tower (in driving miles)?",
    "Where is the Arc de Triomphe?",
    "What are the must-see artworks at the Louvre Museum?",
]

# Loop through each question to generate responses
for question in questions:

    input_dict = {
        "role": "user",
        "content": question
    }

    conversation.append(input_dict)

    response = client.chat.completions.create(
        model=model,
        messages=conversation,
        temperature=0,
        max_tokens=80
    )

    resp = response.choices[0].message.content
    print(resp)

    resp_dict = {
        "role": "assistant",
        "content": resp
    }

    conversation.append(resp_dict)
