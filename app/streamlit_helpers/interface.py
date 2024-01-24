# Local application/library specific imports
import config.config as config
from helpers.llm.bigquery import (
    get_bigquery_query,
    get_bigquery_error_resolution_query,
)
from helpers.llm.question_classification import (
    get_question_classification
)
from helpers.utils.bigquery import (
  get_dataframe_from_bq_query,
)
from streamlit_helpers.visualization import (
  get_visualization_image,
)

# Third party imports
import google.cloud.bigquery as bq
import streamlit as st


def create_interface(llm, bq_data):
    """
    Creates a streamlit interface for the BigQuery Billing Bot.
    """

    # get bq client for querying dataset
    client = bq.Client(project=config.project)

    st.header("GCP Billing with Vertex AI", divider="rainbow")

    st.subheader("Ask a question about billing")

    # billing question
    user_query = st.text_input(
        "Question: \n\n", key="user_query", value="What are my top 5 most expensive services used?"
    )

    # ask question button
    generate_t2t = st.button("Ask Question", key="generate_t2t")

    # generate answer
    if generate_t2t and user_query:
        with st.spinner("Generating answer..."):
            response_tab, sql_query_prompt_tab, sql_query_tab, viz_code_prompt_tab, viz_code_tab = st.tabs([
                "Response",
                "SQL Query Prompt",
                "SQL Query",
                "Visualization Code Prompt",
                "Visualization Code",
            ])

            question_class = get_question_classification(llm, user_query)

            bq_sql_query, prompt = get_bigquery_query(llm, bq_data, user_query, question_class)

            big_query_error = None
            try:
                df = get_dataframe_from_bq_query(client, bq_sql_query)
            except Exception as e:
                print("The following GoogleSQL code is invalid:")
                print(bq_sql_query)
                print("The following error was raised, trying to self correct:")
                print(e)

                bq_sql_query = get_bigquery_error_resolution_query(llm, bq_data, bq_sql_query, str(e))

                try:
                    df = get_dataframe_from_bq_query(client, bq_sql_query)

                except Exception as e2:
                    print("The following GoogleSQL code is invalid:")
                    print(bq_sql_query)
                    print("The following error was raised, giving up:")
                    print(e2)

                    big_query_error = str(e2)
                    df = None

            visualization_code = ""
            viz_code_prompt = ""
            with response_tab:
                if big_query_error is not None:
                    st.write("Error:")
                    st.markdown(f"```\n{big_query_error}\n```")

                    st.write("Failed GoogleSQL query:")
                    st.markdown(f"```sql\n{bq_sql_query}\n```")
                else:
                    image_array, visualization_code, viz_code_prompt, visualization_error = get_visualization_image(llm, user_query, df)

                    df_col, viz_col = st.columns(2)

                    with df_col:
                        st.header("DataFrame")
                        st.markdown(df.to_markdown())

                    with viz_col:
                        st.header("Visualization")

                        if visualization_error is None:
                            st.image(
                                image=image_array,
                                caption=None,
                                width=None,
                                use_column_width=None,
                                clamp=False,
                                channels="RGB",
                                output_format="auto",
                            )
                        else:
                            st.write("Visualization failed:")
                            st.markdown(f"```{visualization_error}```")

            with sql_query_prompt_tab:
                st.markdown(prompt)

            with sql_query_tab:
                st.markdown(f"```sql\n{bq_sql_query}\n```")

            with viz_code_prompt_tab:
                st.markdown(viz_code_prompt)

            with viz_code_tab:
                st.markdown(f"```py\n{visualization_code}\n```")
