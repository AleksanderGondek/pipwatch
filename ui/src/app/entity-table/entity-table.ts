import { DataTableHandler } from "../data-brokers/data-table-handler";
import { IEntity } from "../data-brokers/entities";
import { ITabularizable } from "../data-brokers/tableEntities";

export abstract class EntityTable<T extends IEntity & ITabularizable> {
    private apiBaseUrl: string;
    private cls: {new(jsonObject: any): T};

    constructor(protected broker: DataTableHandler<T>) {
    }

    protected initialize(baseUrl: string, cls: {new(jsonObject: any): T}): void {
        this.apiBaseUrl = baseUrl;
        this.cls = cls;

        this.broker.initialize(this.apiBaseUrl, this.cls);
    }
}
