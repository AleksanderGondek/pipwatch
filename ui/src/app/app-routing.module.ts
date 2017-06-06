import { NgModule } from "@angular/core";
import { RouterModule, Routes } from "@angular/router";

import { CreditsComponent } from "./credits/credits.component";
import { DashboardComponent } from "./dashboard/dashboard.component";
import { HealthComponent } from "./health/health.component";

import { CrudComponent } from "./crud/crud.component";
import { TagsTableComponent } from "./crud/tags-table/tags-table.component";
import { NamespacesTableComponent } from "./crud/namespaces-table/namespaces-table.component";
import { RequirementsTableComponent } from "./crud/requirements-table/requirements-table.component";
import { RequirementsFilesTableComponent } from "./crud/requirements-files-table/requirements-files-table.component";
import { ProjectsTableComponent } from "./crud/projects-table/projects-table.component";

export const routes: Routes = [
  { path: "", redirectTo: "/dashboard", pathMatch: "full" },
  { path: "credits", component: CreditsComponent },
  { path: "dashboard", component: DashboardComponent },
  { path: "health", component: HealthComponent },
  { path: "crud", component: CrudComponent },
  { path: "crud/tags", component: TagsTableComponent },
  { path: "crud/namespaces", component: NamespacesTableComponent },
  { path: "crud/requirements", component: RequirementsTableComponent },
  { path: "crud/requirements-files", component: RequirementsFilesTableComponent },
  { path: "crud/projects", component: ProjectsTableComponent }
];

@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})
export class AppRoutingModule {}
