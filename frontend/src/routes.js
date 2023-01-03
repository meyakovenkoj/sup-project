import React from 'react'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import App from './Main'
import Login from './Login'
import Task from './Task'
import Profile from './Profile'
import NotFound from './NotFound'
// import RequireAuth from './utils/requireAuth'

export default class WebRoutes extends React.Component {
  render() {
    const { history } = this.props
    return (
      <div>
        <Router>
          <Routes>
            <Route
              exact
              path="/"
              history={history}
              element={<App></App>}
            />
            <Route
              exact
              path="/login"
              history={history}
              element={<Login></Login>}
            />
            <Route
              path="/task"
              history={history}
              element={<Task></Task>}
            />
            <Route
              path="/profile"
              history={history}
              element={<Profile></Profile>}
            />
            <Route path="*" element={<NotFound></NotFound>} />
          </Routes>
        </Router>
      </div>
    )
  }
}
