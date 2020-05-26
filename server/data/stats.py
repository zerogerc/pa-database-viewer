from types import SimpleNamespace
from typing import Any, List


class RTypeCounts(SimpleNamespace):
    r_type: str
    counts: List[int]

    def to_json(self):
        return {
            'r_type': self.r_type,
            'counts': self.counts
        }

    @staticmethod
    def from_json(raw: Any):
        return RTypeCounts(**raw)


class RTypesStats(SimpleNamespace):
    counts: List[RTypeCounts]

    def to_json(self):
        return {
            'counts': [c.to_json() for c in self.counts]
        }

    @staticmethod
    def from_json(data: Any):
        return RTypesStats(counts=[RTypeCounts.from_json(r) for r in data['counts']])
