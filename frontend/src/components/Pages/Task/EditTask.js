import React, { useState } from 'react';
import { Typography } from 'antd';
import { Input } from 'antd';

const { Title } = Typography;
const { TextArea } = Input;

const EditTask = () => (
    <>
        <Title level={5}>Comment</Title>
        <TextArea rows={4} placeholder="maxLength is 6" maxLength={6} />
    </>    

      
  );
export default EditTask;