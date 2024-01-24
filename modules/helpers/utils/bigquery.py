# Third party imports
import google.cloud.bigquery as bq
from langchain_community.document_loaders import BigQueryLoader
import pandas as pd

def get_bigquery_schema_query(dataset: str) -> str:
    """
    Gets the BigQuery schema SQL query for a dataset.

    Args:
        dataset (str): the BigQuery dataset

    Returns:
        str: the query
    """

    query = f"""
SELECT table_name, ddl
FROM `{dataset}.INFORMATION_SCHEMA.TABLES`
WHERE table_type = 'BASE TABLE'
ORDER BY table_name;
"""

    return query


def load_bigquery_data(project: str, dataset: str) -> str:
    """
    Loads the BigQuery dataset schema into a DataFrame.
    """

    query = get_bigquery_schema_query(dataset)

    loader = BigQueryLoader(
        query,
        project=project,
        metadata_columns="table_name",
        page_content_columns="ddl",
    )

    data = loader.load()

    return data

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
