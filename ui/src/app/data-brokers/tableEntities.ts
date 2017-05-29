export class TableColumnSetting {
    constructor(public title: string, public filter: boolean) { }
}

export class TableColumnsSettings {
    [index: string]: TableColumnSetting
}

export class TableSettings {
    constructor(public columns: TableColumnsSettings) { }
}

export interface ITabularizable {
    getColumnsSettings(): TableColumnsSettings;
}
