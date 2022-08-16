"""
This script makes a query to elasticsearch 
"""
import requests
import pandas as pd
import json

def make_query(
    type,
    integration_method='',
    gene_value='',
    url='http://35.208.172.98/api/'
):
    """
    type: a string (temporarily defining if it's going to be returning a dataset
    or gene dataframe)
    url: a string pointing to the api to make the query
    integration_method: a string. one of: bbknn_point, harmony_point, rna_point, 
    or scanorama_point
    gene_value: a string. one of the gene_ids

    Returns: a dataframe based on the query to the ElasticSearch API
    """
    if type == "umap":
        query = f"""{{
            umap(dataset: "{integration_method}"){{
                cell_id
                cell_type
                umap_1
                umap_2
            }}
        }}"""

        dataset = requests.post(url, data={'query': query})
        df = pd.DataFrame(json.loads(dataset.text)['data']['umap'])

    elif type == "gene":
        query = f"""{{
            expression(gene: "{gene_value}") {{
                cell_id
                normalized_count
            }}
        }}"""

        dataset = requests.post(url, data={'query': query})
        df = pd.DataFrame(json.loads(dataset.text)['data']['expression'])

    elif type == "metadata":
        query = f"""{{
            metadata_point{{
                cell_id
                age
                sex
            }}
        }}"""

        dataset = requests.post(url, data={'query': query})
        df = pd.DataFrame(json.loads(dataset.text)['data']['metadata_point'])


    return df
