import logging
from abc import abstractmethod
from datetime import datetime
from pathlib import Path

from server.collection import CollectionData

G_LOG = logging.getLogger(__name__)


class PreprocessTask:
    def __init__(self, name: str, directory: CollectionData, *, override_previous: bool = False):
        self.directory = directory
        self.name = name
        self.override_previous = override_previous

    def execute(self):
        prefix = f'directory={self.directory.root.name}, task={self.name}'
        if not self.override_previous and self.is_complete:
            G_LOG.info(f'{prefix} | completed before')
            return

        G_LOG.info(f'{prefix} | running preprocessing')
        start_time = datetime.now()
        self.run_preprocessing()
        G_LOG.info(f'{prefix} | time elapsed {datetime.now() - start_time}')

        self.set_is_complete()

    @abstractmethod
    def run_preprocessing(self):
        raise NotImplementedError

    @property
    def is_complete(self) -> bool:
        return self.path_is_complete.exists()

    def set_is_complete(self):
        self.path_is_complete.write_text('OK')

    @property
    def path_is_complete(self) -> Path:
        return self.directory.root / f'.{self.name}.complete'
