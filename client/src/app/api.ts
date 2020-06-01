import axios, {AxiosInstance} from 'axios';
import {CollectionStats, EntitySuggestItem, MergedRelation, PmidWithProb} from './models';
import {createEffect} from 'effector';

export interface FetchCollectionsParams {
}

export interface FetchCollectionsResponse {
    collections: string[]
}

export const fetchCollections =
    createEffect<FetchCollectionsParams, FetchCollectionsResponse>({
        async handler(params: FetchCollectionsParams) {
            const res = await Endpoint.Instance().axiosInstance.get('/api/collections', {params: params});
            return res.data;
        }
    });

export interface FetchRawExtractedRelationsParams {
    collection: string
    id1: string
    id2: string
    pmid: string
    onlyNovel: number
    page: number
}

export interface FetchRawExtractedRelationsResponse {
    relations: Array<MergedRelation>
    page: number
    totalPages: number
}

export const fetchRawExtractedRelations =
    createEffect<FetchRawExtractedRelationsParams, FetchRawExtractedRelationsResponse>({
        async handler(params: FetchRawExtractedRelationsParams) {
            const res = await Endpoint.Instance().axiosInstance.get('/api/relations', {params: params});
            const rawData = res.data;
            return {
                relations: rawData['relations'],
                page: rawData['page'],
                totalPages: rawData['totalPages']
            }
        }
    });

export interface FetchRelationPmidProbsParams {
    id1: string
    id2: string
    label: string
    pmids: string[]
}

export interface FetchRelationPmidProbsResponse {
    pmidProbs: PmidWithProb[]
}

export const fetchRelationPmidProbs =
    createEffect<FetchRelationPmidProbsParams, FetchRelationPmidProbsResponse>({
        async handler(params: FetchRelationPmidProbsParams) {
            const res = await Endpoint.Instance().axiosInstance.post('/api/relation-pmids', params);
            return res.data;
        }
    });

export interface FetchStatsParams {
    collection: string
}

export interface FetchStatsResponse {
    stats: CollectionStats
}

export const fetchStats =
    createEffect<FetchStatsParams, FetchStatsResponse>({
        async handler(params: FetchStatsParams) {
            const res = await Endpoint.Instance().axiosInstance.get('/api/stats', {params: params});
            const rawData = res.data['stats'];

            const stats: CollectionStats = {
                totalRelations: rawData['total_relations'],
                rTypeCounts: rawData['r_type_counts'].map((raw: any) => {
                    return {rType: raw['r_type'], counts: raw['counts']};
                }),
                totalEntities: rawData['total_entities'],
                chemicals: rawData['chemicals'],
                genes: rawData['genes'],
                diseases: rawData['diseases']
            };
            return {stats: stats}
        }
    });

export interface FetchEntitySuggestParams {
    collection: string,
    query: string
}

export interface FetchEntitySuggestResponse {
    suggest: EntitySuggestItem[]
}

export const fetchEntitySuggest =
    createEffect<FetchEntitySuggestParams, FetchEntitySuggestResponse>({
        async handler(params: FetchEntitySuggestParams) {
            const res = await Endpoint.Instance().axiosInstance.get('/api/suggest', {params: params});
            return res.data;
        }
    });

export class Endpoint {
    baseUrl: string;
    axiosInstance: AxiosInstance;

    private static _instance: Endpoint;

    constructor() {
        if (process.env.NODE_ENV !== "production") {
            this.baseUrl = `${window.location.protocol}//localhost:8888`;
        } else {
            this.baseUrl = `${window.location.protocol}//${window.location.host}`;
        }
        this.axiosInstance = axios.create({baseURL: this.baseUrl})
    }

    public static Instance() {
        if (!this._instance) {
            this._instance = new this();
        }
        return this._instance;
    }
}

