import React, { useState } from 'react';
import { Modal } from 'antd';
import { LaptopOutlined, NotificationOutlined, UserOutlined } from '@ant-design/icons';
import { Breadcrumb, Layout, Menu } from 'antd';
import Search from '../../Header/Search';
// import Solve from './Solve';
import UploadFile from '../../utils/UploadFile';
import { Button, Space } from 'antd';
import { Col, Divider, Row } from 'antd';
import { Card } from 'antd';
import { Input } from 'antd';
import { Typography } from 'antd';
import { ArrowDownOutlined, ArrowUpOutlined } from '@ant-design/icons';
import { Statistic } from 'antd';
import { List } from 'antd';

const { Title } = Typography;
const { TextArea } = Input;

const { Meta } = Card;
const { Header, Content, Footer, Sider } = Layout;


const People = ({data}) => {
    return (
        <div>
            <Content
        style={{
          padding: '0 50px',
        }}
      >
        <Row gutter={16}>
            <Col>
            <Card
    hoverable
    style={{
      width: 240,
    }}
    cover={<img alt="example" src="https://os.alipayobjects.com/rmsportal/QBnOOoLaAfKPirc.png" />}
  >
    <Meta title="Europe Street beat" description="www.instagram.com" />
  </Card>
            </Col>
            <Col>
            <List
      header={<div>Header</div>}
      footer={<div>Footer</div>}
      bordered
      dataSource={data}
      renderItem={(item) => (
        <List.Item>
          <Typography.Text mark>[ITEM]</Typography.Text> {item}
        </List.Item>
      )}
    />
            </Col>
        </Row>
        
  
      </Content>
      </div>
    );
};

export default People;