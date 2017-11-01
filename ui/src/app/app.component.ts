import { Component, OnInit } from "@angular/core";

import { DataBroker } from "./data-brokers/data-broker";
import { Project } from "./data-brokers/entities";

@Component({
  selector: "app-root",
  templateUrl: "./app.component.html",
  styleUrls: ["./app.component.css"]
})
export class AppComponent  implements OnInit {
  title = "app works!";
  listOfProjects = new Array<Project>();
  constructor(private readonly broker: DataBroker<Project>) {
  }

  ngOnInit() {
    this.broker.initialize("http://localhost:8080/api/v1/projects/", Project);
    this.broker.getAll().then(response => {
      this.listOfProjects = response;
    }).catch(error => {});
  }
}
