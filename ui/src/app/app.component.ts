import { Component, OnInit } from "@angular/core";

import { environment } from "../environments/environment";

import { DataBroker } from "./data-brokers/data-broker";
import { Project } from "./data-brokers/entities";
import { ProjectsUpdateService } from "./data-brokers/projectsUpdateService";

@Component({
  selector: "app-root",
  templateUrl: "./app.component.html",
  styleUrls: ["./app.component.css"]
})
export class AppComponent  implements OnInit {
  title = "Hello, from pipwatch-ui!";
  listOfProjects = new Array<Project>();

  constructor(private readonly broker: DataBroker<Project>, private readonly updateService: ProjectsUpdateService) {
  }

  projectUpdate(projectId: number): void {
    this.updateService.triggerUpdate(projectId);
  }

  ngOnInit() {
    this.broker.initialize(environment.pipwatchApiUrl, "projects/", Project);
    this.updateService.initialize(environment.pipwatchApiUrl);

    this.broker.getAll().then(response => {
      this.listOfProjects = response;
    }).catch(error => {});
  }
}
