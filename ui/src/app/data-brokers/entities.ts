export interface IEntity {
    readonly id: number;
}

export class Tag implements IEntity {
    // Cannot declare as: public id: number, public name: string
    // Due to necessary common constructor for Generics (Simplfies things)
    public id: number;
    public name: string;

    constructor(jsonObject: any) {
        this.id = jsonObject.id;
        this.name = jsonObject.name;
    }
}

export class GitRepository implements IEntity {
    public id: number;
    public flavour: string;
    public url: string;
    public upstreamUrl: string;

    public githubApiAddress: string;
    public githubProjectName: string;
    public githubProjectOwner: string;

    public projectId: number;

    constructor(jsonObject: any) {
        this.id = jsonObject.id;
        this.flavour = jsonObject.flavour;
        this.url = jsonObject.url;
        this.upstreamUrl = jsonObject.upstream_url;
        this.githubApiAddress = jsonObject.github_api_address;
        this.githubProjectName = jsonObject.github_project_name;
        this.githubProjectOwner = jsonObject.github_project_owner;

        this.projectId = jsonObject.project_id;
    }
}

export class Requirement implements IEntity {
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
}

export class RequirementsFile implements IEntity {
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
}

export class Project implements IEntity {
    public id: number;
    public name: string;
    public checkCommand: string;
    public namespace: string;

    public namespaceId: number;

    public gitRepository: GitRepository;
    public requirementsFiles: Array<RequirementsFile>;
    public tags: Array<Tag>;


    constructor(jsonObject: any) {
        this.id = jsonObject.id;
        this.name = jsonObject.name;
        this.checkCommand = jsonObject.check_command;
        this.namespace = jsonObject.namespace;

        this.namespaceId = jsonObject.namespace_id;
        this.gitRepository = jsonObject.git_repository;
        this.tags = jsonObject.tags;
        this.requirementsFiles = jsonObject.requirements_files;
    }
}

export class Namespace implements IEntity {
    public id: number;
    public name: string;

    public projects: Array<Project>;

    constructor(jsonObject: any) {
        this.id = jsonObject.id;
        this.name = jsonObject.name;

        this.projects = jsonObject.projects;
    }
}

export class ProjectUpdateStatus {
    public info: string;
    public state: string;
    public taskId: string;

    constructor(jsonObject: any) {
        this.info = jsonObject.info;
        this.state = jsonObject.state;
        this.taskId = jsonObject.taskId;
    }
}
