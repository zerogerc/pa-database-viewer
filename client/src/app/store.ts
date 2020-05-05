import {createApi, createStore, Store} from 'effector';
import {RelationPapersPageStore, RelationsFormValues} from './models';
import {
    fetchRawExtractedRelations,
    FetchRawExtractedRelationsResponse,
    fetchRelationPmidProbs,
    FetchRelationPmidProbsResponse
} from './api';
import {createEvent} from 'effector/effector.cjs';

export const $relationsFormStore: Store<RelationsFormValues> = createStore<RelationsFormValues>({
    id1: '',
    id2: 'MESH:C000657245', // COVID-19 infection
    pmid: '',
    onlyNovel: false,
    page: 0,
});

export const relationsFormApi = createApi($relationsFormStore, {
    setId1: (form, id1: string) => {
        return {...form, id1: id1};
    },
    setId2: (form, id2: string) => {
        return {...form, id2: id2};
    },
    setPmid: (form, pmid: string) => {
        return {...form, pmid: pmid};
    },
    setOnlyNovel: (form, onlyNovel: boolean) => {
        return {...form, onlyNovel};
    },
    setPage: (form, page: number) => {
        return {...form, page};
    },
    setDefaultPage: (form) => {
        return {...form, page: 0}
    },
});

export const $rawExtractedRelationsStore: Store<FetchRawExtractedRelationsResponse> =
    createStore<FetchRawExtractedRelationsResponse>({
        relations: [],
        page: 0,
        totalPages: 0,
    });

$rawExtractedRelationsStore
    .on(fetchRawExtractedRelations.done, (state, fetchResult) => fetchResult.result);

export const $relationPmidProbsStore: Store<FetchRelationPmidProbsResponse> =
    createStore<FetchRelationPmidProbsResponse>({
        pmidProbs: [],
    });

export const clearRelationPmidProbsStore = createEvent<void>('clear relation pmid probs');

$relationPmidProbsStore
    .on(fetchRelationPmidProbs.done, (state, fetchResult) => fetchResult.result)
    .on(clearRelationPmidProbsStore, () => {
        return {pmidProbs: []};
    });

export const $relationPapersPageStore: Store<RelationPapersPageStore> = createStore<RelationPapersPageStore>({});

export const relationPapersPageStoreApi = createApi($relationPapersPageStore, {
    setStore: (store, values: RelationPapersPageStore) => {
        return values;
    }
});
