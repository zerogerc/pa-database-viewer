import {createApi, createEffect, createStore, Store} from 'effector';
import {RelationPapersPageStore, RelationsFormValues} from './models';
import {Api, FetchRawExtractedRelationsResponse} from './api';

export const $relationsFormStore: Store<RelationsFormValues> = createStore<RelationsFormValues>({
    id1: '',
    id2: 'MESH:C000657245', // COVID-19 infection
    pmid: '',
    onlyNovel: false,
    page: 1,
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
    }
});

export const $relationPapersPageStore: Store<RelationPapersPageStore> = createStore<RelationPapersPageStore>({
    pmids: ['12628520']
});

export const relationPapersPageStoreApi = createApi($relationPapersPageStore, {
    setPmids: (store, pmids: string[]) => {
        return {...store, pmids}
    }
});

export const fetchRawExtractedRelations =
    createEffect<RelationsFormValues, FetchRawExtractedRelationsResponse>({
        async handler(values: RelationsFormValues) {
            const res = await Api.fetchRawExtractedRelations({
                id1: values.id1,
                id2: values.id2,
                pmid: values.pmid,
                onlyNovel: values.onlyNovel,
                page: values.page,
            });
            return res.data;
        }
    });

export const $rawExtractedRelationsStore: Store<FetchRawExtractedRelationsResponse> =
    createStore<FetchRawExtractedRelationsResponse>({
        relations: [],
        page: 1,
        totalPages: 0,
    });

$rawExtractedRelationsStore
    .on(fetchRawExtractedRelations.done, (state, fetchResult) => fetchResult.result);
