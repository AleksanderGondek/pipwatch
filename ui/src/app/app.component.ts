import { Component, OnInit } from "@angular/core";

import { environment } from "../environments/environment";

import { DataBroker } from "./data-brokers/data-broker";
import { Project } from "./data-brokers/entities";
import { ProjectsUpdateService } from "./data-brokers/projectsUpdateService";
import { prepareProfile } from "selenium-webdriver/firefox";

@Component({
  selector: "app-root",
  templateUrl: "./app.component.html",
})
export class AppComponent  implements OnInit {
    triggeredTasksIds = new Map<number, string>();
    triggeredTasksStatuses = new Map<string, string>();

    listOfProjects = new Array<Project>();

    pipwatchVersion = environment.version;
    currentYear = new Date().getFullYear();

    constructor(private readonly broker: DataBroker<Project>, private readonly updateService: ProjectsUpdateService) {
    }

    projectUpdate(projectId: number): void {
        this.updateService.triggerUpdate(projectId).then(taskId => {
            this.triggeredTasksIds.set(projectId, taskId);
        });
    }

    getTriggeredTaskIdForProject(projectId: number): string {
        return this.triggeredTasksIds.get(projectId);
    }

    checkStatus(taskId: string): void {
        this.updateService.getStatus(taskId).then(projectStatus => {
            this.triggeredTasksStatuses.set(taskId, projectStatus.state);
        });
    }

    ngOnInit() {
        this.broker.initialize(environment.pipwatchApiUrl, "projects/", Project);
        this.updateService.initialize(environment.pipwatchApiUrl);

        this.broker.getAll().then(response => {
            this.listOfProjects = response;
        }).catch(error => {});
    }
}
