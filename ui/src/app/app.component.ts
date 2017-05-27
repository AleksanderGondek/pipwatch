import { Component, OnInit } from "@angular/core";

import { Tag } from "./data-brokers/entities";
import { DataBroker } from "./data-brokers/data-broker";

@Component({
  selector: "app-root",
  templateUrl: "./app.component.html",
  styleUrls: ["./app.component.css"]
})
export class AppComponent implements OnInit {
    title = "app works!";
    tagsCollection: Tag[];

    private readonly tagsApiBaseUrl = "http://127.0.0.1:8080/api/v1/tags/";

    constructor(private tagsBroker: DataBroker<Tag>) {}

    private loadTags(): void {
        this.tagsBroker.getAll().then(tags => this.tagsCollection = tags);
    }

    ngOnInit(): void {
        this.tagsBroker.initialize(this.tagsApiBaseUrl);
        this.loadTags();
    }
}
