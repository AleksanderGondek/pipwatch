import { Component, OnInit } from "@angular/core";

import { DataTableHandler } from "../data-brokers/data-table-handler";
import { EntityTable } from "../entity-table/entity-table";
import { Namespace } from "../data-brokers/entities";

@Component({
  selector: "app-namespaces-table",
  templateUrl: "./namespaces-table.component.html",
  styleUrls: ["./namespaces-table.component.css"]
})
export class NamespacesTableComponent extends EntityTable<Namespace> implements OnInit {
    constructor(broker: DataTableHandler<Namespace>) {
        super(broker);
    }

    ngOnInit() {
        this.initialize("http://127.0.0.1:8080/api/v1/namespaces/", Namespace);
    }
}
