import { Component, OnInit } from "@angular/core";

import { environment } from "environments/environment";

import { DataBroker } from "app/data-brokers/data-broker";
import { Project } from "app/data-brokers/entities";
import { ProjectsUpdateService } from "app/data-brokers/projectsUpdateService";

@Component({
  selector: "app-projects-overview",
  templateUrl: "./projects-overview.component.html"
})
export class ProjectsOverviewComponent implements OnInit {
  triggeredTasksIds = new Map<number, string>();
  triggeredTasksStatuses = new Map<string, string>();

  listOfProjects = new Array<Project>();

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
