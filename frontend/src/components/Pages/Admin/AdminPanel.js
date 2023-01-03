import React from "react";
import { Layout, Card, Button, Space } from "antd";
import { Link } from "react-router-dom";

const { Header, Content, Footer, Sider } = Layout;

const AdminPanel = () => (
  <Layout className="site-layout-background">
    <Content style={{ padding: "50px" }}>
      {/* <Card> */}
        <Space
          direction="horizontal"
          style={{
            width: "100%",
          }}
        >
          <Link to="/register">
            <Button type="primary">Register User</Button>
          </Link>
          <Link to="/create_project">
            <Button type="primary">Add Project</Button>
          </Link>
        </Space>
      {/* </Card> */}
    </Content>
  </Layout>
);

export default AdminPanel;
