export class TableColumnSetting {
    public type: string;
    public renderComponent: any;

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
