import { Injectable } from "@angular/core";
import { Headers, Http } from "@angular/http";

import "rxjs/add/operator/toPromise";

import { ProjectUpdateStatus } from "./entities";


@Injectable()
export class ProjectsUpdateService {
    private requestHeaders = new Headers({"Content-Type": "application/json"});
    private baseUrl = "";

    constructor(private http: Http) { }

    initialize(baseUrl: string): void {
        this.baseUrl = baseUrl;
    }

    getStatus(taskId: string): Promise<ProjectUpdateStatus> {
        return this.http.get(this.baseUrl + "/projects-updates/" + taskId)
            .toPromise()
            .then(response => this.handleResponse(response))
            .catch(this.handleException);
    }

    triggerUpdate(projectId: number): void {
        this.http.post(this.baseUrl + "/projects-updates/" + projectId, null)
            .toPromise()
            .then(response => {})
            .catch(this.handleException);
    }

    private handleResponse(response: any): ProjectUpdateStatus {
        const rawStatusObject = response.json();
        return new ProjectUpdateStatus(rawStatusObject);
    }

    private handleException(exception: any): Promise<any> {
        return Promise.reject(exception.message || exception);
    }
}
