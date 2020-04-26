import {createApi, createEffect, createStore, Store} from 'effector';
import {RawExtractedRelation, RelationsFormValues} from './models';
import {Api} from './api';

export const $relationsFormStore: Store<RelationsFormValues> = createStore<RelationsFormValues>({
    id1: '',
    id2: 'MESH:C000657245',
    pmid: '',
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
    }
});

export interface FetchRawExtractedRelationsParams {
    id1: string,
    id2: string,
    pmid: string
}

export const fetchRawExtractedRelations = createEffect<FetchRawExtractedRelationsParams, Array<RawExtractedRelation>>({
    async handler(params) {
        const res = await Api.getRawExtractedRelations(params.id1, params.id2, params.pmid);
        return res.data;
    }
});

export const $rawExtractedRelationsStore: Store<Array<RawExtractedRelation>> = createStore<Array<RawExtractedRelation>>([]);

$rawExtractedRelationsStore
    .on(fetchRawExtractedRelations.done, (state, fetchResult) => fetchResult.result);
