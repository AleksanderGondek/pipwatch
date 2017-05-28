import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";

import { Ng2SmartTableModule, LocalDataSource } from "ng2-smart-table";

@NgModule({
  imports: [
    CommonModule,
    Ng2SmartTableModule,
    LocalDataSource
  ],
  declarations: []
})
export class DataViewersModule { }
