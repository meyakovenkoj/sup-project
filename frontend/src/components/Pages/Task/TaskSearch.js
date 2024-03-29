import React, { useLayoutEffect, useState } from "react";
import { Layout, Menu } from "antd";
import { Card } from "antd";
import Task from "./Task";
import SearchBar from "../../Header/SearchBar";
import { connect } from "react-redux";
import { getTask, getTasks, searchTask } from "../../../redux/actions/actions";

const { Header, Content, Footer, Sider } = Layout;



const TaskSearch = ({ component, element, getTasks, getTask, tasks , searchTask, selectedTask}) => {
  useLayoutEffect(() => {
    getTasks();
  }, []);

  const handleSelect = (info) => {
    getTask(info.item.props._id);
  }

  const searchFunc = (data) => {
    if(data === '') {
      getTasks();
    } else {
      searchTask(data);
    }
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
  };

const mapStateToProps = (state) => {
  return {
    loading: state.authUser.loading,
    tasks: state.authUser.tasks,
    selectedTask: state.authUser.sel_task
  }
}

const mapDispatchToProps = (dispatch) => ({
  getTasks: () => dispatch(getTasks()),
  getTask: (task_id) => dispatch(getTask(task_id)),
  searchTask: (title) => dispatch(searchTask(title))
})

export default connect(mapStateToProps, mapDispatchToProps)(TaskSearch);