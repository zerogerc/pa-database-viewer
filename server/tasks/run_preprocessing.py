import argparse
import logging
from pathlib import Path

from server.collection import read_collections
from server.tasks.calculate_stats import CalculateStatsTask
from server.tasks.create_suggest import CreateSuggestDbTask


def main():
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument('--collections_dir', type=str, required=True)
    parser.add_argument('--override_previous', type=bool, default=False)
    args = parser.parse_args()

    collections = read_collections(Path(args.collections_dir))
    for name, collection_data in collections.items():
        tasks = [
            CreateSuggestDbTask(collection_data, override_previous=args.override_previous),
            CalculateStatsTask(collection_data, override_previous=args.override_previous)
        ]
        for task in tasks:
            task.execute()


if __name__ == '__main__':
    main()
