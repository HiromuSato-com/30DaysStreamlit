"""
Created on Fri Jul  5 16:13:32 2024

@author: hs124084
"""

import streamlit as st
import os

# Everything is accessible via the st.secrets dict:
st.write("DB username:", st.secrets["db_username"]) # Hiromu
st.write("DB password:", st.secrets["db_password"]) # mumuHiro15
st.write("My cool secrets:", st.secrets["my_cool_secrets"]["things_i_like"]) # Dog and Mimi

# And the root-level secrets are also accessible as environment variables:
st.write(
    "Has environment variables been set:",
    os.environ["db_username"] == st.secrets["db_username"],
)

st.title('st.secrets')

st.write(st.secrets['message'])
