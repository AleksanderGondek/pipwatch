import { Component, OnInit } from "@angular/core";

import { Axes, Components, Dataset, Plots, Scales } from "plottable";

@Component({
  selector: "app-dashboard",
  templateUrl: "./dashboard.component.html",
  styleUrls: ["./dashboard.component.css"]
})
export class DashboardComponent implements OnInit {
    chart: Components.Table;

    constructor() { }

    ngOnInit() {
      this.makeBasicChart();
    }

    makeBasicChart(): void {
        const xScale = new Scales.Linear();
        const yScale = new Scales.Linear();

        const xAxis = new Axes.Numeric(xScale, "bottom");
        const yAxis = new Axes.Numeric(yScale, "left");

        const plot = new Plots.Line();

        plot.x(function(d) { return d.x; }, xScale);
        plot.y(function(d) { return d.y; }, yScale);

        const dataset = new Dataset([
          { "x": 0, "y": 1 },
          { "x": 1, "y": 2 },
          { "x": 2, "y": 4 },
          { "x": 3, "y": 8 }
        ]);

        plot.addDataset(dataset);

        this.chart = new Components.Table([
          [yAxis, plot],
          [null, xAxis]
        ]);

        this.chart.renderTo("div#tutorial-result");
    }
}
