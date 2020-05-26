from collections import defaultdict, Counter
from typing import Dict, List

from server.collection import CollectionData
from server.data.suggest import SuggestEntry
from server.tasks.task import PreprocessTask


class CreateSuggestDbTask(PreprocessTask):
    def __init__(self, directory: CollectionData, *, override_previous: bool = False):
        super(CreateSuggestDbTask, self).__init__('create-suggest-db', directory, override_previous=override_previous)

    def run_preprocessing(self):
        id2possible_names: Dict[str, Counter] = defaultdict(lambda: Counter())
        for e1, e2 in self.directory.relations_db.get_entity_pairs():
            id2possible_names[e1.id].update({e1.name: 1})
            id2possible_names[e2.id].update({e2.name: 1})

        suggest_db = self.directory.suggest_db
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
