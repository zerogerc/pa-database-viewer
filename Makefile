test:
	PYTHONPATH=. python3 -m pytest

run_debug:
	PYTHONPATH=. python3 server/main.py --collection="data/databases/LitCovid" --debug
