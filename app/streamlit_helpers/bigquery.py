# Local application/library specific imports
import config.config as config

# Third party imports
import google.cloud.bigquery as bq
from langchain_community.document_loaders import BigQueryLoader
import pandas as pd

def get_dataframe_from_bq_query(client: bq.Client, query: str) -> pd.DataFrame:
    """
    Gets a dataframe from a BigQuery query.

    Args:
        client (bq.Client): the BigQuery client
        query (str): the query to run

    Returns:
        pd.DataFrame: the dataframe
    """

    df = client.query(query).result().to_dataframe()

    return df

def load_bigquery_data():
    """
    Loads the BigQuery dataset schema into a DataFrame.
    """

    query = f"""
SELECT table_name, ddl
FROM `{config.bigquery_dataset}.INFORMATION_SCHEMA.TABLES`
WHERE table_type = 'BASE TABLE'
ORDER BY table_name;
    """

    loader = BigQueryLoader(
        query,
        project=config.project,
        metadata_columns="table_name",
        page_content_columns="ddl",
    )

    data = loader.load()

    return data
