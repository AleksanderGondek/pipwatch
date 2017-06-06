import { Component, OnInit } from "@angular/core";

import { EntityTable } from "../entity-table/entity-table";
import { DataTableHandler } from "../../data-brokers/data-table-handler";
import { Project } from "../../data-brokers/entities";

@Component({
  selector: "app-projects-table",
  templateUrl: "./projects-table.component.html",
  styleUrls: ["./projects-table.component.css"]
})
export class ProjectsTableComponent extends EntityTable<Project> implements OnInit {
    constructor(broker: DataTableHandler<Project>) {
        super(broker);
    }

    ngOnInit() {
        this.initialize("http://127.0.0.1:8080/api/v1/projects/", Project);
    }
}
