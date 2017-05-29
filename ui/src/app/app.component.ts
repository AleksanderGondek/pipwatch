import { Component, OnInit } from "@angular/core";

import { Tag } from "./data-brokers/entities";
import { DataTableHandler } from "./data-brokers/data-table-handler";

@Component({
  selector: "app-root",
  templateUrl: "./app.component.html",
  styleUrls: ["./app.component.css"]
})
export class AppComponent implements OnInit {
    private readonly tagsApiBaseUrl = "http://127.0.0.1:8080/api/v1/tags/";

    title = "app works!";

    constructor(private tagsBroker: DataTableHandler<Tag>) {
        this.tagsBroker.baseApiUrl = this.tagsApiBaseUrl;
    }

    ngOnInit(): void {
        this.tagsBroker.initialize(this.tagsApiBaseUrl, Tag);
    }
}
