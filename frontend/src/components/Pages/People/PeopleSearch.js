import React, { useLayoutEffect, useState } from "react";
import { Card, Input, Layout, Menu } from "antd";
import People from "./People";
import SearchBar from "../../Header/SearchBar";
import { getUsers, searchUser } from "../../../redux/actions/actions";
import { connect } from "react-redux";
const { Search } = Input;

const { Header, Content, Footer, Sider } = Layout;


const PeopleSearch = ({ component, element, getUsers, users, searchUser }) => {
  useLayoutEffect(() => {
    getUsers();
  }, []);
  const [selectedUser, setSelectedUser] = useState({});

  const handleSelect = (info) => {
    setSelectedUser(info.item.props);
  }

  const searchFunc = (data) => {
    if(data === '') {
      getUsers();
    } else {
      searchUser(data);
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
            style={{ height: "100%" }}
            items={users}
            onSelect={handleSelect}
          />
        </Sider>
        <Content style={{ padding: "0 24px", minHeight: 280 }}>
          <Card>
            <People data={selectedUser}></People>
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
    users: state.authUser.users
  }
}

const mapDispatchToProps = (dispatch) => ({
  getUsers: () => dispatch(getUsers()),
  searchUser: (username) => dispatch(searchUser(username))
})

export default connect(mapStateToProps, mapDispatchToProps)(PeopleSearch);
