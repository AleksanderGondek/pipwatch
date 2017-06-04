import { NgModule } from "@angular/core";
import { RouterModule, Routes } from "@angular/router";

import { DashboardComponent } from "./dashboard/dashboard.component";

import { TagsTableComponent } from "./tags-table/tags-table.component";
import { NamespacesTableComponent } from "./namespaces-table/namespaces-table.component";
import { RequirementsTableComponent } from "./requirements-table/requirements-table.component";
import { RequirementsFilesTableComponent } from "./requirements-files-table/requirements-files-table.component";
import { ProjectsTableComponent } from "./projects-table/projects-table.component";

export const routes: Routes = [
  { path: "", redirectTo: "/dashboard", pathMatch: "full" },
  { path: "dashboard",  component: DashboardComponent },
  { path: "crud",  component: DashboardComponent }, // TODO: Switch to separate component
  { path: "crud/tags",  component: TagsTableComponent },
  { path: "crud/namespaces",  component: NamespacesTableComponent },
  { path: "crud/requirements",  component: RequirementsTableComponent },
  { path: "crud/requirements-files",  component: RequirementsFilesTableComponent },
  { path: "crud/projects",  component: ProjectsTableComponent }
];

@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})
export class AppRoutingModule {}
