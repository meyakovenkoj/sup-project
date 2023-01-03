import React, { useState } from "react";
import { Link } from "react-router-dom";
import { withRouter } from "react-router";
import { Modal, Menu, Button, Space, Typography, Avatar, Dropdown } from "antd";
import { UserOutlined, DownOutlined } from "@ant-design/icons";
import Search from "./MySearch";
import TaskModal from "../Pages/Task/TaskModal";
import { connect } from "react-redux";
import { Logout } from "../../redux/actions/actions";

const { Title } = Typography;

const HeaderBar = ({ location, Logout }) => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const showModal = () => {
    setIsModalOpen(true);
  };
  const handleOk = () => {
    setIsModalOpen(false);
  };
  const handleCancel = () => {
    setIsModalOpen(false);
  };
  const handleLogout = () => {
    Logout();
  }
  const items = [
    {
      label: <Link to="/profile">Profile</Link>,
      key: "0",
    },
    {
      type: "divider",
    },
    {
      label: <Link to="/login" onClick={handleLogout}>Logout</Link>,
      key: "1",
    },
  ];
  return (
    <div>
      <Menu theme="dark" mode="horizontal" selectedKeys={[location.pathname]}>
        <Space align="center">
          <Menu.Item key="title">
            <Title style={{ color: "#F0F0F0" }} level={2}>
              SUP
            </Title>
            <Link to="/"></Link>
          </Menu.Item>
          <Menu.Item key="/">
            <Link to="/">Tasks</Link>
          </Menu.Item>
          <Menu.Item key="/projects">
            <Link to="/projects">Projects</Link>
          </Menu.Item>
          <Menu.Item key="/people">
            <Link to="/people">People</Link>
          </Menu.Item>
          <Menu.Item key="/admin">
            <Link to="/admin">Admin Panel</Link>
          </Menu.Item>
          <Menu.Item key="create">
            <Button type="primary" onClick={showModal}>
              Create Task
            </Button>
          </Menu.Item>
          <Menu.Item key="search">
            <Search></Search>
          </Menu.Item>
          <Menu.Item key="user">
            <Dropdown
              menu={{
                items,
              }}
              trigger={["click"]}
            >
              <a onClick={(e) => e.preventDefault()}>
                <Space>
                  <Avatar
                    size="large"
                    style={{ backgroundColor: "#87d068" }}
                    icon={<UserOutlined />}
                  />
                  <DownOutlined />
                </Space>
              </a>
            </Dropdown>
          </Menu.Item>
        </Space>
      </Menu>
      <Modal
        title="New Task"
        open={isModalOpen}
        onOk={handleOk}
        onCancel={handleCancel}
      >
        <TaskModal></TaskModal>
      </Modal>
    </div>
  );
};


const mapStateToProps = (state) => {
  return {
    loading: state.authUser.loading
  }
}

const mapDispatchToProps = (dispatch) => ({
  Logout: () => dispatch(Logout())
})

export default connect(mapStateToProps, mapDispatchToProps)(withRouter(HeaderBar));