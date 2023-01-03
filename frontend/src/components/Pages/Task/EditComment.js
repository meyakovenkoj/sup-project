import React from "react";
import { Typography } from "antd";
import { Input } from "antd";

const { Title } = Typography;
const { TextArea } = Input;

const EditComment = ({edit}) => (
  <>
    <Title level={5}>Comment</Title>
    <TextArea rows={4} placeholder="maxLength is 6" maxLength={6} onChange={edit}/>
  </>
);
export default EditComment;
