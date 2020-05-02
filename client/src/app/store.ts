import {createApi, createEffect, createStore, Store} from 'effector';
import {RelationsFormValues} from './models';
import {Api, FetchRawExtractedRelationsParams, FetchRawExtractedRelationsResponse} from './api';

export const $relationsFormStore: Store<RelationsFormValues> = createStore<RelationsFormValues>({
    id1: '',
    id2: 'MESH:C000657245', // COVID-19
    pmid: '',
    onlyNovel: false,
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
    }
});

export const fetchRawExtractedRelations =
    createEffect<FetchRawExtractedRelationsParams, FetchRawExtractedRelationsResponse>({
        async handler(params) {
            const res = await Api.fetchRawExtractedRelations(params);
            return res.data;
        }
    });

export const $rawExtractedRelationsStore: Store<FetchRawExtractedRelationsResponse> =
    createStore<FetchRawExtractedRelationsResponse>({
        relations: [],
        page: 0,
        totalPages: 0,
    });

$rawExtractedRelationsStore
    .on(fetchRawExtractedRelations.done, (state, fetchResult) => fetchResult.result);
