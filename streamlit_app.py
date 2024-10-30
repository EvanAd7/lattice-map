import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from itertools import product

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

def parse_r_groups(r_groups_text):
    # Parse R-groups text into a dictionary of possibilities
    r_groups = {}
    for line in r_groups_text.strip().split('\n'):
        line = line.strip()
        if line:
            group, smiles = line.split(':')
            r_groups[group] = [s.strip() for s in smiles.split(',')]
    return r_groups

def generate_permutations(template_smiles, r_groups):
    # Get all possible combinations of R-groups
    keys = sorted(r_groups.keys())  # Sort to ensure consistent order
    values = [r_groups[k] for k in keys]
    all_combinations = list(product(*values))
    
    # Generate each permutation
    permutations = []
    for combo in all_combinations:
        current_smiles = template_smiles
        for i, key in enumerate(keys):
            current_smiles = current_smiles.replace(f'[{key}]', combo[i])
        permutations.append(current_smiles)

    return permutations

def get_ai_response(messages):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    return response.choices[0].message.content

def process_input(user_input, template_smiles):
    # Get R-group possibilities from AI
    possibilities = get_ai_response([
        {"role": "system", "content": """You are helping me do a transformation of natural language chemical descriptions into chemical SMILES codes. A user will give you a verbal description of variable chemical groups (R1, R2,...,Rn). Then, you will take these verbal descriptions and output the possible SMILES for each given variable group.
        For example, R1 might be verbally described as either a methyl or ethyl group. From this, you will output the SMILES codes for both a methyl and ethyl group, under R1. Output NOTHING but the variable groups, separated by newlines, followed by its SMILES code, separated by commas. Here is an example format:
        R1: C, CC
        R2: CC=C, CCC
        R3: O"""
        },
        {"role": "user", "content": user_input}
    ])
    st.write("Extracted R-group possibilities:")
    st.write(possibilities)
    
    # Parse R-groups
    r_groups = parse_r_groups(possibilities)
    
    # Generate all permutations
    permutations = generate_permutations(template_smiles, r_groups)
    st.write(f"Generated {len(permutations)} permutations:")
    for i, perm in enumerate(permutations, 1):
        st.write(f"{i}. {perm}")


# Streamlit UI
st.title("Chemical Patent Analysis")
template_smiles = st.text_input("Enter the base SMILES for you chemical diagram:")
user_input = st.text_area("Enter your chemical descriptors here:", height=150)

if st.button("Process") and user_input.strip() and template_smiles.strip():
    process_input(user_input, template_smiles)
else:
    st.write("Please enter base SMILES, chemical descriptors, and click the button to process.")
