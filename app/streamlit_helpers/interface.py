# Local application/library specific imports
import config.config as config
from helpers.llm.question_classification import (
    get_question_classification
)
from helpers.utils.markdown import strip_markdown
from helpers.prompts.bigquery import (
    create_bq_error_resolution_prompt_template,
    create_bq_prompt_template,
)
from streamlit_helpers.bigquery import (
  get_dataframe_from_bq_query,
)
from streamlit_helpers.llm import (
    create_bq_chain,
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

    st.header("BigQuery Billing Bot with Vertex AI", divider="rainbow")

    st.subheader("Ask a question about billing")

    # billing question
    user_query = st.text_input(
        "Enter question about billing: \n\n", key="user_query", value="What are my top 5 most expensive services used?"
    )

    # ask question button
    generate_t2t = st.button("Ask question", key="generate_t2t")

    # generate answer
    if generate_t2t and user_query:
        # st.write(prompt)
        with st.spinner("Generating answer..."):
            first_tab1, first_tab2 = st.tabs(["Response", "Prompt"])

            question_class = get_question_classification(llm, user_query)
            prompt_template = create_bq_prompt_template(user_query, question_class)
            chain = create_bq_chain(llm, prompt_template)

            # get bq client for querying dataset
            client = bq.Client(project=config.project)

            with first_tab1:
                # Invoke the chain with the documents, and remove code backticks
                _result = chain.invoke(bq_data)
                result = strip_markdown(_result)

                try:
                    result_df = get_dataframe_from_bq_query(client, result)

                except Exception as e:
                    print("The following GoogleSQL code is invalid:")
                    print(result)
                    print("The following error was raised, trying to self correct:")
                    print(e)

                    prompt_template = create_bq_error_resolution_prompt_template(result, str(e))

                    chain = create_bq_chain(llm, prompt_template)

                    # invoke the chain with the bq docs, and
                    _result = chain.invoke(bq_data)
                    # remove markdown code snippet backticks
                    result = strip_markdown(_result)

                    try:
                        result_df = get_dataframe_from_bq_query(client, result)

                    except Exception as e2:
                        print("The following GoogleSQL code is invalid:")
                        print(result)
                        print("The following error was raised, giving up:")
                        print(e2)

                        st.write("GoogleSQL code is invalid:")
                        st.markdown(_result)
                        st.write("Error:")
                        st.markdown(f"```{str(e2)}```")

                        result_df = None

                visualization_error = None
                if result_df is not None:
                    image_array, visualization_code, visualization_error = get_visualization_image(llm, user_query, result_df)

                    col1, col2 = st.columns(2)

                    with col1:
                        st.header("DataFrame")
                        st.markdown(result_df.to_markdown())

                    with col2:
                        st.header("Visualization")
                        viz_tab1, viz_tab2 = st.tabs(["Image", "Code"])

                        with viz_tab1:
                            if visualization_error is not None:
                                st.write("Visualization failed:")
                                st.markdown(f"```{visualization_error}```")

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

                        with viz_tab2:
                            st.markdown(f"```py\n{visualization_code}```")

            with first_tab2:
                st.text(prompt_template.format(content=bq_data))
