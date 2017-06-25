import { Component, OnInit } from "@angular/core";

import { ConstantsService } from "../../constants.service";
import { EntityTable } from "../entity-table/entity-table";
import { DataTableHandler } from "../../data-brokers/data-table-handler";
import { Project } from "../../data-brokers/entities";

@Component({
  selector: "app-projects-table",
  templateUrl: "./projects-table.component.html",
  styleUrls: ["./projects-table.component.css"]
})
export class ProjectsTableComponent extends EntityTable<Project> implements OnInit {
    constructor(broker: DataTableHandler<Project>, private constants: ConstantsService) {
        super(broker);
    }

    ngOnInit() {
        this.initialize(this.constants.API_URL + "v1/projects/", Project);
    }
}
