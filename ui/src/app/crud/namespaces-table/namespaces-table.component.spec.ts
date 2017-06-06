import { async, ComponentFixture, TestBed } from "@angular/core/testing";

import { NamespacesTableComponent } from "./namespaces-table.component";

describe("NamespacesTableComponent", () => {
  let component: NamespacesTableComponent;
  let fixture: ComponentFixture<NamespacesTableComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ NamespacesTableComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(NamespacesTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it("should be created", () => {
    expect(component).toBeTruthy();
  });
});
