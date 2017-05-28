import { Injectable } from "@angular/core";
import { Headers, Http } from "@angular/http";

import "rxjs/add/operator/toPromise";

import { Entity } from "./entities";

@Injectable()
export class DataBroker<T extends Entity> {
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
        let collection = response.json();
        let entityCollection = collection.map(function(item: any) {
            return new cls(item);
        });
        return entityCollection as T[];
    }

    private handleException(exception: any): Promise<any> {
        return Promise.reject(exception.message || exception);
    }
}
