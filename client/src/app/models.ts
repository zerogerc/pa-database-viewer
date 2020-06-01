export interface Entity {
    name: string
    id: string
    group: string
}

export interface MergedRelation {
    entity1: Entity
    entity2: Entity
    label: string
    pmids: string[]
    prob: number
}

export interface PmidWithProb {
    pmid: string
    prob: number
}

export interface RelationsFormValues {
    collection: string
    id1: string
    name1: string
    id2: string
    name2: string
    pmid: string
    onlyNovel: boolean
    page: number
}

export interface RelationPapersPageStore {
    head?: Entity
    tail?: Entity
    label?: string
}

export interface EntitySuggestItem {
    id: string
    name: string
}

export interface RTypeCounts {
    rType: string
    counts: number[]
}

export interface EntityIdCount {
    eid: string
    count: number
}

export interface EntityGroupCounts {
    total: number
    relations: number
    top: EntityIdCount[]
}

export interface CollectionStats {
    totalRelations: number
    rTypeCounts: RTypeCounts[]
    totalEntities: number
    chemicals: EntityGroupCounts
    genes: EntityGroupCounts
    diseases: EntityGroupCounts
}
