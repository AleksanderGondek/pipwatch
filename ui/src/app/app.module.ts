import { BrowserModule } from "@angular/platform-browser";
import { NgModule } from "@angular/core";
import { FormsModule } from "@angular/forms";
import { HttpModule } from "@angular/http";

import { NgbModule} from "@ng-bootstrap/ng-bootstrap";
import { Ng2SmartTableModule } from "ng2-smart-table";

import { TagInputModule } from "ng2-tag-input";
import { BrowserAnimationsModule } from "@angular/platform-browser/animations"; // this is needed!

import { AppComponent } from "./app.component";
import { AppRoutingModule } from "./app-routing.module";

import { ConstantsService } from "./constants.service";

import { DataBrokersModule } from "./data-brokers/data-brokers.module";

import { TagsTableComponent } from "./crud/tags-table/tags-table.component";
import { NamespacesTableComponent } from "./crud/namespaces-table/namespaces-table.component";
import { RequirementsTableComponent } from "./crud/requirements-table/requirements-table.component";
import { RequirementsFilesTableComponent } from "./crud/requirements-files-table/requirements-files-table.component";
import { ProjectsTableComponent } from "./crud/projects-table/projects-table.component";
import { DashboardComponent } from "./dashboard/dashboard.component";
import { TopMenuComponent } from "./top-menu/top-menu.component";
import { HealthComponent } from "./health/health.component";
import { CreditsComponent } from "./credits/credits.component";
import { CrudComponent } from "./crud/crud.component";

import { TagsRowCellRenderComponent } from "./data-brokers/tags-row-render.component";
import { ProjectsTableDetailsComponent } from "./crud/projects-table-details/projects-table-details.component";

@NgModule({
  entryComponents: [TagsRowCellRenderComponent],
  declarations: [
    AppComponent,
    TagsRowCellRenderComponent,
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
    ProjectsTableDetailsComponent,
  ],
  imports: [
    AppRoutingModule,
    TagInputModule,
    BrowserAnimationsModule,
    Ng2SmartTableModule,
    DataBrokersModule,
    NgbModule.forRoot(),
    BrowserModule,
    FormsModule,
    HttpModule
  ],
  providers: [ConstantsService],
  bootstrap: [AppComponent]
})
export class AppModule { }
