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
import { Card } from 'antd';

import { Col, Divider, Row } from 'antd';
import { Avatar } from 'antd';
const { Title } = Typography;


const { Header, Content, Footer, Sider } = Layout;

const SearchBar = () => {
    return (
    <Content
    style={{
      padding: '10px 0 0 0',
    }}
  >
    <Card
                            bordered={false}
                            style={{
                            }}
                        >
                <Row gutter={14}>
                    <Col className="gutter-row" span={6}>
                        <Button type="primary">
                            Close
                        </Button>
                    </Col>
                    <Col className="gutter-row" span={6}>
                        <Search></Search>
                    </Col>
                    <Col className="gutter-row" span={6}>
                        <Button >Primary Button</Button>
                    </Col>
                    <Col className="gutter-row" span={6}>
                        <Button type="primary">Primary Button</Button>

                    </Col>
                </Row>
                
                        
       
                        </Card>
                     

</Content>);
};


export default SearchBar;