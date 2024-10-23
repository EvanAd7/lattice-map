import os
import streamlit as st
from openai import AsyncOpenAI
from dotenv import load_dotenv
import asyncio

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

async def get_ai_response(messages):
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    return response.choices[0].message.content

async def process_input(user_input):
    # First API call
    possibilities = await get_ai_response([
        {"role": "system", "content": "Given the natural language description of variable R-groups from this chemical patent, extract all the individual possibilities for each R-group."},
        {"role": "user", "content": user_input}
    ])
    st.write("Processing R-groups...")

    # Second API call
    permutations = await get_ai_response([
        {"role": "system", "content": "Given these extracted R-group possibilities, generate the SMILES string for each chemical possibility."},
        {"role": "user", "content": possibilities}
    ])
    st.write("Calculating permutations...")

    # Third API call
    smiles = await get_ai_response([
        {"role": "system", "content": "Given these generated SMILES strings based on the variable R-groups, generate the chemical SMILES string for each permutation of the chemical, as a list. Generate ONLY the SMILES strings, nothing else."},
        {"role": "user", "content": permutations}
    ])
    st.write("Chemical SMILES strings:")
    st.write(smiles)

# Streamlit UI
st.title("Chemical Patent Analysis")
user_input = st.text_area("Enter your Markush descriptor here:", height=150)

if st.button("Process") and user_input.strip():
    asyncio.run(process_input(user_input))
else:
    st.write("Please enter a Markush descriptor and click the button to process.")
