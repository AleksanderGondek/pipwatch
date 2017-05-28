import { TableColumnSetting, TableColumnsSettings, Tabularizable } from "../data-viewers/tabularizable"

export interface Entity extends Tabularizable {
    readonly id: number;
}

export class Tag implements Entity {
    constructor(public id: number, public name: string) {
    }

    getColumnsSettings(): TableColumnsSettings {
        let settings = new TableColumnsSettings();
        settings["id"] = new TableColumnSetting("Id", false);
        settings["name"] = new TableColumnSetting("Name", false);
        return settings;
    }
}
