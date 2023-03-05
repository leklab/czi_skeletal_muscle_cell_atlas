from dash import dcc, html
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc

with open("data/genes.tsv") as gene:
    genes = [line.strip("\n") for line in gene]
    gene.close()

integration_methods = ["Harmony", "BBKNN", "Scanorama"]

staining_methods = [ 
	"All",
	"H&E", 
	"NADH", 
	"SDH", 
	"Gomori", 
	"fast-myosin", 
	"slow-myosin"
]

age_groups = ["All", "0 - 2 yrs", "3 - 5 yrs", "6 - 12 yrs", "13 - 18 yrs"]

sex = ["All", "M", "F"]

def visualization_options ():
	return dbc.Card([
		dbc.ListGroup([
			dbc.ListGroupItem([
				html.Label(['Select a Gene:']),
				html.Div(className='three columns', children=
					dmc.MultiSelect(
						data=[{'label': x, 'value': x} for x in genes],
						value = ["Thoc1"],
						searchable=True,
						limit=10,
						# maxSelectedValues=1,
						clearable = False,
						id='chosen_gene',
					)
				)
			])
		], flush=False)
	], style={"margin-bottom":"2%", "margin-top":"2%"})

def histology_options ():
	return dbc.Card([
		dbc.ListGroup([
			dbc.ListGroupItem([
				html.Label(['Select a Staining Method:']),
				html.Div(className='three columns', children=
					dcc.Dropdown(
						options=[
							{'label': x, 'value': x} for x in staining_methods
						],
						value="All",
						id='chosen_stain',
						clearable=False
					)
				)
			]),
			dbc.ListGroupItem([
				html.Label(['Select Age Group:']),
				html.Div(className='three columns', children=
					dcc.Dropdown(
						options=[
							{'label': x, 'value': x} for x in age_groups
						],
						value="All",
						id='chosen_age',
						clearable=False
					)
				)
			]),
			dbc.ListGroupItem([
				html.Label(['Select Sex:']),
				html.Div(className='three columns', children=
					dcc.Dropdown(
						options=[
							{'label': x, 'value': x} for x in sex
						],
						value="All",
						id='chosen_sex',
						clearable=False
					)
				)
			]),
			dbc.ListGroupItem([
				html.Label(['Images per Row:']),
				html.Div(className="three columns", children=
					dcc.Slider(1, 4, 1, value=3, id='image-slider')
				)
			])
		])
	])