import React, { useLayoutEffect } from "react";
import { Layout, Card, Typography, List } from "antd";
import People from "./People";
import { connect } from "react-redux";
import { GetMe, getTasks } from "../../../redux/actions/actions";
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

const Profile = ({user, GetMe, getTasks, tasks}) => {
  useLayoutEffect(() => {
    GetMe();
    getTasks();
  }, []);
  return (
    <div>
      <Layout className="site-layout-background">
        <Content style={{ padding: "50px" }}>
          <Card>
            <People data={user}></People>
            <List
              header={<div>Tasks</div>}
              bordered
              dataSource={tasks}
              renderItem={(item) => (
                <List.Item>
                  <Typography.Text mark>{item.index}</Typography.Text>{" "}
                  {item.title}
                </List.Item>
              )}
            ></List>
          </Card>
        </Content>
      </Layout>
    </div>
  );
};

const mapStateToProps = (state) => {
  return {
    user: state.authUser.user,
    tasks: state.authUser.tasks
  }
}

const mapDispatchToProps = (dispatch) => ({
  GetMe: () => dispatch(GetMe()),
  getTasks: () => dispatch(getTasks())

})

export default connect(mapStateToProps, mapDispatchToProps)(Profile);

