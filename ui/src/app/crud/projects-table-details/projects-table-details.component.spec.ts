import { async, ComponentFixture, TestBed } from "@angular/core/testing";

import { ProjectsTableDetailsComponent } from "./projects-table-details.component";

describe("ProjectsTableDetailsComponent", () => {
  let component: ProjectsTableDetailsComponent;
  let fixture: ComponentFixture<ProjectsTableDetailsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ProjectsTableDetailsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ProjectsTableDetailsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it("should be created", () => {
    expect(component).toBeTruthy();
  });
});
