import { async, ComponentFixture, TestBed } from "@angular/core/testing";

import { RequirementsFileDetailsComponent } from "./requirements-file-details.component";

describe("RequirementsFileDetailsComponent", () => {
  let component: RequirementsFileDetailsComponent;
  let fixture: ComponentFixture<RequirementsFileDetailsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RequirementsFileDetailsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RequirementsFileDetailsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it("should be created", () => {
    expect(component).toBeTruthy();
  });
});
