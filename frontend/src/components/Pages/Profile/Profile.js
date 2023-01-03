import React, { useState } from 'react';
import { Modal } from 'antd';
import { LaptopOutlined, NotificationOutlined, UserOutlined } from '@ant-design/icons';
import { Breadcrumb, Layout, Menu } from 'antd';
import Search from '../../Header/Search';
import Solve from '../Task/Solve';
import UploadFile from '../../utils/UploadFile';
import { Button, Space } from 'antd';
import { Col, Divider, Row } from 'antd';
import { Card } from 'antd';
import { Input } from 'antd';
import { Typography } from 'antd';
import { ArrowDownOutlined, ArrowUpOutlined } from '@ant-design/icons';
import { Statistic } from 'antd';
import { List } from 'antd';
import People from '../People/People';
const { Title } = Typography;
const { TextArea } = Input;
const { Header, Content, Footer, Sider } = Layout;

const { Meta } = Card;
const data = [
  'Racing car sprays burning fuel into crowd.',
  'Japanese princess to wed commoner.',
  'Australian walks 100km after outback crash.',
  'Man charged over missing wedding girl.',
  'Los Angeles battles huge wildfires.',
];

const mock_tasks = [
  {title:'Racing car sprays burning fuel into crowd.', index: 'TS-1'},
  {title:'Japanese princess to wed commoner.', index: 'TS-1'},
  {title:'Australian walks 100km after outback crash.', index: 'TS-1'},
  {title:'Man charged over missing wedding girl.', index: 'TS-1'},
  {title:'Los Angeles battles huge wildfires.', index: 'TS-1'}
];


const Profile = () => {
    return (
        <div>
            <Layout className="site-layout-background">
            <Content style={{ padding: '50px' }}>

              <Card>

            <People data={data}></People>
            <List header={<div>Tasks</div>}
      bordered
      dataSource={mock_tasks}
      renderItem={(item) => (
        <List.Item>
          <Typography.Text mark>{item.index}</Typography.Text> {item.title}
        </List.Item>
      )}></List>
              </Card>
            <Content>some controls</Content>
      </Content>
      </Layout>
      </div>
      );
      };

      export default Profile;