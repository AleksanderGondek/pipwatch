import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";

import { Ng2SmartTableModule } from "ng2-smart-table";

import { DataTableHandler } from "./data-table-handler";

import { DataBrokersModule } from "../data-brokers/data-brokers.module";

@NgModule({
  imports: [
    CommonModule,
    Ng2SmartTableModule,
    DataBrokersModule
  ],
  declarations: [],
  providers: [DataTableHandler]
})
export class DataViewersModule { }
