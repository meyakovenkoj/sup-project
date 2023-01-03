import React from "react";
import { Layout, Card, Typography, List } from "antd";
import People from "./People";
const { Header, Content, Footer, Sider } = Layout;

const data = [
  "Racing car sprays burning fuel into crowd.",
  "Japanese princess to wed commoner.",
  "Australian walks 100km after outback crash.",
  "Man charged over missing wedding girl.",
  "Los Angeles battles huge wildfires.",
];

const mock_tasks = [
  { title: "Racing car sprays burning fuel into crowd.", index: "TS-1" },
  { title: "Japanese princess to wed commoner.", index: "TS-1" },
  { title: "Australian walks 100km after outback crash.", index: "TS-1" },
  { title: "Man charged over missing wedding girl.", index: "TS-1" },
  { title: "Los Angeles battles huge wildfires.", index: "TS-1" },
];

const Profile = () => {
  return (
    <div>
      <Layout className="site-layout-background">
        <Content style={{ padding: "50px" }}>
          <Card>
            <People data={data}></People>
            <List
              header={<div>Tasks</div>}
              bordered
              dataSource={mock_tasks}
              renderItem={(item) => (
                <List.Item>
                  <Typography.Text mark>{item.index}</Typography.Text>{" "}
                  {item.title}
                </List.Item>
              )}
            ></List>
          </Card>
          <Content>some controls</Content>
        </Content>
      </Layout>
    </div>
  );
};

export default Profile;
