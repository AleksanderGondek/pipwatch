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
import { AppFooterComponent } from "./app-footer/app-footer.component";
import { RequirementsFileDetailsComponent } from "./requirements-file-details/requirements-file-details.component";
import { AboutComponent } from "./about/about.component";


@NgModule({
    declarations: [
        AppComponent,
        AppFooterComponent,
        MenuComponent,
        ProjectDetailsComponent,
        ProjectsOverviewComponent,
        RequirementsFileDetailsComponent,
        AboutComponent
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
