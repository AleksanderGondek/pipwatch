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
  { path: "tags",  component: TagsTableComponent },
  { path: "namespaces",  component: NamespacesTableComponent },
  { path: "requirements",  component: RequirementsTableComponent },
  { path: "requirements-files",  component: RequirementsFilesTableComponent },
  { path: "projects",  component: ProjectsTableComponent }
];

@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})
export class AppRoutingModule {}