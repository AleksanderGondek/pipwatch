import { Component, Input, OnInit } from "@angular/core";

import { environment } from "environments/environment";

import { DataBroker } from "app/data-brokers/data-broker";
import { RequirementsFile } from "app/data-brokers/entities";

@Component({
    selector: "app-requirements-file-details",
    templateUrl: "./requirements-file-details.component.html"
})
export class RequirementsFileDetailsComponent implements OnInit {
    isDataLoaded: boolean;
    @Input() requirementsFileId: string;
    requirementsFile: RequirementsFile;


    constructor(private readonly broker: DataBroker<RequirementsFile>) { }

    ngOnInit() {
        this.broker.initialize(environment.pipwatchApiUrl, "requirements-files", RequirementsFile);
        this.broker.get(this.requirementsFileId).then(response => {
            this.requirementsFile = response;
            this.isDataLoaded = true;
        }).catch(error => {});
    }

}
