import React, { useLayoutEffect, useState } from "react";
import { Layout, Menu } from "antd";
import { Card } from "antd";
import Task from "./Task";
import SearchBar from "../../Header/SearchBar";
import { connect } from "react-redux";
import { getTasks } from "../../../redux/actions/actions";

const { Header, Content, Footer, Sider } = Layout;



const TaskSearch = ({ component, element, getTasks, tasks }) => {
  useLayoutEffect(() => {
    getTasks();
  }, []);
  const [selectedTask, setSelectedTask] = useState({});

  const handleSelect = (info) => {
    setSelectedTask(info.item.props);
  }

  const searchFunc = (data) => {
    getTasks();
  }
  return (
    <Layout style={{ height: "100%" }}>
    <Content style={{ padding: "0 50px" }}>
      <SearchBar searchFunc={searchFunc}></SearchBar>

      <Layout style={{ padding: "24px 0" }}>
        <Sider className="site-layout-background" width={200}>
          <Menu
            mode="inline"
            defaultSelectedKeys={["1"]}
            defaultOpenKeys={["sub1"]}
            style={{ height: "100%" }}
            items={tasks}
            onSelect={handleSelect}
          />
        </Sider>
        <Content style={{ padding: "0 24px", minHeight: 280 }}>
          <Card>
            <Task data={selectedTask}></Task>
          </Card>
        </Content>
      </Layout>
    </Content>
    <Footer style={{ textAlign: "center" }}>
      Ant Design ©2018 Created by Ant UED
    </Footer>
  </Layout>
);
  };

const mapStateToProps = (state) => {
  return {
    loading: state.authUser.loading,
    tasks: state.authUser.tasks
  }
}

const mapDispatchToProps = (dispatch) => ({
  getTasks: () => dispatch(getTasks()),
})

export default connect(mapStateToProps, mapDispatchToProps)(TaskSearch);