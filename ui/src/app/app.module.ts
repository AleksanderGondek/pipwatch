import { BrowserModule } from "@angular/platform-browser";
import { NgModule } from "@angular/core";
import { FormsModule } from "@angular/forms";
import { HttpModule } from "@angular/http";

import { AppComponent } from "./app.component";
import { AppRouting } from "./app-routing.module";

import { DataBrokersModule } from "./data-brokers/data-brokers.module";
import { MenuComponent } from "./top-menu/menu.component";
import { ProjectDetailsComponent } from "./project-details/project-details.component";
import { ProjectsOverviewComponent } from "./projects-overview/projects-overview.component";


@NgModule({
    declarations: [
        AppComponent,
        MenuComponent,
        ProjectDetailsComponent,
        ProjectsOverviewComponent
    ],
    imports: [
        BrowserModule,
        DataBrokersModule,
        FormsModule,
        HttpModule,
        AppRouting
    ],
    providers: [],
    bootstrap: [AppComponent]
})
export class AppModule { }
