import React, { useState } from "react";
import { Button, Layout, List, Modal, Typography } from "antd";
import ProjectModal from "./ProjectModal";
import Search from "../../Header/MySearch";
const { Title } = Typography;

const { Header, Content, Footer, Sider } = Layout;

const mock_users = [
  { title: "Max Ivanov", role: "dev" },
  { title: "Mihail Ro", role: "dev" },
  { title: "Anila Po", role: "dev" },
  { title: "Nono No", role: "dev" },
  { title: "Ayya T1", role: "dev" },
];

const mock_tasks = [
  { title: "Racing car sprays burning fuel into crowd.", index: "TS-1" },
  { title: "Japanese princess to wed commoner.", index: "TS-1" },
  { title: "Australian walks 100km after outback crash.", index: "TS-1" },
  { title: "Man charged over missing wedding girl.", index: "TS-1" },
  { title: "Los Angeles battles huge wildfires.", index: "TS-1" },
];

const Project = (props) => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const showModal = () => {
    setIsModalOpen(true);
  };
  const handleOk = () => {
    setIsModalOpen(false);
  };
  const handleCancel = () => {
    setIsModalOpen(false);
  };

  const [isModalAddOpen, setIsModalAddOpen] = useState(false);
  const showModalAdd = () => {
    setIsModalAddOpen(true);
  };
  const handleAddOk = () => {
    setIsModalAddOpen(false);
  };
  const handleAddCancel = () => {
    setIsModalAddOpen(false);
  };
  return (
    <div>
      <Content
        style={{
          padding: "0 50px",
        }}
      >
        <Title level={2}>Project Title</Title>
        <Title level={4}>Leader</Title><Button onClick={showModalAdd}>Change</Button>
        <Button type="primary" onClick={showModal}>
          Edit
        </Button>
        <Button type="primary">Send Nofication</Button>
        <Button type="primary">Lock</Button>
        <Title level={4}>Status:</Title>
        <Typography.Text mark>OPEN</Typography.Text>

        <List
          header={<div>Participants <Button onClick={showModalAdd}>Add</Button></div>}
          bordered
          dataSource={mock_users}
          renderItem={(item) => (
            <List.Item>
              <Typography.Text mark>{item.role}</Typography.Text> {item.title}
            </List.Item>
          )}
        ></List>

        <List
          header={<div>Tasks</div>}
          bordered
          dataSource={mock_tasks}
          renderItem={(item) => (
            <List.Item>
              <Typography.Text mark>{item.index}</Typography.Text> {item.title}
            </List.Item>
          )}
        ></List>
      </Content>
      <Modal
        title="Close"
        open={isModalOpen}
        onOk={handleOk}
        onCancel={handleCancel}
      >
        <ProjectModal></ProjectModal>
      </Modal>
      <Modal
        title="Close"
        open={isModalAddOpen}
        onOk={handleAddOk}
        onCancel={handleAddCancel}
      >
        <Search></Search>
      </Modal>
    </div>
  );
};

export default Project;
