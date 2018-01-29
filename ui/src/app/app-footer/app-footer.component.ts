import { Component, OnInit } from "@angular/core";

import { environment } from "environments/environment";

@Component({
  selector: "app-footer",
  templateUrl: "./app-footer.component.html"
})
export class AppFooterComponent implements OnInit {
  pipwatchVersion = environment.version;
  currentYear = new Date().getFullYear();

  constructor() { }

  ngOnInit() {
  }

}
