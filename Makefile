COLLECTIONS_DIR = "data/databases"

test:
	PYTHONPATH=. python3 -m pytest

run_preprocessing:
	PYTHONPATH=. python3 server/tasks/run_preprocessing.py --collections_dir=$(COLLECTIONS_DIR)

run_debug:
	PYTHONPATH=. python3 server/main.py --collections_dir=$(COLLECTIONS_DIR) --debug
