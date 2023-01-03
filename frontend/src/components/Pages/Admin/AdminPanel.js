import React from 'react';
import { LaptopOutlined, NotificationOutlined, UserOutlined } from '@ant-design/icons';
import { Breadcrumb, Layout, Menu } from 'antd';
import { Card } from 'antd';
import { Link } from 'react-router-dom';
import { Button, Space } from 'antd';
const { Meta } = Card;

const { Header, Content, Footer, Sider } = Layout;



const AdminPanel = ({component, element}) => (
    <Layout className="site-layout-background">
    <Content style={{ padding: '50px' }}>
        <Card>
        <Space
    direction="vertical"
    style={{
      width: '100%',
    }}
  >
        <Link to="/register"><Button type="primary">Register User</Button></Link>
        <Link to="/create_project"><Button type="primary">Add Project</Button></Link>
        </Space>
        </Card>
      
    </Content>
    </Layout>
);

export default AdminPanel;