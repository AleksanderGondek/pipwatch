import { async, ComponentFixture, TestBed } from "@angular/core/testing";

import { TagsTableComponent } from "./tags-table.component";

describe("TagsTableComponent", () => {
  let component: TagsTableComponent;
  let fixture: ComponentFixture<TagsTableComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TagsTableComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TagsTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it("should be created", () => {
    expect(component).toBeTruthy();
  });
});
