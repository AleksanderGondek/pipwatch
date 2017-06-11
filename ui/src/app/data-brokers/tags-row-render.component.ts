import { Component, Input, OnInit } from "@angular/core";

import { ViewCell } from "ng2-smart-table";

import { Tag } from "./entities";

@Component({
  template: `
    {{renderValue}}
  `,
})
export class TagsRowCellRenderComponent implements ViewCell, OnInit {
    renderValue: string;

    @Input() value: string | number;
    @Input() rowData: any;

    ngOnInit() {
        const elo: Array<Tag> = this.rowData.tags as Array<Tag>;
        this.renderValue = elo.map(function(item: Tag) {
            return item.name;
        }).join(", ");
    }
}
