COLLECTIONS_DIR = "data/databases"


install-client-deps:
	cd client && npm install && cd ..

build-client:
	cd client && yarn build && cd ..

install-server-deps:
	python3 -m pip install -r server/reqs.txt

run-server-preprocessing:
	PYTHONPATH=. python3 server/tasks/run_preprocessing.py --collections_dir=$(COLLECTIONS_DIR)

run-server-debug:
	PYTHONPATH=. python3 server/main.py --collections_dir=$(COLLECTIONS_DIR) --debug

run-server-prod:
	PYTHONPATH=. python3 server/main.py --collections_dir=$(COLLECTIONS_DIR) \
		--index-path="client/build/index.html" \
		--static-dir="client/build/static"

test-server:
	PYTHONPATH=. python3 -m pytest
