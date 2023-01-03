import React, { useLayoutEffect, useState } from "react";
import { Form, Typography, Button } from "antd";
import { Input } from "antd";
import { Col, Divider, Row } from "antd";
import { Select } from "antd";
import UploadFile from "../../utils/UploadFile";
import { createTask, getProjects, getUsers } from "../../../redux/actions/actions";
import { connect } from "react-redux";

const { Title } = Typography;
const { TextArea } = Input;

const onChange = (value) => {
  console.log(`selected ${value}`);
};
const onSearch = (value) => {
  console.log("search:", value);
};


const TaskModal = (props) => {
  useLayoutEffect(() => {
    props.getProjects();
  }, []);

  const [project_id, setProjectID] = useState('');
  const [projectName, setProjectName] = useState('');
  const [title, setTaskTitle] = useState('');
  const [description, setTaskDescription] = useState('');
  const [type, setTaskType] = useState('');

  const handleTitle = (value) => {
    setTaskTitle(value);
  }
  const onFinish = (values) => {
    props.createTask(values.title, values.description, values.type, values.project.value)
    console.log("Success:", values);
  };

  const handleProject = (value) => {
    setProjectID(value._id);
    setProjectName(value.title);
  }

  return (
  <>
    <Row>
      <Col>
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
                label="Description"
                name="description"
              >
                <TextArea />
              </Form.Item>

              <Form.Item
                label="Project"
                name="project"
              >
                <Select
          labelInValue
          placeholder="Select project"
          optionFilterProp="children"
          onSelect={handleProject}
          filterOption={(input, option) =>
            (option?.title ?? "").toLowerCase().includes(input.toLowerCase())
          }
          options={props.projects}
          value={projectName}
        />
              </Form.Item>

              <Form.Item
                label="Type"
                name="type"
              >
                <Select
          showSearch
          placeholder="Select type"
          optionFilterProp="children"
          filterOption={(input, option) =>
            (option?.label ?? "").toLowerCase().includes(input.toLowerCase())
          }
          options={[
            {
              value: "bug",
              label: "Bug",
            },
            {
              value: "task",
              label: "Task",
            },
            {
              value: "feature",
              label: "Feature",
            },
            {
              value: "story",
              label: "Story",
            },
          ]}
        />
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
   
      </Col>
    </Row>

    <Divider></Divider>
  </>
);
};

const mapStateToProps = (state) => {
  return {
    loading: state.authUser.loading,
    users: state.authUser.users,
    projects: state.authUser.projects

  }
}

const mapDispatchToProps = (dispatch) => ({
  getProjects: () => dispatch(getProjects()),
  getUsers: () => dispatch(getUsers()),
  createTask: (title, description, type, project_id) => dispatch(createTask(title, description, type, project_id))
})

export default connect(mapStateToProps, mapDispatchToProps)(TaskModal);
