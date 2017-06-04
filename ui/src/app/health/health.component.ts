import { Component, OnInit } from "@angular/core";

class Status {
    constructor(public name: string, public details: string, public cssStyle: string) { }
}

class ServiceState {
    constructor(public name: string, public url: string, public description: string, public status: Status) { }
}


@Component({
    selector: "app-health",
    templateUrl: "./health.component.html",
    styleUrls: ["./health.component.css"]
})
export class HealthComponent implements OnInit {
    statuses: Array<ServiceState>;

    constructor() { }

    ngOnInit() {
        this.statuses = this.getStatusReportMock();
    }

    private getStatusReportMock(): Array<ServiceState> {
        return [
            new ServiceState("Pipwatch Ui", "127.0.0.1:4200", "Website - frontend for interacting with Pipwatch",
                new Status("Operational", "", "badge-success")),
            new ServiceState("Pipwatch Api", "127.0.0.1:8080", "Api -  common interface for communicating with Pipwatch",
                new Status("Operational", "", "badge-success")),
            new ServiceState("Redis", "127.0.0.1:4096", "Redis - in-memory data structure store, used as a message broker",
                new Status("Down", "Cannot connect", "badge-danger")),
            new ServiceState("SqlLite", "127.0.0.1:4023", "Database - contains all settings and project state",
                new Status("Operational", "", "badge-success")),
            new ServiceState("Pipwatch Woker", "127.0.0.1:4300", "Worker - processes requirments update requests",
                new Status("Interrupted", "Frequent network interruptions", "badge-warning"))
        ];
    }
}
