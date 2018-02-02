import { Component, Input, OnInit } from "@angular/core";
import { ActivatedRoute, ParamMap } from "@angular/router";
import { Location } from "@angular/common";

import "rxjs/add/operator/switchMap";
import { environment } from "environments/environment";

import { DataBroker } from "app/data-brokers/data-broker";
import { Project } from "app/data-brokers/entities";


@Component({
    selector: "app-project-details",
    templateUrl: "./project-details.component.html",
    styleUrls: ["./project-details.component.css"]
})
export class ProjectDetailsComponent implements OnInit {
    @Input() projectDetails: Project;

    constructor(
        private readonly route: ActivatedRoute,
        private readonly broker: DataBroker<Project>,
        private readonly location: Location
    ) { }

    ngOnInit() {
        this.broker.initialize(environment.pipwatchApiUrl, "projects", Project);

        this.route.paramMap.switchMap((params: ParamMap) => this.broker.get(params.get("id")))
        .subscribe(projectDetails => this.projectDetails = projectDetails);
    }

    goBack(): void {
        this.location.back();
    }

}
