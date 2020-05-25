test:
	PYTHONPATH=. python3 -m pytest

run_debug:
	PYTHONPATH=. python3 server/main.py --collections_dir="data/databases" --debug
