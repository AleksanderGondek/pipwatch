import { Component, OnInit } from "@angular/core";

import { Router, NavigationEnd } from "@angular/router";

import { routes } from "../app-routing.module";


class MenuItem {
    constructor(public name:string, public url:string) { }
}


@Component({
  selector: "app-top-menu",
  templateUrl: "./top-menu.component.html",
  styleUrls: ["./top-menu.component.css"]
})
export class TopMenuComponent implements OnInit {
    menuItems: Array<MenuItem> = [];
    currentRoute: string;

    constructor(private _router: Router) {
        _router.events.subscribe((navigationState:NavigationEnd) => this.currentRoute = navigationState.urlAfterRedirects);
        this.getMenuRoutes();
    }

    private getMenuRoutes() {
        // Remove default route from possible options
        let cleanedRoutes: any = routes.slice(1);
        for (let route of cleanedRoutes) {
            let itemName = route.path;
            let itemUrl = `/${itemName}`;

            this.menuItems.push(new MenuItem(itemName, itemUrl));
        }
    }

    ngOnInit() {
    }

}
