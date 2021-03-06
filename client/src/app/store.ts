import {createApi, createStore, Store} from 'effector';
import {RelationPapersPageStore, RelationsFormValues} from './models';
import {
    fetchCollections,
    FetchCollectionsResponse,
    fetchEntitySuggest,
    FetchEntitySuggestResponse,
    fetchRawExtractedRelations,
    FetchRawExtractedRelationsResponse,
    fetchRelationPmidProbs,
    FetchRelationPmidProbsResponse,
    fetchStats,
    FetchStatsResponse,
} from './api';
import {createEvent} from 'effector/effector.cjs';

export const $relationsFormStore: Store<RelationsFormValues> = createStore<RelationsFormValues>({
    collection: '',
    id1: '',
    name1: '',
    id2: 'MESH:C000657245',
    name2: 'COVID-19',
    pmid: '',
    onlyNovel: false,
    page: 0,
});

export const relationsFormApi = createApi($relationsFormStore, {
    setCollection: (form, collection: string) => {
        clearStatsStore();
        clearRawExtractedRelationsStore();
        clearRelationPmidProbsStore();
        return {...form, collection: collection};
    },
    setId1: (form, id1: string) => {
        return {...form, id1: id1};
    },
    setName1: (form, name1: string) => {
        return {...form, name1: name1};
    },
    setId2: (form, id2: string) => {
        return {...form, id2: id2};
    },
    setName2: (form, name2: string) => {
        return {...form, name2: name2};
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

export const clearRawExtractedRelationsStore = createEvent<void>('clear relations');

$rawExtractedRelationsStore
    .on(fetchRawExtractedRelations.done, (state, fetchResult) => fetchResult.result)
    .on(clearRawExtractedRelationsStore, () => {
        return {
            relations: [],
            page: 0,
            totalPages: 0
        }
    });

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

export const $statsStore: Store<FetchStatsResponse> =
    createStore<FetchStatsResponse>({
        stats: {
            totalRelations: 0,
            rTypeCounts: [],
            totalEntities: 0,
            chemicals: {total: 0, relations: 0, top: []},
            genes: {total: 0, relations: 0, top: []},
            diseases: {total: 0, relations: 0, top: []},
        }
    });

export const clearStatsStore = createEvent<void>('clear stats');

$statsStore
    .on(fetchStats.done, (state, fetchResult) => fetchResult.result)
    .on(clearStatsStore, () => {
        return {
            stats: {
                totalRelations: 0,
                rTypeCounts: [],
                totalEntities: 0,
                chemicals: {total: 0, relations: 0, top: []},
                genes: {total: 0, relations: 0, top: []},
                diseases: {total: 0, relations: 0, top: []},
            }
        }
    });

export const $entitySuggestStore: Store<FetchEntitySuggestResponse> =
    createStore<FetchEntitySuggestResponse>({
        suggest: []
    });

export const clearEntitySuggestStore = createEvent<void>('clear entity suggest');

$entitySuggestStore
    .on(fetchEntitySuggest.done, (state, fetchResult) => fetchResult.result)
    .on(clearEntitySuggestStore, () => {
        return {suggest: []};
    });

export const $relationPapersPageStore: Store<RelationPapersPageStore> = createStore<RelationPapersPageStore>({});

export const relationPapersPageStoreApi = createApi($relationPapersPageStore, {
    setStore: (store, values: RelationPapersPageStore) => {
        return values;
    }
});

export const $collectionsStore: Store<FetchCollectionsResponse> =
    createStore<FetchCollectionsResponse>({
        collections: []
    });

$collectionsStore
    .on(fetchCollections.done, (state, fetchResult) => {
        if (fetchResult.result.collections.length === 0) {
            relationsFormApi.setCollection('');
        } else {
            relationsFormApi.setCollection(fetchResult.result.collections[0]);
        }
        return fetchResult.result;
    });
