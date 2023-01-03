import React, { useLayoutEffect, useState } from "react";
import { Typography } from "antd";
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
    props.getUsers();
    props.getProjects();
  }, []);

  const [project_id, setProjectID] = useState('');
  const [title, setTaskTitle] = useState('');
  const [description, setTaskDescription] = useState('');
  const [type, setTaskType] = useState('');

  const handleTitle = (value) => {
    setTaskTitle(value);
  }

  return (
  <>
    <Title level={5}>Title</Title>

    <Input placeholder="Basic usage" onChange={handleTitle} />
    <Title level={5}>Task</Title>

    <TextArea rows={6} placeholder="maxLength is 256" maxLength={256} onChange={(value) => {setTaskDescription(value)}}/>

    <Row>
      <Col>
        <Title level={5}>Project</Title>

        <Select
          showSearch
          placeholder="Select status"
          optionFilterProp="children"
          onChange={(value) => {setProjectID(value._id)}}
          onSearch={onSearch}
          filterOption={(input, option) =>
            (option?.title ?? "").toLowerCase().includes(input.toLowerCase())
          }
          options={props.projects}
        />
      </Col>
      <Col>
        <Title level={5}>Worker</Title>

        <Select
          showSearch
          placeholder="Select status"
          optionFilterProp="children"
          onChange={onChange}
          onSearch={onSearch}
          filterOption={(input, option) =>
            (option?.username ?? "").toLowerCase().includes(input.toLowerCase())
          }
          options={props.users}
        />
      </Col>
      <Col>
        <Title level={5}>Type</Title>

        <Select
          showSearch
          placeholder="Select status"
          optionFilterProp="children"
          onChange={(value) => {setTaskType(value)}}
          onSearch={onSearch}
          filterOption={(input, option) =>
            (option?.label ?? "").toLowerCase().includes(input.toLowerCase())
          }
          options={[
            {
              value: "bug",
              label: "Bug",
            },
            {
              value: "error",
              label: "Error",
            },
            {
              value: "note",
              label: "Note",
            },
          ]}
        />
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
