import React, { useState } from 'react';
import { Modal } from 'antd';
import { LaptopOutlined, NotificationOutlined, UserOutlined } from '@ant-design/icons';
import { Breadcrumb, Layout, Menu } from 'antd';
import Search from './Search';
import Solve from './Solve';
import UploadFile from './UploadFile';
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
// const style = {
//     background: '#0092ff',
//     padding: '8px 0',
// };

const { Header, Content, Footer, Sider } = Layout;

const items1 = ['1', '2', '3'].map((key) => ({
    key,
    label: `nav ${key}`,
}));

const Task = () => {
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
    return (
        <div>
            <Layout>
            <Content
        style={{
          padding: '0 50px',
        }}
      >
                <Breadcrumb
                    style={{
                        margin: '16px 0',
                    }}
                >
                    <Breadcrumb.Item>Home</Breadcrumb.Item>
                    <Breadcrumb.Item>List</Breadcrumb.Item>
                    <Breadcrumb.Item>App</Breadcrumb.Item>
                </Breadcrumb>
    
                    <Title level={2}>h1. Ant Design</Title>
                    <Row gutter={14}>
                        <Col className="gutter-row" span={6}>
                            <Button type="primary" onClick={showModal}>
                                Close
                            </Button>
                        </Col>
                        <Col className="gutter-row" span={6}>
                        </Col>
                        <Col className="gutter-row" span={6}>
                            <Button >Primary Button</Button>
                        </Col>
                        <Col className="gutter-row" span={6}>
                            <Button type="primary">Primary Button</Button>

                        </Col>
                    </Row>
                    <Row gutter={16}>
                        <Col className="gutter-row" span={6}>
                            <Button >Primary Button</Button>
                            <Button >Primary Button</Button>
                        </Col>
                        <Col className="gutter-row" span={6}>
                        </Col>
                        <Col className="gutter-row" span={6}>
                            <Button >Primary Button</Button>
                        </Col>
                        <Col className="gutter-row" span={6}>
                            <Button >Primary Button</Button>
                        </Col>
                    </Row>

                    <Row gutter={16}>
                        <Col className="gutter-row" span={18}>
                            <Card
                                title="Card title"
                                bordered={false}
                                style={{
                                }}
                            >
                                <p>Card content</p>
                                <p>Card content</p>
                                <p>Card content</p>
                            </Card>
                            <Card>
                                <UploadFile></UploadFile>
                            </Card>
                            <TextArea rows={4} placeholder="maxLength is 6" maxLength={6} />
                    <Button type="primary">Send</Button>
                        </Col>
                        <Col className="gutter-row" span={4}>

                            <Card
                                title="Card title"
                                bordered={false}
                                style={{
                                }}
                            >
                                <p>Card content</p>
                                <p>Card content</p>
                                <p>Card content</p>
                            </Card>
                            
                            <Row>

                                <Col span={12}>
                                    <Card>
                                        <Statistic
                                            title="Active"
                                            value={11.28}
                                            precision={2}
                                            valueStyle={{
                                                color: '#3f8600',
                                            }}
                                            prefix={<ArrowUpOutlined />}
                                            suffix="%"
                                        />
                                    </Card>
                                </Col>
                                <Col span={12}>
                                    <Card>
                                        <Statistic
                                            title="Idle"
                                            value={9.3}
                                            precision={2}
                                            valueStyle={{
                                                color: '#cf1322',
                                            }}
                                            prefix={<ArrowDownOutlined />}
                                            suffix="%"
                                        />
                                    </Card>
                                </Col>
                            </Row>
                        </Col>
                    </Row>
                    <br />
                    <br />


</Content>
            </Layout>
            <Modal title="Close" open={isModalOpen} onOk={handleOk} onCancel={handleCancel}>
                <Solve></Solve>
            </Modal>
        </div>
    );
};

export default Task;