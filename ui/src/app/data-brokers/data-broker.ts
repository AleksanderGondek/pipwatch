import { Injectable } from "@angular/core";
import { Headers, Http } from "@angular/http";

import "rxjs/add/operator/toPromise";

import { IEntity } from "./entities";


@Injectable()
export class DataBroker<T extends IEntity> {
    private apiBaseUrl = "";
    private cls: { new(jsonObject: any): T };
    private resourceName = "";
    private readonly requestHeaders = new Headers({ "Content-Type": "application/json" });

    constructor(private http: Http) { }

    initialize(apiBaseUrl: string, resourceName: string, cls: { new(jsonObject: any): T }): void {
        this.apiBaseUrl = apiBaseUrl;
        this.resourceName = resourceName;
        this.cls = cls;
    }

    getAll(): Promise<T[]> {
        return this.http.get(this.apiBaseUrl + this.resourceName)
            .toPromise()
            .then(response => this.handleResponseAsCollection(response, this.cls))
            .catch(this.handleException);
    }

    get(id: string): Promise<T> {
        return this.http.get(this.apiBaseUrl + this.resourceName + "/" + id)
            .toPromise()
            .then(response => this.handleResponseForItem(response, this.cls))
            .catch(this.handleException);
    }

    private handleResponseForItem(response: any, cls: { new(jsonObject: any): T}): T {
        // Enforce response having full typing of T
        const itemJson = response.json();
        const item = new cls(itemJson);
        return item as T;
    }

    private handleResponseAsCollection(response: any, cls: { new(jsonObject: any): T }): T[] {
        // Enforce response having full typing of T
        const collection = response.json();
        const entityCollection = collection.map(function (item: any) {
            return new cls(item);
        });
        return entityCollection as T[];
    }

    private handleException(exception: any): Promise<any> {
        return Promise.reject(exception.message || exception);
    }
}
