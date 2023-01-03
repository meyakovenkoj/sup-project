import React from "react";
import { Layout, Menu } from "antd";
import { Card } from "antd";
import Task from "./Task";
import SearchBar from "../../Header/SearchBar";

const { Header, Content, Footer, Sider } = Layout;

const mock_items = [
  {
    key: "task1",
    label: "task1",
  },
  {
    key: "task2",
    label: "task2",
  },
  {
    key: "task3",
    label: "task3",
  },
  {
    key: "task4",
    label: "task4",
  },
];

const TaskSearch = ({ component, element }) => (
  <Layout style={{ height: "100%" }}>
    <Content style={{ padding: "0 50px" }}>
      <SearchBar></SearchBar>

      <Layout style={{ padding: "24px 0" }}>
        <Sider className="site-layout-background" width={200}>
          <Menu
            mode="inline"
            defaultSelectedKeys={["1"]}
            defaultOpenKeys={["sub1"]}
            style={{ height: "100%" }}
            items={mock_items}
          />
        </Sider>
        <Content style={{ padding: "0 24px", minHeight: 280 }}>
          <Card>
            <Task></Task>
          </Card>
        </Content>
      </Layout>
    </Content>
    <Footer style={{ textAlign: "center" }}>
      Ant Design ©2018 Created by Ant UED
    </Footer>
  </Layout>
);

export default TaskSearch;
