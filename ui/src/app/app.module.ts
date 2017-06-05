import { BrowserModule } from "@angular/platform-browser";
import { NgModule } from "@angular/core";
import { FormsModule } from "@angular/forms";
import { HttpModule } from "@angular/http";

import { NgbModule} from "@ng-bootstrap/ng-bootstrap";
import { Ng2SmartTableModule } from "ng2-smart-table";

import { AppComponent } from "./app.component";
import { AppRoutingModule } from "./app-routing.module";

import { DataBrokersModule } from "./data-brokers/data-brokers.module";

import { TagsTableComponent } from "./tags-table/tags-table.component";
import { NamespacesTableComponent } from "./namespaces-table/namespaces-table.component";
import { RequirementsTableComponent } from "./requirements-table/requirements-table.component";
import { RequirementsFilesTableComponent } from "./requirements-files-table/requirements-files-table.component";
import { ProjectsTableComponent } from "./projects-table/projects-table.component";
import { DashboardComponent } from "./dashboard/dashboard.component";
import { TopMenuComponent } from "./top-menu/top-menu.component";
import { HealthComponent } from "./health/health.component";
import { CreditsComponent } from "./credits/credits.component";
import { CrudComponent } from "./crud/crud.component";

@NgModule({
  declarations: [
    AppComponent,
    NamespacesTableComponent,
    ProjectsTableComponent,
    RequirementsTableComponent,
    RequirementsFilesTableComponent,
    TagsTableComponent,
    DashboardComponent,
    TopMenuComponent,
    HealthComponent,
    CreditsComponent,
    CrudComponent,
  ],
  imports: [
    AppRoutingModule,
    Ng2SmartTableModule,
    DataBrokersModule,
    NgbModule.forRoot(),
    BrowserModule,
    FormsModule,
    HttpModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
