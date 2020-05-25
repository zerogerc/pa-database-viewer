from collections import defaultdict, Counter
from pathlib import Path
from typing import Dict, List

from server.db.relations import PaperAnalyzerDatabase
from server.db.suggest import SuggestEntry, SuggestDatabase
from server.tasks.task import PreprocessTask
from server.utils import CollectionData


class CreateSuggestDbTask(PreprocessTask):
    def __init__(self, directory: CollectionData):
        super(CreateSuggestDbTask, self).__init__('create-suggest-db', directory)

    def execute(self):
        if self.is_complete:
            return

        relations_db = PaperAnalyzerDatabase(self.directory.path_relations_db)
        id2possible_names: Dict[str, Counter] = defaultdict(lambda: Counter())
        for e1, e2 in relations_db.get_entity_pairs():
            id2possible_names[e1.id].update({e1.name: 1})
            id2possible_names[e2.id].update({e2.name: 1})

        suggest_db = SuggestDatabase(self.directory.path_suggest_db)
        suggest_db.delete_all()

        entries_batch: List[SuggestEntry] = []
        for med_id, possible_names in id2possible_names.items():
            cname = possible_names.most_common(1)[0][0]
            for name, _ in possible_names.items():
                entries_batch.append(SuggestEntry(
                    id=med_id, name=name, cname=cname
                ))
                if len(entries_batch) >= 1000:
                    suggest_db.insert_entries(entries_batch)
                    entries_batch = []

        suggest_db.insert_entries(entries_batch)

        self.set_is_complete()


def main():
    directory = Path('/Users/Uladzislau.Sazanovich/dev/pa-database-viewer/data/databases/LitCovid')
    create_suggest_task = CreateSuggestDbTask(directory)

    create_suggest_task.execute()


if __name__ == '__main__':
    main()
