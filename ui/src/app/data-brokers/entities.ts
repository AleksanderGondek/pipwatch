import { TableColumnSetting, TableColumnsSettings, Tabularizable } from "../data-viewers/tabularizable";

export interface Entity {
    readonly id: number;
}

export class Tag implements Entity, Tabularizable {
    // Cannot declare as: public id: number, public name: string
    // Due to necessary common constructor
    public id: number;
    public name: string;

    constructor(jsonObject: any) {
        this.id = jsonObject.id;
        this.name = jsonObject.name;
    }

    public getColumnsSettings(): TableColumnsSettings {
        const settings = new TableColumnsSettings();
        settings["id"] = new TableColumnSetting("Id", false);
        settings["name"] = new TableColumnSetting("Name", false);
        return settings;
    }
}
