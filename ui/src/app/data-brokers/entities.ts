import { ITabularizable, TableColumnSetting, TableColumnsSettings } from "./tableEntities";

export interface IEntity {
    readonly id: number;
}

export class Tag implements IEntity, ITabularizable {
    // Cannot declare as: public id: number, public name: string
    // Due to necessary common constructor for Generics (Simplfies things)
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

export class Requirement implements IEntity, ITabularizable {
    public id: number;
    public name: string;
    public currentVersion: string;
    public desiredVersion: string;
    public status: string;

    public requirementsFileId: number;

    constructor(jsonObject: any) {
        this.id = jsonObject.id;
        this.name = jsonObject.name;
        this.currentVersion = jsonObject.current_version;
        this.desiredVersion = jsonObject.desiredVersion;
        this.status = jsonObject.status;

        this.requirementsFileId = jsonObject.requirements_file_id;
    }

    public getColumnsSettings(): TableColumnsSettings {
        const settings = new TableColumnsSettings();
        settings["id"] = new TableColumnSetting("Id", false);
        settings["name"] = new TableColumnSetting("Name", false);
        settings["currentVersion"] = new TableColumnSetting("Current Version", false);
        settings["desiredVersion"] = new TableColumnSetting("Desired Version", false);
        settings["status"] = new TableColumnSetting("Status", false);

        settings["requirementsFileId"] = new TableColumnSetting("Requirements File Id", false);
        return settings;
    }
}

export class RequirementsFile implements IEntity, ITabularizable {
    public id: number;
    public fullPath: string;
    public status: string;

    public projectId: number;
    public requirements: Array<Requirement>;

    constructor(jsonObject: any) {
        this.id = jsonObject.id;
        this.fullPath = jsonObject.full_path;
        this.status = jsonObject.status;

        this.projectId = jsonObject.project_id;
        this.requirements = jsonObject.requirements;
    }

    public getColumnsSettings(): TableColumnsSettings {
        const settings = new TableColumnsSettings();
        settings["id"] = new TableColumnSetting("Id", false);
        settings["fullPath"] = new TableColumnSetting("Full Path", false);
        settings["status"] = new TableColumnSetting("Status", false);

        settings["projectId"] = new TableColumnSetting("Project Id", false);
        settings["requirements"] = new TableColumnSetting("Requirements", false);
        return settings;
    }
}

export class Project implements IEntity, ITabularizable {
    public id: number;
    public name: string;
    public url: string;

    public namespaceId: number;
    public tags: Array<Tag>;
    public requirementsFiles: Array<RequirementsFile>;

    constructor(jsonObject: any) {
        this.id = jsonObject.id;
        this.name = jsonObject.name;
        this.url = jsonObject.url;

        this.namespaceId = jsonObject.namespace_id;
        this.tags = jsonObject.tags;
        this.requirementsFiles = jsonObject.requirements_files;
    }

    public getColumnsSettings(): TableColumnsSettings {
        const settings = new TableColumnsSettings();
        settings["id"] = new TableColumnSetting("Id", false);
        settings["name"] = new TableColumnSetting("Name", false);
        settings["url"] = new TableColumnSetting("Url", false);

        settings["namespaceId"] = new TableColumnSetting("Namespace Id", false);
        settings["tags"] = new TableColumnSetting("Tags", false);
        settings["requirementsFiles"] = new TableColumnSetting("Requirements Files", false);
        return settings;
    }
}

export class Namespace implements IEntity, ITabularizable {
    public id: number;
    public name: string;

    public projects: Array<Project>;

    constructor(jsonObject: any) {
        this.id = jsonObject.id;
        this.name = jsonObject.name;

        this.projects = jsonObject.projects;
    }

    public getColumnsSettings(): TableColumnsSettings {
        const settings = new TableColumnsSettings();
        settings["id"] = new TableColumnSetting("Id", false);
        settings["name"] = new TableColumnSetting("Name", false);

        settings["projects"] = new TableColumnSetting("Projects", false);
        return settings;
    }
}
