from typing import Any, List

import attr


@attr.s(auto_attribs=True)
class RTypeCounts:
    r_type: str
    counts: List[int]

    @staticmethod
    def from_json(raw: Any):
        return RTypeCounts(**raw)


@attr.s(auto_attribs=True)
class EntityIdCount:
    eid: str
    count: int

    @staticmethod
    def from_json(raw: Any):
        return EntityIdCount(**raw)


@attr.s(auto_attribs=True)
class EntityGroupCounts:
    total: int = attr.Factory(int)
    relations: int = attr.Factory(int)
    top: List[EntityIdCount] = attr.Factory(list)

    @staticmethod
    def from_json(raw: Any):
        return EntityGroupCounts(
            total=raw['total'],
            relations=raw['relations'],
            top=[EntityIdCount.from_json(r) for r in raw['top']]
        )


@attr.s(auto_attribs=True)
class CollectionStats:
    total_relations: int
    r_type_counts: List[RTypeCounts]
    total_entities: int
    chemicals: EntityGroupCounts
    genes: EntityGroupCounts
    diseases: EntityGroupCounts

    @staticmethod
    def from_dict(raw: Any):
        return CollectionStats(
            total_relations=raw['total_relations'],
            total_entities=raw['total_entities'],
            chemicals=EntityGroupCounts.from_json(raw['chemicals']),
            genes=EntityGroupCounts.from_json(raw['genes']),
            diseases=EntityGroupCounts.from_json(raw['diseases']),
            r_type_counts=[RTypeCounts.from_json(r) for r in raw['r_type_counts']]
        )
