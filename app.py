import io

import duckdb
import pandas as pd
import streamlit as st

csv = '''
beverage,price
orange juice,2.5
Expresso,2
Tea,3
'''
beverages = pd.read_csv(io.StringIO(csv))

csv2 = '''
food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
'''
food_items = pd.read_csv(io.StringIO(csv2))

answer_str = """
SELECT * FROM beverages
CROSS JOIN food_items
"""

solution_df = duckdb.sql(answer_str).df()

with st.sidebar:
    option = st.selectbox(
        "What would you like to review ?",
        ('Join', 'GroupBy', 'Windows functions'),
        index=None,
        placeholder='select a theme'
    )
    st.write('You selected:', option)

st.header("enter your code:")
query = st.text_area(label="votre code SQL ici", key="user_input")
if query:
    result = duckdb.sql(query).df()
    st.dataframe(result)

    try:
        result = result[solution_df.columns]
        st.dataframe(result.compare(solution_df.columns))
    except KeyError as e:
        st.write('Le nombre de colonne est différent')

    nb_row_diff = result.shape[0] - solution_df.shape[0]
    if nb_row_diff != 0:
        st.write(f' {nb_row_diff} lignes de différence')

tab2, tab3 = st.tabs(["Tables", "Solution"])

with tab2:
    st.write("table: beverages")
    st.dataframe(beverages)
    st.write("table: food_items")
    st.dataframe(food_items)
    st.write("expected:")
    st.dataframe(solution_df)

with tab3:
        st.write(answer_str)