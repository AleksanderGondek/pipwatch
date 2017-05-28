import { Injectable } from "@angular/core";

import { DataBroker } from "../data-brokers/data-broker"
import { Entity } from "../data-brokers/entities"

import { Tabularizable, TableSettings } from "./tabularizable"

@Injectable()
export class DataTableHandler<T extends Entity & Tabularizable> {
    public baseApiUrl: string;
    public settings: TableSettings;

    private entityCollection: T[];
    private cls: {new(jsonObject: any): T};

    constructor(private readonly dataBroker: DataBroker<T>) {
    }

    public initialize(baseApiUrl: string, cls: {new(jsonObject: any): T}): void {
        this.baseApiUrl = baseApiUrl;
        this.cls = cls;

        this.dataBroker.initialize(this.baseApiUrl, this.cls);
        this.getTableSettings();

        this.loadCollection();
    }

    private getTableSettings(): void {
        let columnsSettings = new this.cls({}).getColumnsSettings();
        this.settings = new TableSettings(columnsSettings);
    }

    private loadCollection(): void {
        this.dataBroker.getAll().then(response => this.entityCollection = response);
    }
}
