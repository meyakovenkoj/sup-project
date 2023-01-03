import React from "react";
import { Link } from "react-router-dom";
import { Button } from "antd";

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
      <Link to="/">
        <Button type="primary">Go home</Button>
      </Link>
    </div>
  );
};

export default NotFound;
