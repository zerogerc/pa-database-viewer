import csv
import logging
from typing import List

from tqdm import tqdm

from server.collection import CollectionData
from server.data.relations import ExtractedRelationEntry
from server.tasks.task import PreprocessTask
from server.utils import open_file

G_LOG = logging.getLogger(__name__)


class CreateRelationsDbTask(PreprocessTask):
    def __init__(self, directory: CollectionData, *, override_previous: bool = False):
        super(CreateRelationsDbTask, self).__init__('create-relations-db', directory,
                                                    override_previous=override_previous)

    def run_preprocessing(self):
        if not self.directory.path_relations_tsv.exists():
            return

        ExtractedRelationEntry.metadata.create_all(self.directory.relations_db.db_engine)
        self.directory.relations_db.delete_all()

        with open_file(self.directory.path_relations_tsv) as f:
            reader = csv.reader(f, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            entries_batch: List[ExtractedRelationEntry] = []
            total_rows = 0
            for row in tqdm(reader):
                total_rows += 1
                name1, id1, group1, name2, id2, group2, r_type, pmid, prob = row
                entries_batch.append(ExtractedRelationEntry(
                    name1=name1, id1=id1, group1=group1,
                    name2=name2, id2=id2, group2=group2,
                    label=r_type, pmid=pmid, prob=prob, in_ctd=0
                ))
                if len(entries_batch) >= 10000:
                    self.directory.relations_db.insert_entries(entries_batch)
                    entries_batch = []

            self.directory.relations_db.insert_entries(entries_batch)
            G_LOG.info(f'Total relations inserted: {total_rows}')
