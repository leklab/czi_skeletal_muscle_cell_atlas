from dash import dcc, html
import dash_bootstrap_components as dbc

# Options
with open("data/filtered_genes.csv") as gene:
    common_genes = [line.strip("\n") for line in gene]
    gene.close()

# genes = get_gene_id("gene_names.tsv")
with open("data/genes.tsv") as gene:
    genes = [line.strip("\n") for line in gene]
    gene.close()

metadata_feature = ["source", "sample", "chemistry", "injury days", "injury agent", "age", "type",
                    "tissue", "mouse strain", "sex", "mice per sample", "sequencing instrument"]
integration_methods = ["BBKNN", "Harmony", "Scanorama"]
staining_methods = ["H&E", "NADH", "SDH"]
age_groups = ["0 - 2 yrs", "3 - 5 yrs", "6 - 12 yrs", "13 - 18 yrs"]

def visualization_options ():
	return dbc.Card([
            dbc.ListGroup([
                dbc.ListGroupItem([
                    html.Label(['Select a Gene (fast): ']),
                    html.Div(className='three columns', children=dcc.Dropdown(
                        options=[
                            {'label': x, 'value': x} for x in common_genes
                        ],
                        value="Pi16",
                        id='chosen_gene',
                        clearable=False
                    ))
                ]),
                dbc.ListGroupItem([
                    html.Label(['Select a Gene (slow): ']),
                    html.Div(className='three columns', children=dcc.Dropdown(
                        options=[
                            {'label': x, 'value': x} for x in genes
                        ],
                        value="Thoc1",
                        id='chosen_gene',
                        clearable=False
                    ))
                ]),
                dbc.ListGroupItem([
                    html.Label(['Select a Dataset:']),
                    html.Div(className='three columns', children=dcc.Dropdown(
                        options=[
                            {'label': x, 'value': x.lower()} for x in integration_methods
                        ],
                        value="bbknn",
                        id='chosen_dataset',
                        clearable=False
                    ))
                ]),
                dbc.ListGroupItem([
                    html.Label(['Select a Feature: ']),
                    html.Div(className='three columns', children=dcc.Dropdown(
                        options=[
                            {'label': x, 'value': x} for x in metadata_feature
                        ],
                        value="source",
                        id='chosen_feature',
                        clearable=False
                    ))
                ])
            ], flush=False)
        ])

def histology_options ():
	return dbc.Card([
				dbc.ListGroup([
					dbc.ListGroupItem([
						html.Label(['Select a Staining Method:']),
						html.Div(className='three columns', children=dcc.Dropdown(
							options=[
								{'label': x, 'value': x.lower()} for x in staining_methods
							],
							value="h&e",
							id='chosen_stain',
							clearable=False
						))
					]),
					dbc.ListGroupItem([
						html.Label(['Select Age Group:']),
						html.Div(className='three columns', children=dcc.Dropdown(
							options=[
								{'label': x, 'value': x.lower()} for x in age_groups
							],
							value="0 - 2 yrs",
							id='chosen_stain',
							clearable=False
						))
					]),
					dbc.ListGroupItem([
						html.Label(['Select Sex:']),
						html.Div(className='three columns', children=dcc.Dropdown(
							options=[
								{'label': 'Male', 'value': 'male'},
								{'label': 'Female', 'value': 'female'}
							],
							value="male",
							id='chosen_stain',
							clearable=False
						))
					])
				])
			])

def metadata_options ():
	return dbc.Card([
				dbc.ListGroup([
					dbc.ListGroupItem([
						html.Label(['Select a Dataset:']),
						html.Div(className='three columns', children=dcc.Dropdown(
							options=[
								{'label': x, 'value': x.lower()} for x in integration_methods
							],
							value="bbknn",
							id='chosen_dataset',
							clearable=False
						))
					]),
					dbc.ListGroupItem([
						html.Label(['Select a Sex: ']),
						html.Div(className='three columns', children=dcc.Dropdown(
							options=[
								{'label': 'Male', 'value': 'M'},
								{'label': 'Female', 'value': 'F'},
							],
							value= 'M',
							id='chosen_sex',
							clearable=False
						))
					]),
					dbc.ListGroupItem([
						html.Label(['Select an Age Group: ']),
						html.Div(className='three columns', children=dcc.Dropdown(
							options=[
								{'label': x, 'value' : x } for x in age_groups
							],
							value= "0 - 2 yrs",
							id='chosen_age',
							clearable=False
						))
					]),
					dbc.ListGroupItem([
						html.Label(['Select an Ethnicity: ']),
						html.Div(className='three columns', children=dcc.Dropdown(
							options=[
								{'label': 'European', 'value': 'eu'},
								{'label': 'Non-European', 'value': 'neu'},
							],
							value= "eu",
							id='chosen_ethnicity',
							clearable=False
						))
					]),
					dbc.ListGroupItem([
						html.Label(['Select a Donor: ']),
						html.Div(className='three columns', children=dcc.Dropdown(
							options=[
								{'label': 'X', 'value': 'x'},
								{'label': 'Y', 'value': 'y'},
							],
							value= "x",
							id='chosen_donor',
							clearable=False
						))
					]),
				], flush = False)
			])