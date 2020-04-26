import axios, {AxiosInstance, AxiosResponse} from 'axios';
import {RawExtractedRelation} from './models';

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

    static getRawExtractedRelations(id1: string, id2: string, pmid: string,
                                    onlyNovel: boolean): Promise<AxiosResponse<Array<RawExtractedRelation>>> {
        return Api.Instance().axiosInstance.get('/relations', {
            params: {
                id1: id1,
                id2: id2,
                pmid: pmid,
                only_novel: onlyNovel ? 1 : 0,
            }
        })
    }
}

