import { Component, OnInit } from "@angular/core";

import { DataBroker } from "./data-brokers/data-broker";
import { Project } from "./data-brokers/entities";
import { ProjectsUpdateService } from "./data-brokers/projectsUpdateService";

@Component({
  selector: "app-root",
  templateUrl: "./app.component.html",
  styleUrls: ["./app.component.css"]
})
export class AppComponent  implements OnInit {
  title = "app works!";
  listOfProjects = new Array<Project>();

  constructor(private readonly broker: DataBroker<Project>, private readonly updateService: ProjectsUpdateService) {
  }

  projectUpdate(projectId: number): void {
    this.updateService.triggerUpdate(projectId);
  }

  ngOnInit() {
    this.broker.initialize("http://localhost:8080/api/v1/projects/", Project);
    this.updateService.initialize("http://localhost:8080/api/v1");
    this.broker.getAll().then(response => {
      this.listOfProjects = response;
    }).catch(error => {});
  }
}
