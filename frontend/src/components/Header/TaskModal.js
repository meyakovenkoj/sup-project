import React, { useState } from 'react';
import { Button, Modal } from 'antd';
import { Space } from 'antd';
import { Typography } from 'antd';
import { Input } from 'antd';
import { Col, Divider, Row } from 'antd';
import { Select } from 'antd';
import UploadFile from '../utils/UploadFile';

const { Title } = Typography;
const { TextArea } = Input;

const onChange = (value) => {
  console.log(`selected ${value}`);
};
const onSearch = (value) => {
  console.log('search:', value);
};

const TaskModal = () => (
    <>              

                    <Title level={5}>Title</Title>

                    <Input placeholder="Basic usage" />
      <Title level={5}>Task</Title>

      <TextArea rows={6} placeholder="maxLength is 6" maxLength={6} />

  <UploadFile></UploadFile>
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
(option?.label ?? '').toLowerCase().includes(input.toLowerCase())
}
options={[
{
  value: 'solve',
  label: 'Solve',
},
{
  value: 'wontfixed',
  label: 'Won\'t Fixed',
},
{
  value: 'closed',
  label: 'Closed',
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
(option?.label ?? '').toLowerCase().includes(input.toLowerCase())
}
options={[
{
  value: 'solve',
  label: 'Solve',
},
{
  value: 'wontfixed',
  label: 'Won\'t Fixed',
},
{
  value: 'closed',
  label: 'Closed',
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
(option?.label ?? '').toLowerCase().includes(input.toLowerCase())
}
options={[
{
  value: 'solve',
  label: 'Solve',
},
{
  value: 'wontfixed',
  label: 'Won\'t Fixed',
},
{
  value: 'closed',
  label: 'Closed',
},
]}
/>
    </Col>
</Row>

<Divider></Divider>
    </>
  );
export default TaskModal;