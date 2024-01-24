# Local application/library specific imports
import config.config as config

from helpers.utils.bigquery import load_bigquery_data
from streamlit_helpers.interface import create_interface
from streamlit_helpers.llm import initialize_llm

# Third party imports
from langchain_community.document_loaders import BigQueryLoader
import vertexai
import streamlit as st

# initialize Vertex AI and LLM
#
vertexai.init(project=config.project, location=config.location)

# set up LLM
#
@st.cache_resource
def load_models():
    return initialize_llm()


# load BigQuery schema info
#
@st.cache_resource
def load_bigquery():
    """
    Loads the BigQuery dataset schema into a DataFrame.
    """

    return load_bigquery_data(
        project=config.project,
        dataset=config.bigquery_dataset,
    )

# create streamlit interface
#
create_interface(
    llm=load_models(),
    bq_data=load_bigquery(),
)
