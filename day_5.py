# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 14:41:09 2024

@author: hs124084
"""

import numpy as np
import altair as alt
import pandas as pd
import streamlit as st

st.header('st.write')

st.write('Hello, *World!* :sunglasses:')

st.write(1234)

df = pd.DataFrame({
    'first column': [1,2,3,4],
    'second column': [10,20,30,40]
    })
st.write(df)
st.write("#"*30)
st.write('Below is a DataFrame:',df,'Active is a dataframe')
st.write("#"*30)

df2 = pd.DataFrame(np.random.randn(200,3),
                   columns=['a','b','c'])
c = alt.Chart(df2).mark_circle().encode(
    x='a',y='b',size='c',color='c',tooltip=['a','b','c'])
st.write(c)

