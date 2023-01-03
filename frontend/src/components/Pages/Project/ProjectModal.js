import React from "react";
import { Typography } from "antd";
import { Input } from "antd";
import { Col, Divider, Row } from "antd";
import { Select } from "antd";

const { Title } = Typography;
const { TextArea } = Input;

const onChange = (value) => {
  console.log(`selected ${value}`);
};
const onSearch = (value) => {
  console.log("search:", value);
};

const ProjectModal = (props) => (
  <>
    <Title level={5}>Title</Title>

    <Input placeholder="Basic usage" />

    <Row>
      <Col>
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
    </Row>

    <Divider></Divider>
  </>
);
export default ProjectModal;
