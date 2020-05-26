COLLECTIONS_DIR = "data/databases"

init:
	cd client && yarn build && cd .. &&\
	python3 -m pip install -r server/reqs.txt

run-preprocessing:
	PYTHONPATH=. python3 server/tasks/run_preprocessing.py --collections_dir=$(COLLECTIONS_DIR)

run-debug:
	PYTHONPATH=. python3 server/main.py --collections_dir=$(COLLECTIONS_DIR) --debug

run-prod:
	PYTHONPATH=. python3 server/main.py --collections_dir=$(COLLECTIONS_DIR) \
		--index-path="client/build/index.html" \
		--static-dir="client/build/static"

test:
	PYTHONPATH=. python3 -m pytest
