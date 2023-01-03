import React, { Component } from "react";
import { Button, Space } from 'antd';

const divStyle = {
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  flexDirection: "column",
};

const NotFound = () => {
    return (
      <div style={divStyle}>
        <h1>Not Found</h1>
        <p>Return back?</p>
        <Button
        type="primary"
          onClick={() => {
            window.location.href = "/";
          }}
        >
          Go home
        </Button>
      </div>
    );
}

export default NotFound;
