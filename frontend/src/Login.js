import React from 'react';
import { Button, Checkbox, Form, Input } from 'antd';
import { Card, Space } from 'antd';
const { Meta } = Card;

    const Login = () => {
        const onFinish = (values) => {
          console.log('Success:', values);
        };
        const onFinishFailed = (errorInfo) => {
          console.log('Failed:', errorInfo);
        };
    return (
        <div>
<Space align="center">

        <Card
                style={{
                    width: 350,
                }}
                >
    <Form
      name="basic"
      labelCol={{
          span: 8,
        }}
        wrapperCol={{
            span: 16,
        }}
        onFinish={onFinish}
        onFinishFailed={onFinishFailed}
        autoComplete="off"
        >
      <Form.Item
        label="Username"
        name="username"
        rules={[
            {
                required: true,
                message: 'Please input your username!',
            },
        ]}
        >
        <Input />
      </Form.Item>

      <Form.Item
        label="Password"
        name="password"
        rules={[
            {
                required: true,
                message: 'Please input your password!',
            },
        ]}
        >
        <Input.Password />
      </Form.Item>

      <Form.Item
        wrapperCol={{
            offset: 8,
            span: 16,
        }}
        >
        <Button type="primary" htmlType="submit">
          Submit
        </Button>
      </Form.Item>
    </Form>
          </Card>
          </Space>
    </div>
);
    };

export default Login;