import React from "react";
import { Typography } from "antd";
import { Input } from "antd";
import { Col, Divider, Row } from "antd";
import { Select } from "antd";
import UploadFile from "../../utils/UploadFile";
import { createTask } from "../../../redux/actions/actions";
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
  const state = {
    title: '',
    description: '',
    type: '',
    project_id: '',
  }
  return (
  <>
    <Title level={5}>Title</Title>

    <Input placeholder="Basic usage" />
    <Title level={5}>Task</Title>

    <TextArea rows={6} placeholder="maxLength is 6" maxLength={6} />

    <Row>
      <Col>
        <Title level={5}>Project</Title>

        <Select
          showSearch
          placeholder="Select status"
          optionFilterProp="children"
          onChange={onChange}
          onSearch={onSearch}
          filterOption={(input, option) =>
            (option?.label ?? "").toLowerCase().includes(input.toLowerCase())
          }
          options={[
            {
              value: "solve",
              label: "Solve",
            },
            {
              value: "wontfixed",
              label: "Won't Fixed",
            },
            {
              value: "closed",
              label: "Closed",
            },
          ]}
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
            (option?.label ?? "").toLowerCase().includes(input.toLowerCase())
          }
          options={[
            {
              value: "solve",
              label: "Solve",
            },
            {
              value: "wontfixed",
              label: "Won't Fixed",
            },
            {
              value: "closed",
              label: "Closed",
            },
          ]}
        />
      </Col>
      <Col>
        <Title level={5}>Type</Title>

        <Select
          showSearch
          placeholder="Select status"
          optionFilterProp="children"
          onChange={onChange}
          onSearch={onSearch}
          filterOption={(input, option) =>
            (option?.label ?? "").toLowerCase().includes(input.toLowerCase())
          }
          options={[
            {
              value: "solve",
              label: "Solve",
            },
            {
              value: "wontfixed",
              label: "Won't Fixed",
            },
            {
              value: "closed",
              label: "Closed",
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
    loading: state.authUser.loading
  }
}

const mapDispatchToProps = (dispatch) => ({
  createTask: (title, description, type, project_id) => dispatch(createTask(title, description, type, project_id))
})

export default connect(mapStateToProps, mapDispatchToProps)(TaskModal);
