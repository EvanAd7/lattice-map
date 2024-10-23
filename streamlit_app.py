import os
import streamlit as st
from openai import AsyncOpenAI
from dotenv import load_dotenv
import asyncio

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

@st.cache_data
async def get_ai_response(messages):
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    return response.choices[0].message.content

async def process_input(user_input):
    # First API call
    possibilities = await get_ai_response([
        {
            "role": "system",
            "content": "Given the natural language description of variable R-groups from this chemical patent, extract all the individual possibilities for each R-group."
        },
        {
            "role": "user",
            "content": user_input
        }
    ])
    st.write(possibilities)

    # Second API call
    permutations = await get_ai_response([
        {
            "role": "system",
            "content": "Given these extracted R-group possibilities, generate all possible permutations of the chemical given the R-groups."
        },
        {
            "role": "user",
            "content": possibilities
        }
    ])
    st.write(permutations)

    # Third API call
    smiles = await get_ai_response([
        {
            "role": "system",
            "content": "Given these generated chemical permutations, generate the chemical SMILES string for each permutation."
        },
        {
            "role": "user",
            "content": permutations
        }
    ])
    st.write(smiles)

# Streamlit UI
st.title("Chemical Patent Analysis")
user_input = st.text_area("Enter your Markush descriptor here:", height=150)

if st.button("Get all possible SMILES strings") and user_input.strip():
    asyncio.run(process_input(user_input))
else:
    st.write("Please enter a Markush descriptor and click the button to process.")
