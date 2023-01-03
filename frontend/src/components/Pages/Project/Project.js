import React from "react";
import { Layout, Typography } from "antd";
const { Title } = Typography;

const { Header, Content, Footer, Sider } = Layout;

const Project = () => {
  return (
    <div>
      <Content
        style={{
          padding: "0 50px",
        }}
      >
        <Title level={2}>h1. Ant Design</Title>
      </Content>
    </div>
  );
};

export default Project;
