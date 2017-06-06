import { async, ComponentFixture, TestBed } from "@angular/core/testing";

import { ProjectsTableComponent } from "./projects-table.component";

describe("ProjectsTableComponent", () => {
  let component: ProjectsTableComponent;
  let fixture: ComponentFixture<ProjectsTableComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ProjectsTableComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ProjectsTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it("should be created", () => {
    expect(component).toBeTruthy();
  });
});
