import duckdb
import streamlit as st

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

with st.sidebar:
    theme = st.selectbox(
        "What would you like to review ?",
        ('cross_joins', 'GroupBy', 'Windows functions'),
        index=None,
        placeholder='select a theme'
    )
    st.write('You selected:', theme)

    exercise = con.execute(f"SELECT * FROM memory_state WHERE theme = '{theme}'").df().sort_values(
        "last_reviewed").reset_index()
    st.write(exercise)

    if not exercise.empty:
        exercise_name = exercise.loc[0, "exercise_name"]
        with open(f"answer/{exercise_name}.sql", "r") as f:
            answer = f.read()

        solution_df = con.execute(answer).df()

st.header("enter your code:")
query = st.text_area(label="votre code SQL ici", key="user_input")

if query:
    result = con.execute(query).df()
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
    exercise_tables = exercise.loc[0, "tables"]
    for table in exercise_tables:
        st.write(f"table: {table}")
        df_table = con.execute(f"SELECT * FROM {table}").df()
        st.dataframe(df_table)

with tab3:
    st.write(answer)
