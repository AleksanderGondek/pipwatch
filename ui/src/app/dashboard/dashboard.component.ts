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

    redraw(): void {
        console.log("elo");
    }

    makeBasicChart(): void {
        let xScale = new Scales.Linear();
        let yScale = new Scales.Linear();

        let xAxis = new Axes.Numeric(xScale, "bottom");
        let yAxis = new Axes.Numeric(yScale, "left");

        let plot = new Plots.Line();

        plot.x(function(d) { return d.x; }, xScale);
        plot.y(function(d) { return d.y; }, yScale);

        let dataset = new Dataset([
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
