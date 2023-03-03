start:
	. venv/bin/activate
	pip3 install -r requirements.txt
	rm -r images/
	python3 web/cell_atlas_main.py