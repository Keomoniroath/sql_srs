import pandas as pd
import streamlit as st
import duckdb

st.write('SQL SRS')

with st.sidebar:
    option = st.selectbox(
        "What would you like to review ?",
        ('Join', 'GroupBy', 'Windows functions'),
        index=None,
        placeholder='select a theme'
    )

    st.write('You selected:', option)

data = {"a": [1, 2, 3], "b": [4, 5, 6]}
df = pd.DataFrame(data)

q = st.text_area(label="Tapez votre input")
result = duckdb.sql(q).df()
st.write(f"vous avez entré la query: {q}")
st.dataframe(result)