import axios, {AxiosInstance} from 'axios';
import {PmidWithProb, RawExtractedRelation} from './models';
import {createEffect} from 'effector';

export interface FetchRawExtractedRelationsParams {
    id1: string
    id2: string
    pmid: string
    onlyNovel: number
    page: number
}

export interface FetchRawExtractedRelationsResponse {
    relations: Array<RawExtractedRelation>
    page: number
    totalPages: number
}

export const fetchRawExtractedRelations =
    createEffect<FetchRawExtractedRelationsParams, FetchRawExtractedRelationsResponse>({
        async handler(params: FetchRawExtractedRelationsParams) {
            const res = await Endpoint.Instance().axiosInstance.get('/api/relations', {params: params});
            const rawData = res.data;
            return {
                relations: rawData['relations'].map((raw: any) => {
                    return {
                        head: {name: raw['name1'], id: raw['id1'], group: raw['group1']},
                        tail: {name: raw['name2'], id: raw['id2'], group: raw['group2']},
                        label: raw['label'], prob: raw['prob'], pmids: raw['pmids'],
                    }
                }),
                page: rawData['page'], totalPages: rawData['totalPages']
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

