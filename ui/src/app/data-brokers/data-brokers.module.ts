import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { HttpModule } from "@angular/http";

import { DataBroker } from "./data-broker";
import { ProjectsUpdateService } from "./projectsUpdateService";


@NgModule({
  imports: [
    CommonModule,
    HttpModule
  ],
  declarations: [],
  providers: [DataBroker, ProjectsUpdateService]
})
export class DataBrokersModule { }
