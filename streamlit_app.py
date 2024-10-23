import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

# get user input
user_input = st.text_area("Enter your Markush descriptor here:", height=150)

# Call AI api when user clicks button
if st.button("Extract R-group possibilities") and user_input.strip():
    possibilities = client.chat.completions.create(
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
    st.write("Extracted R-group possibilities:")
    st.write(possibilities.choices[0].message.content)
    permutations = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Given these extracted R-group possibilities, generate all possible permutations of the chemical given the R-groups."
            },
            {
                "role": "user",
                "content": possibilities.choices[0].message.content
            }
        ]
    )
    st.write("Generated chemical permutations:")
    st.write(permutations.choices[0].message.content)
    smiles = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Given these generated chemical permutations, generate the chemical SMILES string for each permutation."
            },
            {
                "role": "user",
                "content": permutations.choices[0].message.content
            }
        ]
    )
    st.write("Extracted R-group possibilities:")
    st.write(possibilities.choices[0].message.content)
else:
    st.write("Please enter a Markush descriptor and click the button to extract R-group possibilities.")
