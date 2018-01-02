import { TestBed, async } from "@angular/core/testing";

import { AppComponent } from "./app.component";
import { DataBrokersModule } from "./data-brokers/data-brokers.module";

describe("AppComponent", () => {
  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [
        AppComponent
      ],
      imports: [
        DataBrokersModule
      ]
    }).compileComponents();
  }));

  it("should create the app", async(() => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.debugElement.componentInstance;
    expect(app).toBeTruthy();
  }));
});
