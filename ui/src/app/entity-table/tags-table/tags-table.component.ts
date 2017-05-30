import { Component, OnInit } from "@angular/core";

import {DataTableHandler} from "../../data-brokers/data-table-handler";
import { EntityTable } from "../entity-table";
import { Tag } from "../../data-brokers/entities";

@Component({
  selector: "app-tags-table",
  templateUrl: "./tags-table.component.html",
  styleUrls: ["./tags-table.component.css"]
})
export class TagsTableComponent extends EntityTable<Tag> implements OnInit {
  constructor(tagsBroker: DataTableHandler<Tag>) {
      super(tagsBroker);
  }

  ngOnInit() {
      this.initialize("http://127.0.0.1:8080/api/v1/tags/", Tag);
  }
}
