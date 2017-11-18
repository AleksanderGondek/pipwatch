import { BrowserModule } from "@angular/platform-browser";
import { NgModule } from "@angular/core";
import { FormsModule } from "@angular/forms";
import { HttpModule } from "@angular/http";

import { AppComponent } from "./app.component";

import { DataBrokersModule } from "./data-brokers/data-brokers.module";
import { MenuComponent } from "./top-menu/menu.component";


@NgModule({
    declarations: [
        AppComponent, MenuComponent
    ],
    imports: [
        BrowserModule,
        DataBrokersModule,
        FormsModule,
        HttpModule
    ],
    providers: [],
    bootstrap: [AppComponent]
})
export class AppModule { }
