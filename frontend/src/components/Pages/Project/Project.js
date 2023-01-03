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
const { Title } = Typography;
const { TextArea } = Input;

const { Meta } = Card;
const { Header, Content, Footer, Sider } = Layout;


const Project = () => {
    return (
        <div>
            <Content
        style={{
          padding: '0 50px',
        }}
      >

    
                    <Title level={2}>h1. Ant Design</Title>


</Content>
        </div>
    );
};

export default Project;