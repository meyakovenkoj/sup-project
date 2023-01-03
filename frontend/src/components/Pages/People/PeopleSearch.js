import React from "react";
import { Card, Layout, Menu } from "antd";
import People from "./People";
import SearchBar from "../../Header/SearchBar";

const { Header, Content, Footer, Sider } = Layout;

const mock_items = [
  {
    key: "man 1",
    label: "man 1",
  },
  {
    key: "man 2",
    label: "man 2",
  },
  {
    key: "man 3",
    label: "man 3",
  },
  {
    key: "man 4",
    label: "man 4",
  },
];

const data = [
  "Racing car sprays burning fuel into crowd.",
  "Japanese princess to wed commoner.",
  "Australian walks 100km after outback crash.",
  "Man charged over missing wedding girl.",
  "Los Angeles battles huge wildfires.",
];

const PeopleSearch = ({ component, element }) => (
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
            <People data={data}></People>
          </Card>
        </Content>
      </Layout>
    </Content>
    <Footer style={{ textAlign: "center" }}>
      Ant Design ©2018 Created by Ant UED
    </Footer>
  </Layout>
);

export default PeopleSearch;
