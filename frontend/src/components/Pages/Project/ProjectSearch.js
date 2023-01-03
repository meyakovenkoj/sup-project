import React from 'react';
import { LaptopOutlined, NotificationOutlined, UserOutlined } from '@ant-design/icons';
import { Breadcrumb, Layout, Menu } from 'antd';
import Search from '../../Header/Search';
import { Card } from 'antd';
import Project from './Project';
import SearchBar from '../../Header/SearchBar';
const { Meta } = Card;

const { Header, Content, Footer, Sider } = Layout;

const mock_items = [
    {
        key: 'proj1',
        label: 'proj1'
    },
    {
        key: 'proj2',
        label: 'proj2'
    },
    {
        key: 'proj3',
        label: 'proj3'
    },
    {
        key: 'proj4',
        label: 'proj4'
    },
];

const ProjectSearch = ({component, element}) => (
  <Layout style={{ height: '100%' }}>
    <Content style={{ padding: '0 50px' }}>
            <SearchBar></SearchBar>
      <Layout style={{ padding: '24px 0' }}>
        <Sider className="site-layout-background" width={200}>
          <Menu
            mode="inline"
            defaultSelectedKeys={['1']}
            defaultOpenKeys={['sub1']}
            style={{ height: '100%' }}
            items={mock_items}
          />
        </Sider>
        <Content style={{ padding: '0 24px', minHeight: 280 }}>
          <Card
          >
            <Project></Project>
          </Card>
        </Content>
      </Layout>
    </Content>
    <Footer style={{ textAlign: 'center' }}>Ant Design ©2018 Created by Ant UED</Footer>
  </Layout>
);

export default ProjectSearch;