import { NgModule } from "@angular/core";
import { RouterModule, Routes } from "@angular/router";

import { AppComponent } from "app/app.component";
import { ProjectsOverviewComponent } from "app/projects-overview/projects-overview.component";
import { ProjectDetailsComponent } from "app/project-details/project-details.component";

const routes: Routes = [
    {path: "", redirectTo: "/home", pathMatch: "full"},
    {path: "home", component: ProjectsOverviewComponent},
    {path: "details/:id", component: ProjectDetailsComponent}
];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class AppRouting {}
