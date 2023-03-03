"""
This script takes a tsv and returns a list of gene_id names. This is meant to 
be temporary until the data is stored better.
"""

import csv
import pandas as pd

def get_gene_id(file):
    """
    file: the relative path to the file containing gene_id

    Returns: a one dimensional list of gene_ids 
    """
    res = []
    with open(file) as f:
        tsv_file = csv.reader(f, delimiter="\t")

        for row in tsv_file:
            res.append(row)

        f.close()

    return res[0]

def most_frequent():
    """
    Saves a filterd dataframe based on the following:
    - avg_logFC > 1.25
    - p_val_adj < 10E-50
    """
    df = pd.read_csv(
        "../data/scMuscle_harmonytypes_plus_phatebins_markers_SupFile2.csv")
    
    df = df[df['avg_logFC'] > 1.25]
    df = df[df['p_val_adj'] < 10E-50] 

    df.to_csv(
        '../data/filtered_genes.csv', 
        columns = ["gene"], 
        index = False, 
        header = False
    )