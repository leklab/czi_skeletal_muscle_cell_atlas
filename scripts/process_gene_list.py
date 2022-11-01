import pandas as pd

df = pd.read_csv("../data/scMuscle_harmonytypes_plus_phatebins_markers_SupFile2.csv")
df = df[df['avg_logFC'] > 1.25]
df = df[df['p_val_adj'] < 10E-50] 

df.to_csv('../data/filtered_genes.csv', columns = ["gene"], index = False, header = False)