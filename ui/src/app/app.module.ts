import { BrowserModule } from "@angular/platform-browser";
import { NgModule } from "@angular/core";
import { FormsModule } from "@angular/forms";
import { HttpModule } from "@angular/http";

import { NgbModule} from "@ng-bootstrap/ng-bootstrap";

import { AppComponent } from "./app.component";

import { DataBrokersModule } from "./data-brokers/data-brokers.module";
import { DataViewersModule } from "./data-viewers/data-viewers.module";

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    DataBrokersModule,
    DataViewersModule,
    NgbModule.forRoot(),
    BrowserModule,
    FormsModule,
    HttpModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
