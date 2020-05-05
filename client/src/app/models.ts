export interface Entity {
    name: string
    id: string
    group: string
}

export interface RawExtractedRelation {
    head: Entity
    tail: Entity
    label: string
    pmids: string[]
    prob: number
}

export interface PmidWithProb {
    pmid: string
    prob: number
}

export interface RelationsFormValues {
    id1: string
    id2: string
    pmid: string
    onlyNovel: boolean
    page: number
}

export interface RelationPapersPageStore {
    head?: Entity
    tail?: Entity
    label?: string
}
