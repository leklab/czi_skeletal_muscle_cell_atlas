from dash import html
import dash_bootstrap_components as dbc

from itertools import islice, chain, repeat

def chunk_pad(it, size, padval=None):
	"""
	it: an iterable object
	size: an int indicating the size of each chunk
	padval: value to pad the final chunk, default = None

	Returns: an iterator that splits the input into chunks

	For more information, see: https://stackoverflow.com/questions/312443/how-do-i-split-a-list-into-equally-sized-chunks
	"""
	it = chain(iter(it), repeat(padval))
	return iter(lambda: tuple(islice(it, size)), (padval,) * size)

def convert(img):
	"""
	img: 

	Returns:
	"""
	if not img:
		return imageSquare("", "")
	return imageSquare(img[0],img[1], img[2] if len(img) > 2 else 0)

def imageSquare(src, alt, num=0):
	"""
	src: source URL of the image to be displayed
	alt: description of image
	num: unique identifier number; default = 0

	Returns: dbc.Col component displaying the image. Returns an empty component
	if empty.
	"""
	return dbc.Col(children = [
		html.Div(className="histology", children = [
			html.Img(
				src=src, 
				width="100%", 
				style = {"cursor": "pointer"}, 
				id = f"enlarge-image-{num}"
			),
			html.Div(
				html.P(alt), 
				style = {
					"textAlign": "center", 
					"padding": "10px 20px"
				}),
			], style = {
				"width":"95%", 
				"backgroundColor" : "white", 
				"boxShadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)", 
				"marginBottom" : "25px"
			}
		)
	]) if src != "" else dbc.Col()

def generate_grid (lst, slider):
	"""
	lst: a list of images to split
	slider: an int indicating number of images per row

	Returns: a Dash component of the grid split into chunks of
	slider elements
	"""
	imageSquares = list(chunk_pad(lst, slider))
	for i in range(len(imageSquares)):
		imageSquares[i] = list(map(convert, imageSquares[i]))

	return [dbc.Row(group) for group in imageSquares]