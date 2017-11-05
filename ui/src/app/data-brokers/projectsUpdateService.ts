import { Injectable } from "@angular/core";
import { Headers, Http } from "@angular/http";

import "rxjs/add/operator/toPromise";

import { ProjectUpdateStatus } from "./entities";


@Injectable()
export class ProjectsUpdateService {
    private apiBaseUrl = "";
    private readonly resourceName = "projects-updates/";
    private readonly requestHeaders = new Headers({"Content-Type": "application/json"});

    constructor(private http: Http) { }

    initialize(apiBaseUrl: string): void {
        this.apiBaseUrl = apiBaseUrl;
    }

    getStatus(taskId: string): Promise<ProjectUpdateStatus> {
        return this.http.get(this.apiBaseUrl + this.resourceName + taskId)
            .toPromise()
            .then(response => this.handleResponse(response))
            .catch(this.handleException);
    }

    triggerUpdate(projectId: number): void {
        this.http.post(this.apiBaseUrl + this.resourceName + projectId, null)
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
