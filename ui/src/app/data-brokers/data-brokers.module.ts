import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { HttpModule } from "@angular/http";

import { DataBroker } from "./data-broker";
import { DataTableHandler } from "./data-table-handler";

@NgModule({
  imports: [
    CommonModule,
    HttpModule
  ],
  declarations: [],
  providers: [DataBroker, DataTableHandler]
})
export class DataBrokersModule { }
