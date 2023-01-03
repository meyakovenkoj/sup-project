import React from "react";
import { CopyOutlined } from "@ant-design/icons";
import {
  Typography,
  Input,
  Button,
  Space,
  Layout,
  AutoComplete,
  Cascader,
  DatePicker,
  InputNumber,
  Select,
  TimePicker,
  Tooltip,
  TreeSelect,
  Form,
} from "antd";
import { connect } from "react-redux";
import { createProject } from "../../../redux/actions/actions";
const { Option } = Select;
const { TreeNode } = TreeSelect;
const { Title } = Typography;
const { Header, Content, Footer, Sider } = Layout;

const CreateProject = (props) => {

  const onFinish = (values) => {
    props.createProject(values.title);
    console.log("Success:", values);
  };
  return (
    <div>
      <Layout style={{ height: "100%" }}>
        <Content style={{ padding: "0 50px" }}>
          <Title level={2}>Create Project</Title>
          <Form
              name="basic"
              labelCol={{
                span: 8,
              }}
              wrapperCol={{
                span: 16,
              }}
              onFinish={onFinish}
              autoComplete="off"
            >
              <Form.Item
                label="Title"
                name="title"
                rules={[
                  {
                    required: true,
                    message: "Please input title!",
                  },
                ]}
              >
                <Input />
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
        </Content>
      </Layout>
    </div>
  );
};


const mapStateToProps = (state) => {
  return {
    loading: state.authUser.loading
  }
}

const mapDispatchToProps = (dispatch) => ({
  createProject: (title) => dispatch(createProject(title))
})

export default connect(mapStateToProps, mapDispatchToProps)(CreateProject);
