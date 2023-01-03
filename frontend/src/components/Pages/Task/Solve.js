import React, { useState } from 'react';
import { Button, Modal } from 'antd';
import { Space } from 'antd';
import { Typography } from 'antd';
import { Input } from 'antd';
import { Col, Divider, Row } from 'antd';
import { Select } from 'antd';

const { Title } = Typography;
const { TextArea } = Input;

const onChange = (value) => {
  console.log(`selected ${value}`);
};
const onSearch = (value) => {
  console.log('search:', value);
};

const Solve = () => (
    <>              

                    <Title level={5}>Comment</Title>

      <TextArea rows={4} placeholder="maxLength is 6" maxLength={6} />
      <Title level={5}>Testing Plan</Title>

      <TextArea rows={4} placeholder="maxLength is 6" maxLength={6} />
      <Title level={5}>Tester</Title>

      <Select
    showSearch
    placeholder="Select a person"
    optionFilterProp="children"
    onChange={onChange}
    onSearch={onSearch}
    filterOption={(input, option) =>
      (option?.label ?? '').toLowerCase().includes(input.toLowerCase())
    }
    options={[
      {
        value: 'jack',
        label: 'Jack',
      },
      {
        value: 'lucy',
        label: 'Lucy',
      },
      {
        value: 'tom',
        label: 'Tom',
      },
    ]}
  />

<Title level={5}>Status</Title>

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
<Divider></Divider>
    </>
  );
export default Solve;