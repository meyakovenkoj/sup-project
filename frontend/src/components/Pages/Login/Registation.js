import React from "react";
import { Button, Form, Input, Card, Space, Typography } from "antd";
import { Layout } from "antd";
import { connect } from "react-redux";
import { RegisterUser } from "../../../redux/actions/actions";
const { Title } = Typography;
const { Meta } = Card;
const { Header, Content, Footer, Sider } = Layout;

const formItemLayout = {
  labelCol: {
    xs: {
      span: 24,
    },
    sm: {
      span: 8,
    },
  },
  wrapperCol: {
    xs: {
      span: 24,
    },
    sm: {
      span: 16,
    },
  },
};
const tailFormItemLayout = {
  wrapperCol: {
    xs: {
      span: 24,
      offset: 0,
    },
    sm: {
      span: 16,
      offset: 8,
    },
  },
};
const Registration = (props) => {
  const [form] = Form.useForm();
  const onFinish = (values) => {
    props.RegisterUser({ user: { ...values } })
    console.log("Received values of form: ", values);
  };

  return (
    <Layout style={{ height: "100%" }}>
      <Content style={{ padding: "0 50vh", justifyContent: "center" }}>
      <Title level={2}>Registation</Title>

        {/* <Space align="center"> */}
          {/* <Card> */}
            <Form
              {...formItemLayout}
              form={form}
              name="register"
              onFinish={onFinish}
              initialValues={{
                residence: ["zhejiang", "hangzhou", "xihu"],
                prefix: "86",
              }}
              scrollToFirstError
            >
              <Form.Item
                name="name"
                label="Name"
                rules={[
                  {
                    required: true,
                    message: "Please input name!",
                  },
                ]}
              >
                <Input />
              </Form.Item>

              <Form.Item
                name="surname"
                label="Surname"
                rules={[
                  {
                    required: true,
                    message: "Please input surname!",
                  },
                ]}
              >
                <Input />
              </Form.Item>

              <Form.Item
                name="username"
                label="Username"
                rules={[
                  {
                    required: true,
                    message: "Please input username!",
                    whitespace: true,
                  },
                ]}
              >
                <Input />
              </Form.Item>

              <Form.Item
                name="password"
                label="Password"
                rules={[
                  {
                    required: true,
                    message: "Please input your password!",
                  },
                ]}
                hasFeedback
              >
                <Input.Password />
              </Form.Item>

              <Form.Item
                name="confirm"
                label="Confirm Password"
                dependencies={["password"]}
                hasFeedback
                rules={[
                  {
                    required: true,
                    message: "Please confirm your password!",
                  },
                  ({ getFieldValue }) => ({
                    validator(_, value) {
                      if (!value || getFieldValue("password") === value) {
                        return Promise.resolve();
                      }
                      return Promise.reject(
                        new Error(
                          "The two passwords that you entered do not match!"
                        )
                      );
                    },
                  }),
                ]}
              >
                <Input.Password />
              </Form.Item>

              <Form.Item {...tailFormItemLayout}>
                <Button type="primary" htmlType="submit">
                  Register
                </Button>
              </Form.Item>
            </Form>
          {/* </Card> */}
        {/* </Space> */}
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
    RegisterUser: (userInfo) => dispatch(RegisterUser(userInfo))
  })
  
  export default connect(mapStateToProps, mapDispatchToProps)(Registration);
  
