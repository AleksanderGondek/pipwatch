import { NgModule } from "@angular/core";
import { RouterModule, Routes } from "@angular/router";

import { AboutComponent } from "app/about/about.component";
import { AppComponent } from "app/app.component";
import { CreateProjectComponent } from "app/create-project/create-project.component";
import { ProjectsOverviewComponent } from "app/projects-overview/projects-overview.component";
import { ProjectDetailsComponent } from "app/project-details/project-details.component";

const routes: Routes = [
    {path: "", redirectTo: "/home", pathMatch: "full"},
    {path: "home", component: ProjectsOverviewComponent},
    {path: "new", component: CreateProjectComponent},
    {path: "about", component: AboutComponent},
    {path: "details/:id", component: ProjectDetailsComponent}
];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class AppRouting {}
