import React, { useState }  from 'react';
import { useLocation } from 'react-router';
import { Modal } from 'antd';
import { LaptopOutlined, NotificationOutlined, UserOutlined } from '@ant-design/icons';
import { Breadcrumb, Layout, Menu } from 'antd';
import { Button, Space } from 'antd';
import Search from './Search';
import TaskModal from './TaskModal';

import { Avatar } from 'antd';

const { Header, Content, Footer, Sider } = Layout;

const HeaderBar = () => {
  const location = useLocation();
  // const items1 = [
  //   {
  //     key,
  //     label: `nav ${key}`,
  //   },
  //   {
  //     'Projects',

  //   }
  // ];
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
  return(
  // <Layout style={{ height: '100%' }}>
  <div>
    <Header className="header">
      <div className="logo" />
      {/* <Menu theme="dark" mode="horizontal" defaultSelectedKeys={['2']} items={[...items1, {label:(<Search></Search>), key:"search"}, {label:(<Button type="primary" onClick={showModal}>Create Task</Button>), key:"create"}, {label:(<Avatar size="large" style={{ backgroundColor: '#87d068' }} icon={<UserOutlined />} />), key:"user"}]}> */}
      {/* </Menu> */}
      <Menu theme="dark" mode="horizontal">
        <Menu.Item key="/explore">
          <Link to="/explore">Explore</Link>
        </Menu.Item>
        <Menu.Item key="/">
          <Link to="/">Dashboard</Link>
        </Menu.Item>
      </Menu>
    </Header>
    <Modal title="New Task" open={isModalOpen} onOk={handleOk} onCancel={handleCancel}>
    <TaskModal></TaskModal>
  </Modal>
  </div>
    // </Layout>
    );
  };

export default HeaderBar;