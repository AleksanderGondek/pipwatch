import { Component, OnInit } from "@angular/core";

import { Router, NavigationEnd } from "@angular/router";

import { routes } from "../app-routing.module";


class MenuItem {
    constructor(public name: string, public url: string, public nestedItems: Array<MenuItem>) { }

    public isDropdown(): boolean {
        return this.nestedItems && this.nestedItems != null && this.nestedItems.length > 0;
    }
}


@Component({
  selector: "app-top-menu",
  templateUrl: "./top-menu.component.html",
  styleUrls: ["./top-menu.component.css"]
})
export class TopMenuComponent implements OnInit {
    menuItems: Array<MenuItem>;
    currentRoute: string;

    constructor() {
        this.getMenuRoutes();
    }

    private getMenuRoutes(): void {
        this.menuItems = [
            new MenuItem("Dashboard", "/dashboard", null),
            new MenuItem("Projects", "/projects", [
                new MenuItem("Show all", "/projects", null),
                new MenuItem("Create new", "/projects/new", null)
            ]),
            new MenuItem("CRUD", "/crud", [
                new MenuItem("Namespaces", "/crud/namespaces", null),
                new MenuItem("Projects", "/crud/projects", null),
                new MenuItem("Requirements Files", "/crud/requirements-files", null),
                new MenuItem("Requirements", "/crud/requirements", null),
                new MenuItem("Tags", "/crud/tags", null)
            ]),
            new MenuItem("Health", "/health", null),
            new MenuItem("Credits", "/credits", null)
        ];
    }

    ngOnInit() {
    }

}
