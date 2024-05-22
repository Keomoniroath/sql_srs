import duckdb
import streamlit as st
import os
from datetime import date, timedelta

if "data" not in os.listdir():
    os.mkdir("data")

if "exercises_sql_tables.duckdb" not in os.listdir("data"):
    exec(open("init_db.py").read())

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)


def compare_user_query(q: str):
    result = con.execute(q).df()
    st.dataframe(result)
    try:
        result = result[solution_df.columns]
        st.dataframe(result.compare(solution_df))
        if result.compare(solution_df).shape == (0, 0):
            st.write('Correct')
            st.balloons()
    except KeyError as e:
        st.write('Le nombre de colonne est différent')
    nb_row_diff = result.shape[0] - solution_df.shape[0]
    if nb_row_diff != 0:
        st.write(f' {nb_row_diff} lignes de différence')


with st.sidebar:
    themes = con.execute("SELECT theme FROM memory_state").df()
    theme = st.selectbox(
        "What would you like to review ?",
        themes['theme'].unique(),
        index=None,
        placeholder='select a theme'
    )

    if theme:
        st.write('You selected:', theme)
        query_select_ex = f"SELECT * FROM memory_state WHERE theme = '{theme}'"
    else:
        query_select_ex = "SELECT * FROM memory_state"

    exercise = con.execute(query_select_ex).df().sort_values(
        "last_reviewed").reset_index(drop=True)
    st.write(exercise)
    exercise_name = exercise.loc[0, "exercise_name"]
    with open(f"answer/{exercise_name}.sql", "r") as f:
        answer = f.read()

    solution_df = con.execute(answer).df()

st.header("enter your code:")
query = st.text_area(label="votre code SQL ici", key="user_input")

if query:
    compare_user_query(query)

for n_days in [2, 7, 14]:
    if st.button(f"Revoir dans {n_days}"):
        next_review = date.today() + timedelta(days=n_days)
        con.execute(
            f"UPDATE memory_state SET last_reviewed = '{next_review}' WHERE exercise_name = '{exercise_name}'"
        )
        st.rerun()

if st.button('Reset'):
    con.execute("UPDATE memory_state SET last_reviewed = '1970-01-01'")
    st.rerun()

tab2, tab3 = st.tabs(["Tables", "Solution"])

with tab2:
    exercise_tables = exercise.loc[0, "tables"]
    for table in exercise_tables:
        st.write(f"table: {table}")
        df_table = con.execute(f"SELECT * FROM {table}").df()
        st.dataframe(df_table)

with tab3:
    st.write(answer)
