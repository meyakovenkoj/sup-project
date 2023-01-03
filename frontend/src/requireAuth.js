/* eslint-disable import/no-anonymous-default-export */
import React, { Component } from "react";
import { connect } from "react-redux";
import { Redirect } from "react-router-dom";

export default function (ComposedComponent) {
  class RequireAuth extends Component {
    render() {
      return this.props.isAuth ? (
        //   return 1 ? (
        <ComposedComponent {...this.props} />
      ) : (
        <Redirect
          to={{
            pathname: "/login",
          }}
        />
      );
    }
  }

  const mapStateToProps = (state) => {
    return { isAuth: state.lists.isAuth };
  };
  return connect(mapStateToProps)(RequireAuth);
}
