import React, { useState, useEffect } from "react";
import {useParams} from "react-router-dom"
import { Button, Layout, List, Modal, Typography } from "antd";
import ProjectModal from "./ProjectModal";
import { connect } from "react-redux";
import { getUsers, getProject, changeStatus } from "../../../redux/actions/actions";

const { Title } = Typography;

const { Header, Content, Footer, Sider } = Layout;


const Project = (props) => {
  const {projId} = useParams();
  const projectId = projId ? projId : props.projId;
  useEffect(() => {
    props.getProject(projectId);
  }, []);
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
  const handleCloseProject = () => {
    if (props.project &&  props.project.status == 'open'){
      props.changeStatus('finish', projectId);
    }
  }
  const handleLockProject = () => {
    if (props.project &&  props.project.status == 'closed'){
      props.changeStatus('archive', projectId);
    }
  }
  
  const handleReopenProject = () => {
    if (props.project &&  props.project.status == 'archived'){
      props.changeStatus('reopen', projectId);
    }
  }
  return (
    <div>
      <Content
        style={{
          padding: "0 50px",
        }}
      >
        <Title level={2}>{props.project ? props.project.title : 'Loading'}</Title>
        <Title level={4}>{props.project && props.project.head && props.project.head.user ? props.project.head.user.name +' '+ props.project.head.user.surname : 'Loading'}</Title><Button onClick={showModalAdd}>Change</Button>
        <Button type="primary" onClick={showModal}>
          Edit
        </Button>
        {/* <Button type="primary">Send Nofication</Button> */}
        {props.project &&  props.project.status == 'open' ? <Button type="primary" onClick={handleCloseProject}>Close</Button> : <></>}
        {props.project &&  props.project.status == 'closed'?<Button type="primary" onClick={handleLockProject}>Lock</Button> : <></>}
        {props.project &&  props.project.status == 'archived'?<Button type="primary" onClick={handleReopenProject}>Reopen</Button> : <></>}
        <Title level={4}>Status:</Title>
        <Typography.Text mark>{props.project ? props.project.status : 'Loading'}</Typography.Text>

        <List
          header={<div>Participants <Button onClick={showModalAdd}>Add</Button></div>}
          bordered
          dataSource={props.project && props.project.participants ? props.project.participants : []}
          renderItem={(item) => (
            item && item.user?
            <List.Item>
              <Typography.Text mark>{item.role}</Typography.Text> {item.user.name + ' ' + item.user.surname}
            </List.Item> : <></>
          )}
        ></List>

        <List
          header={<div>Tasks</div>}
          bordered
          dataSource={props.project && props.project.tasks ? props.project.tasks : []}
          renderItem={(item) => (
            <List.Item>
              <Typography.Text mark>{item.id}</Typography.Text> {item.title}
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
        <ProjectModal users={props.users}></ProjectModal>
      </Modal>
      <Modal
        title="Close"
        open={isModalAddOpen}
        onOk={handleAddOk}
        onCancel={handleAddCancel}
      >
        
      </Modal>
    </div>
  );
};

const mapStateToProps = (state) => {
  return {
    loading: state.authUser.loading,
    users: state.authUser.users,
    project: state.authUser.project
  }
}

const mapDispatchToProps = (dispatch) => ({
  getUsers: () => dispatch(getUsers()),
  getProject: (projectId) => dispatch(getProject(projectId)),
  changeStatus: (status, project_id) => dispatch(changeStatus(status, project_id))
})

export default connect(mapStateToProps, mapDispatchToProps)(Project);
