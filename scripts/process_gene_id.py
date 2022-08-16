"""
This script takes a tsv and returns a list of gene_id names. This is meant to 
be temporary until the data is stored better.
"""

import csv

def get_gene_id(file):
    """
    file: the relative path to the file containing gene_id

    returns: a one dimensional list of gene_ids in the format ["gene1",
     "gene2", ...]
    """
    res = []
    with open(file) as f:
        tsv_file = csv.reader(f, delimiter="\t")

        for row in tsv_file:
            res.append(row)

        f.close()

    return res[0]