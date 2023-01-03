import React, { useState } from 'react';
import { Modal } from 'antd';
import { LaptopOutlined, NotificationOutlined, UserOutlined } from '@ant-design/icons';
import { EditOutlined, DeleteOutlined, SettingOutlined } from '@ant-design/icons';
import { Breadcrumb, Layout, Menu } from 'antd';
import Search from '../../Header/Search';
import Solve from './Solve';
import UploadFile from '../../utils/UploadFile';
import { Button, Space } from 'antd';
import { Col, Divider, Row } from 'antd';
import { Card } from 'antd';
import { Input } from 'antd';
import { Typography } from 'antd';
import { ArrowDownOutlined, ArrowUpOutlined } from '@ant-design/icons';
import { ExclamationCircleFilled } from '@ant-design/icons';
import { Statistic } from 'antd';
import EditComment from './EditComment';
import EditTask from './EditTask';
const { Title } = Typography;
const { confirm } = Modal;
const { TextArea } = Input;

const showDeleteConfirm = () => {
    confirm({
      title: 'Are you sure delete this task?',
      icon: <ExclamationCircleFilled />,
      content: 'Some descriptions',
      okText: 'Yes',
      okType: 'danger',
      cancelText: 'No',
      onOk() {
        console.log('OK');
      },
      onCancel() {
        console.log('Cancel');
      },
    });
  };

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

    const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
    const deleteShowModal = () => {
        setIsDeleteModalOpen(true);
    };
    const handleOkDelete = () => {
        setIsDeleteModalOpen(false);
    };
    const handleCancelDelete = () => {
        setIsDeleteModalOpen(false);
    };

    const [isEditModalOpen, setIsEditModalOpen] = useState(false);
    const editShowModal = () => {
        setIsEditModalOpen(true);
    };
    const handleOkEdit = () => {
        setIsEditModalOpen(false);
    };
    const handleCancelEdit = () => {
        setIsEditModalOpen(false);
    };

    const [isEditTaskModalOpen, setIsEditTaskModalOpen] = useState(false);
    const editTaskShowModal = () => {
        setIsEditTaskModalOpen(true);
    };
    const handleOkEditTask = () => {
        setIsEditTaskModalOpen(false);
    };
    const handleCancelEditTask = () => {
        setIsEditTaskModalOpen(false);
    };

    return (
        <div>
            {/* <Layout> */}
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
                            <Button onClick={editTaskShowModal} >Edit</Button>
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
                                title="Card title НАСТЯ"
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
                            <Card>
                            <Card
                             type="inner"
                             title="User 1"
                             extra={<div>
                                <Button type="primary" onClick={editShowModal}>Edit</Button>
                                <DeleteOutlined key="delete" onClick={showDeleteConfirm}/>
                                </div>}
                            >
                            <p>Card content</p>
                            </Card>
                            <br></br>
                            <TextArea rows={4} placeholder="maxLength is 6" maxLength={6} />
                            <Button type="primary">Send</Button>
                            </Card>
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
            {/* </Layout> */}
            <Modal title="Close" open={isModalOpen} onOk={handleOk} onCancel={handleCancel}>
                <Solve></Solve>
            </Modal>
            <Modal title="Are you sure to delete?" open={isDeleteModalOpen} onOk={handleOkDelete} onCancel={handleCancelDelete}>
            </Modal>
            <Modal title="Edit" open={isEditModalOpen} onOk={handleOkEdit} onCancel={handleCancelEdit}>
                <EditComment></EditComment>
            </Modal>
            <Modal title="Edit" open={isEditTaskModalOpen} onOk={handleOkEditTask} onCancel={handleCancelEditTask}>
                <EditTask></EditTask>
            </Modal>
        </div>
    );
};

export default Task;