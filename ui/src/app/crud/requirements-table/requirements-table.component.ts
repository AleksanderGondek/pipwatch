import { Component, OnInit } from "@angular/core";

import { ConstantsService } from "../../constants.service";
import { DataTableHandler } from "../../data-brokers/data-table-handler";
import { EntityTable } from "../entity-table/entity-table";
import { Requirement } from "../../data-brokers/entities";

@Component({
  selector: "app-requirements-table",
  templateUrl: "./requirements-table.component.html",
  styleUrls: ["./requirements-table.component.css"]
})
export class RequirementsTableComponent extends EntityTable<Requirement> implements OnInit {
    constructor(broker: DataTableHandler<Requirement>, private constants: ConstantsService) {
        super(broker);
    }

    ngOnInit() {
        this.initialize(this.constants.API_URL + "v1/requirements/", Requirement);
    }
  }
