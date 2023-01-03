import React from "react";
import { BrowserRouter, Route, Switch } from "react-router-dom";
import Login from "./components/Pages/Login/Login";
import Task from "./components/Pages/Task/Task";
import Profile from "./components/Pages/People/Profile";
import NotFound from "./components/Pages/NotFound/NotFound";
import HeaderBar from "./components/Header/HeaderBar";
import Project from "./components/Pages/Project/Project";
import ProjectSearch from "./components/Pages/Project/ProjectSearch";
import TaskSearch from "./components/Pages/Task/TaskSearch";
import PeopleSearch from "./components/Pages/People/PeopleSearch";
import CreateProject from "./components/Pages/Project/CreateProject";
import Registration from "./components/Pages/Login/Registation";
import AdminPanel from "./components/Pages/Admin/AdminPanel";
import RequireAuth from "./requireAuth";

export default class WebRoutes extends React.Component {
  render() {
    const { history } = this.props;
    return (
      <div>
        <BrowserRouter>
          <div>
            <HeaderBar history={history} />
            <Switch>
              <Route exact path="/" history={history} component={RequireAuth(TaskSearch)} />
              <Route
                exact
                path="/projects"
                history={history}
                component={RequireAuth(ProjectSearch)}
              />
              <Route exact path="/login" history={history} component={Login} />
              <Route path="/task" history={history} component={RequireAuth(Task)} />
              <Route path="/project" history={history} component={RequireAuth(Project)} />
              <Route path="/profile" history={history} component={RequireAuth(Profile)} />
              <Route
                path="/people"
                history={history}
                component={RequireAuth(PeopleSearch)}
              />
              <Route
                path="/create_project"
                history={history}
                component={RequireAuth(CreateProject)}
              />
              <Route
                path="/register"
                history={history}
                component={RequireAuth(Registration)}
              />
              <Route path="/admin" history={history} component={RequireAuth(AdminPanel)} />

              <Route path="*" component={NotFound} />
            </Switch>
          </div>
        </BrowserRouter>
      </div>
    );
  }
}
