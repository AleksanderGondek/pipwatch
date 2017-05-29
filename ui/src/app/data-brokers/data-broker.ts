import { Injectable } from "@angular/core";
import { Headers, Http } from "@angular/http";

import "rxjs/add/operator/toPromise";

import { IEntity } from "./entities";


@Injectable()
export class DataBroker<T extends IEntity> {
    private requestHeaders = new Headers({"Content-Type": "application/json"});
    private cls: {new(jsonObject: any): T};

    public baseUrl = "";

    constructor(private http: Http) { }

    initialize(baseUrl: string, cls: {new(jsonObject: any): T}): void {
        this.baseUrl = baseUrl;
        this.cls = cls;
    }

    getAll(): Promise<T[]> {
        return this.http.get(this.baseUrl)
            .toPromise()
            .then(response => this.handleResponse(response, this.cls))
            .catch(this.handleException);
    }

    private handleResponse(response: any, cls: {new(jsonObject: any): T}): T[] {
        // Enforce response having full typing of T
        const collection = response.json();
        const entityCollection = collection.map(function(item: any) {
            return new cls(item);
        });
        return entityCollection as T[];
    }

    private handleException(exception: any): Promise<any> {
        return Promise.reject(exception.message || exception);
    }
}
