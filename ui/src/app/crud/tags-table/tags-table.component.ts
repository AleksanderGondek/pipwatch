import { Component, OnInit } from "@angular/core";

import { ConstantsService } from "../../constants.service";
import { DataTableHandler } from "../../data-brokers/data-table-handler";
import { EntityTable } from "../entity-table/entity-table";
import { Tag } from "../../data-brokers/entities";

@Component({
  selector: "app-tags-table",
  templateUrl: "./tags-table.component.html",
  styleUrls: ["./tags-table.component.css"]
})
export class TagsTableComponent extends EntityTable<Tag> implements OnInit {
  constructor(broker: DataTableHandler<Tag>, constants: ConstantsService) {
      super(broker);
  }

  ngOnInit() {
      this.initialize(ConstantsService.API_URL + "v1/tags/", Tag);
  }
}
