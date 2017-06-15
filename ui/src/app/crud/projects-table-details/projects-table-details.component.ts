import { Component, OnInit } from "@angular/core";

import { Project } from "../../data-brokers/entities";

@Component({
  selector: "app-projects-table-details",
  templateUrl: "./projects-table-details.component.html",
  styleUrls: ["./projects-table-details.component.css"]
})
export class ProjectsTableDetailsComponent implements OnInit {
    public project: Project;

    constructor() {
        this.project = new Project({
            id: 1,
            name: "Swaggerson",
            namespace: "Test Namespace",
            url: "http://www.eu.eu",
            namespaceId: 1,
            tags: ["swag", "boost"],
            requirementsFiles: [],
        });
    }

    ngOnInit() {
    }

}
