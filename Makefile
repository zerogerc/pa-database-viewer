COLLECTIONS_DIR = "data/databases"

run_preprocessing:
	PYTHONPATH=. python3 server/tasks/run_preprocessing.py --collections_dir=$(COLLECTIONS_DIR)

run_debug:
	PYTHONPATH=. python3 server/main.py --collections_dir=$(COLLECTIONS_DIR) --debug

run_prod:
	PYTHONPATH=. python3 server/main.py --collections_dir=$(COLLECTIONS_DIR) \
		--index-path="client/build/index.html" \
		--static-dir="client/build/static"

test:
	PYTHONPATH=. python3 -m pytest
