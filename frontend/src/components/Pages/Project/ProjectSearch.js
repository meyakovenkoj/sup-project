import React, { useLayoutEffect, useState } from "react";
import { Layout, Menu, Card } from "antd";
import Project from "./Project";
import SearchBar from "../../Header/SearchBar";
import { getProjects, searchProject } from "../../../redux/actions/actions";
import { connect } from "react-redux";

const { Header, Content, Footer, Sider } = Layout;



const ProjectSearch = ({ component, element, projects, getProjects, searchProject }) => {
  useLayoutEffect(() => {
    getProjects();
  }, []);
  const [selectedProject, setSelectedProject] = useState({});

  const handleSelect = (info) => {
    setSelectedProject(info.item.props);
  }

  const searchFunc = (data) => {
    if(data === '') {
      getProjects();
    } else {
      searchProject(data);
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
            items={projects}
            onSelect={handleSelect}
          />
        </Sider>
        <Content style={{ padding: "0 24px", minHeight: 280 }}>
          <Card>
            <Project  data={selectedProject} projId={selectedProject._id}></Project>
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
    users: state.authUser.users,
    projects: state.authUser.projects
  }
}

const mapDispatchToProps = (dispatch) => ({
  getProjects: () => dispatch(getProjects()),
  searchProject: (title) => dispatch(searchProject(title))
})

export default connect(mapStateToProps, mapDispatchToProps)(ProjectSearch);
