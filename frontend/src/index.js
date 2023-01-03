import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import WebRoutes from "./routes";
import { Provider } from "react-redux";
import configureStore from "./redux/store";
import { Layout } from "antd";
const store = configureStore();

ReactDOM.render(
  <Provider store={{ ...store }}>
    <Layout style={{ height: "100%" }}>
      <WebRoutes store={{ ...store }} />
    </Layout>
  </Provider>,
  document.getElementById("root")
);
