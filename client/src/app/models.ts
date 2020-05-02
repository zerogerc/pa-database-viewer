export interface RawExtractedRelation {
    name1: string,
    id1: string,
    group1: string,
    name2: string,
    id2: string,
    group2: string,
    label: string,
    pmid: string,
    prob: number,
}

export interface RelationsFormValues {
    id1: string,
    id2: string,
    pmid: string,
    onlyNovel: boolean,
    page: number,
}
