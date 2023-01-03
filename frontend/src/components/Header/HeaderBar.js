import React, { useState }  from 'react';
import { Link } from 'react-router-dom';
import { withRouter } from 'react-router';
import { Modal } from 'antd';
import { LaptopOutlined, NotificationOutlined, UserOutlined } from '@ant-design/icons';
import { Breadcrumb, Layout, Menu } from 'antd';
import { Button, Space } from 'antd';
import Search from './Search';
import TaskModal from './TaskModal';
import { Typography } from 'antd';
import { Col, Divider, Row } from 'antd';
import { Avatar } from 'antd';
import { DownOutlined } from '@ant-design/icons';
import { Dropdown } from 'antd';

const { Title } = Typography;


const { Header, Content, Footer, Sider } = Layout;

const HeaderBar = ({
  location
}) => {
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
  const items = [
    {
      label: <Link to="/profile">Profile</Link>,
      key: '0',
    },
    {
      type: 'divider',
    },
    {
      label: <a href="#">Logout</a>,
      key: '1',
    },
  ];
  return(
    <div>
      <Menu theme="dark" mode="horizontal" selectedKeys={[location.pathname]}>
      <Space align="center">
        <Menu.Item key="title">
        <Title style={{color: "#F0F0F0"}} level={2}>SUP</Title>
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
        <Menu.Item key="create">
        <Button type="primary" onClick={showModal}>Create Task</Button>
        </Menu.Item>
        <Menu.Item key="search">
          <Search></Search>
        </Menu.Item>
        <Menu.Item key="user">
        <Dropdown
    menu={{
      items,
    }}
    trigger={['click']}
  >
    <a onClick={(e) => e.preventDefault()}>
      <Space>
        <Avatar size="large" style={{ backgroundColor: '#87d068' }} icon={<UserOutlined />} />
        <DownOutlined />
      </Space>
    </a>
  </Dropdown>
        </Menu.Item>
      </Space>
      </Menu>
      <Modal title="New Task" open={isModalOpen} onOk={handleOk} onCancel={handleCancel}>
     <TaskModal></TaskModal>
   </Modal>
    </div>
    );
  };

export default withRouter(HeaderBar);