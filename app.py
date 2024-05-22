import ast
import duckdb
import streamlit as st

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

#solution = duckdb.sql(answer).df()

with st.sidebar:
    theme = st.selectbox(
        "What would you like to review ?",
        ('cross_joins', 'GroupBy', 'Windows functions'),
        index=None,
        placeholder='select a theme'
    )
    st.write('You selected:', theme)

    exercise = con.execute(f"SELECT * FROM memory_state WHERE theme = '{theme}'").df()
    st.write(exercise)

st.header("enter your code:")
query = st.text_area(label="votre code SQL ici", key="user_input")

if query:
    result = con.execute(query).df()
    st.dataframe(result)


tab2, tab3 = st.tabs(["Tables", "Solution"])

with tab2:
    exercise_tables = ast.literal_eval(exercise.loc[0, "tables"])
    for table in exercise_tables:
        st.write(f"table: {table}")
        df_table = con.execute(f"SELECT * FROM {table}").df()
        st.dataframe(df_table)

with tab3:
    exercise_name = exercise.loc[0, "exercise_name"]
    with open(f"answer/{exercise_name}.sql", "r") as f:
        answer = f.read()
    st.write(answer)

