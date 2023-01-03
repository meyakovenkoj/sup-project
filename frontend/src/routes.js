import React from 'react'
import { BrowserRouter, Route, Switch } from 'react-router-dom'
import App from './components/Pages/Task/TaskSearch'
import Login from './components/Pages/Login/Login'
import Task from './components/Pages/Task/Task'
import Profile from './components/Pages/Profile/Profile'
import NotFound from './components/Pages/NotFound/NotFound'
import HeaderBar from './components/Header/HeaderBar'
import Project from './components/Pages/Project/Project'
import ProjectSearch from './components/Pages/Project/ProjectSearch'
import TaskSearch from './components/Pages/Task/TaskSearch'
import PeopleSearch from './components/Pages/People/PeopleSearch'
// import RequireAuth from './utils/requireAuth'

export default class WebRoutes extends React.Component {
  render() {
    const { history } = this.props
    return (
      <div>
        <BrowserRouter>
          <div>
            <HeaderBar history={history} />
              <Switch>
                <Route
                  exact
                  path="/"
                  history={history}
                  component={TaskSearch}
                  />
                <Route
                  exact
                  path="/projects"
                  history={history}
                  component={ProjectSearch}
                  />
                <Route
                  exact
                  path="/login"
                  history={history}
                  component={Login}
                  />
                <Route
                  path="/task"
                  history={history}
                  component={Task}
                  />
                <Route
                  path="/project"
                  history={history}
                  component={Project}
                  />
                <Route
                  path="/profile"
                  history={history}
                  component={Profile}
                  />
                <Route
                  path="/people"
                  history={history}
                  component={PeopleSearch}
                  />
                <Route path="*" component={NotFound} />
              </Switch>
            </div>
        </BrowserRouter>
      </div>
    )
  }
}
