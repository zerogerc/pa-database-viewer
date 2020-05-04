import axios, {AxiosInstance, AxiosResponse} from 'axios';
import {RawExtractedRelation} from './models';

export interface FetchRawExtractedRelationsParams {
    id1: string,
    id2: string,
    pmid: string,
    onlyNovel: boolean,
    page: number,
}

export interface FetchRawExtractedRelationsResponse {
    relations: Array<RawExtractedRelation>
    page: number
    totalPages: number
}

export class Api {
    baseUrl: string;
    axiosInstance: AxiosInstance;

    private static _instance: Api;

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

    static fetchRawExtractedRelations(params: FetchRawExtractedRelationsParams):
        Promise<AxiosResponse<FetchRawExtractedRelationsResponse>> {
        return Api.Instance().axiosInstance.get('/api/relations', {
            params: {
                id1: params.id1,
                id2: params.id2,
                pmid: params.pmid,
                only_novel: params.onlyNovel ? 1 : 0,
                page: params.page,
            }
        })
    }
}

