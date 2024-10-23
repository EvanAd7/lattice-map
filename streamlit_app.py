import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

# Get Markush descriptor from user and save it in a variable
user_input = st.text_input("Enter your Markush descriptor here:")

completions = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": "Given the natural language description of variable R-groups from this chemical patent, extract all the individual possibilities for each R-group."
        },
        {
            "role": "user",
            "content": user_input
        }
    ]
)

# Display the result in the Streamlit UI
st.write("Extracted R-group possibilities:")
st.write(completions.choices[0].message.content)
