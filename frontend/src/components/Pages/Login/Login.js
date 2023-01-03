import React from "react";
import { Button, Card, Space, Form, Input, Layout } from "antd";
import { connect } from "react-redux";
import { LoginUser } from "../../../redux/actions/actions";
const { Header, Content, Footer, Sider } = Layout;



const Login = (props) => {
  const onFinish = (values) => {
    props.LoginUser({ user: { ...values } })
    console.log("Success:", values);
  };
  const onFinishFailed = (errorInfo) => {
    console.log("Failed:", errorInfo);
  };
  return (
    <Layout style={{ height: "100%" }}>
      <Content style={{ padding: "0 50px", justifyContent: "center" }}>
        <Space align="center">
          <Card>
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
                    message: "Please input your username!",
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
                    message: "Please input your password!",
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
      </Content>
    </Layout>
  );
};

const mapStateToProps = (state) => {
  return {
    loading: state.authUser.loading
  }
}

const mapDispatchToProps = (dispatch) => ({
  LoginUser: (userInfo) => dispatch(LoginUser(userInfo))
})

export default connect(mapStateToProps, mapDispatchToProps)(Login);
