import { Injectable } from "@angular/core";
import { Headers, Http } from "@angular/http";

import "rxjs/add/operator/toPromise";

import { Entity } from "./entities";

@Injectable()
export class DataBroker<T extends Entity> {
    private requestHeaders = new Headers({"Content-Type": "application/json"});

    public baseUrl = "";

    constructor(private http: Http) { }

    initialize(baseUrl: string): void {
        this.baseUrl = baseUrl;
    }

    getAll(): Promise<T[]> {
        return this.http.get(this.baseUrl)
            .toPromise()
            .then(response => response.json() as T[])
            .catch(this.handleException);
    }

    private handleException(exception: any): Promise<any> {
        return Promise.reject(exception.message || exception);
    }
}
