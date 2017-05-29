import { BrowserModule } from "@angular/platform-browser";
import { NgModule } from "@angular/core";
import { FormsModule } from "@angular/forms";
import { HttpModule } from "@angular/http";

import { NgbModule} from "@ng-bootstrap/ng-bootstrap";
import { Ng2SmartTableModule } from "ng2-smart-table";

import { AppComponent } from "./app.component";

import { DataBrokersModule } from "./data-brokers/data-brokers.module";

@NgModule({
  declarations: [
    AppComponent
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
