import { BrowserModule } from "@angular/platform-browser";
import { NgModule } from "@angular/core";
import { FormsModule } from "@angular/forms";
import { HttpModule } from "@angular/http";

import { NgbModule} from "@ng-bootstrap/ng-bootstrap";
import { Ng2SmartTableModule } from "ng2-smart-table";

import { AppComponent } from "./app.component";

import { DataBrokersModule } from "./data-brokers/data-brokers.module";
import { TagsTableComponent } from "./entity-table/tags-table/tags-table.component";
import { NamespacesTableComponent } from "./entity-table/namespaces-table/namespaces-table.component";
import { RequirementsTableComponent } from "./entity-table/requirements-table/requirements-table.component";
import { RequirementsFilesTableComponent } from "./entity-table/requirements-files-table/requirements-files-table.component";
import { ProjectsTableComponent } from "./entity-table/projects-table/projects-table.component";

@NgModule({
  declarations: [
    AppComponent,
    TagsTableComponent,
    NamespacesTableComponent,
    RequirementsTableComponent,
    RequirementsFilesTableComponent,
    ProjectsTableComponent
  ],
  imports: [
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
