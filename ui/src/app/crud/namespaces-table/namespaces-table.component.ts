import { Component, OnInit } from "@angular/core";

import { ConstantsService } from "../../constants.service";
import { DataTableHandler } from "../../data-brokers/data-table-handler";
import { EntityTable } from "../entity-table/entity-table";
import { Namespace } from "../../data-brokers/entities";

@Component({
  selector: "app-namespaces-table",
  templateUrl: "./namespaces-table.component.html",
  styleUrls: ["./namespaces-table.component.css"]
})
export class NamespacesTableComponent extends EntityTable<Namespace> implements OnInit {
    constructor(broker: DataTableHandler<Namespace>, private constants: ConstantsService) {
        super(broker);
    }

    ngOnInit() {
        this.initialize(this.constants.API_URL + "v1/namespaces/", Namespace);
    }
}
