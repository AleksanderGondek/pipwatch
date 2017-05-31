import { async, ComponentFixture, TestBed } from "@angular/core/testing";

import { RequirementsFilesTableComponent } from "./requirements-files-table.component";

describe("RequirementsFilesTableComponent", () => {
  let component: RequirementsFilesTableComponent;
  let fixture: ComponentFixture<RequirementsFilesTableComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RequirementsFilesTableComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RequirementsFilesTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it("should be created", () => {
    expect(component).toBeTruthy();
  });
});
