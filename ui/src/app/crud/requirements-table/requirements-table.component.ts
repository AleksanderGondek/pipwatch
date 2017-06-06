import { Component, OnInit } from "@angular/core";

import { DataTableHandler } from "../../data-brokers/data-table-handler";
import { EntityTable } from "../entity-table/entity-table";
import { Requirement } from "../../data-brokers/entities";

@Component({
  selector: "app-requirements-table",
  templateUrl: "./requirements-table.component.html",
  styleUrls: ["./requirements-table.component.css"]
})
export class RequirementsTableComponent extends EntityTable<Requirement> implements OnInit {
    constructor(broker: DataTableHandler<Requirement>) {
        super(broker);
    }

    ngOnInit() {
        this.initialize("http://127.0.0.1:8080/api/v1/requirements/", Requirement);
    }
  }
