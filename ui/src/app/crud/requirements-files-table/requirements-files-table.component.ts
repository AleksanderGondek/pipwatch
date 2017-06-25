import { Component, OnInit } from "@angular/core";

import { ConstantsService } from "../../constants.service";
import { DataTableHandler } from "../../data-brokers/data-table-handler";
import { EntityTable } from "../entity-table/entity-table";
import { RequirementsFile } from "../../data-brokers/entities";

@Component({
  selector: "app-requirements-files-table",
  templateUrl: "./requirements-files-table.component.html",
  styleUrls: ["./requirements-files-table.component.css"]
})
export class RequirementsFilesTableComponent extends EntityTable<RequirementsFile> implements OnInit {
    constructor(broker: DataTableHandler<RequirementsFile>, private constants: ConstantsService) {
        super(broker);
    }

    ngOnInit() {
        this.initialize(this.constants.API_URL + "v1/requirements-files/", RequirementsFile);
    }
}
