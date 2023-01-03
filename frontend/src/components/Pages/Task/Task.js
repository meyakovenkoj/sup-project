import React, { useState } from "react";
import { Form, Modal } from "antd";
import { DeleteOutlined } from "@ant-design/icons";
import { Breadcrumb, Layout } from "antd";
import Solve from "./Solve";
import UploadFile from "../../utils/UploadFile";
import { Button } from "antd";
import { Col, Row } from "antd";
import { Card } from "antd";
import { Input } from "antd";
import { Typography } from "antd";
import { ArrowDownOutlined, ArrowUpOutlined } from "@ant-design/icons";
import { ExclamationCircleFilled } from "@ant-design/icons";
import { Statistic } from "antd";
import EditComment from "./EditComment";
import EditTask from "./EditTask";
import { connect } from "react-redux";
import { addComment, deleteComment, editComment } from "../../../redux/actions/actions";
const { Title } = Typography;
const { confirm } = Modal;
const { TextArea } = Input;



const { Meta } = Card;

const { Header, Content, Footer, Sider } = Layout;
const Comment = ({data, edit, deleteComment}) => {
    return (data ? <div>
    {data.map(comment => (
      <Card
      type="inner"
      title="User 1"
      extra={
        <div>
          <Button type="primary" onClick={() => {edit(comment)}}>
            Edit
          </Button>
          <DeleteOutlined key="delete" onClick={() => {deleteComment(comment)}} />
        </div>
      }
    >
      <p>{comment}</p>
    </Card>
    ))}
  </div> : <></>);
}; 

const Task = (props) => {
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

  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const deleteShowModal = () => {
    setIsDeleteModalOpen(true);
  };
  const handleOkDelete = () => {
    props.deleteComment()
    setIsDeleteModalOpen(false);
  };
  const handleCancelDelete = () => {
    setIsDeleteModalOpen(false);
  };
  const [currentComment, setCurrentComment] = useState({id:'', text:''});
  const setCommentId = (id) => {
    setCurrentComment({...currentComment, id:id});
  }
  const setCommentText = (text) => {
    setCurrentComment({...currentComment, text:text.value});
  }

  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const editShowModal = (id) => {
    // setCommentId(id);
    setIsEditModalOpen(true);
  };
  const handleOkEdit = () => {
    // props.editComment(currentComment)
    setIsEditModalOpen(false);
  };
  const handleCancelEdit = () => {
    setIsEditModalOpen(false);
  };

  const [isEditTaskModalOpen, setIsEditTaskModalOpen] = useState(false);
  const editTaskShowModal = () => {
    setIsEditTaskModalOpen(true);
  };
  const handleOkEditTask = () => {
    setIsEditTaskModalOpen(false);
  };
  const handleCancelEditTask = () => {
    setIsEditTaskModalOpen(false);
  };

  const processFiles = () => {
    var files = [];
    if (props.data.files) {

        props.data.files.forEach(item => {
        var title = item.split('/');
        var elem = {
            name: title[0],
            status: "done",
            url: item
        };
            files.push(elem);
        });
    }
    return files;
  }

  const showDeleteConfirm = (comment_id) => {
    confirm({
      title: "Are you sure delete this task?",
      icon: <ExclamationCircleFilled />,
      content: "Some descriptions",
      okText: "Yes",
      okType: "danger",
      cancelText: "No",
      onOk() {
        props.deleteComment(comment_id);
        console.log("OK");
      },
      onCancel() {
        console.log("Cancel");
      },
    });
  };

  const onFinish = (values) => {
    props.addComment(props.data._id, values.text)
  };

  return (
    <div>
      <Content
        style={{
          padding: "0 50px",
        }}
      >
        <Breadcrumb
          style={{
            margin: "16px 0",
          }}
        >
          <Breadcrumb.Item>Home</Breadcrumb.Item>
          <Breadcrumb.Item>List</Breadcrumb.Item>
          <Breadcrumb.Item>App</Breadcrumb.Item>
        </Breadcrumb>

        <Title level={2}>{props.data.title}</Title>
        <Row gutter={14}>
          <Col className="gutter-row" span={6}>
            <Button type="primary" onClick={showModal}>
              Solve
            </Button>
          </Col>
          <Col className="gutter-row" span={6}></Col>
          <Col className="gutter-row" span={6}>
            <Button onClick={editTaskShowModal}>Edit</Button>
          </Col>
          <Col className="gutter-row" span={6}>
            <Button type="primary">Subscribe</Button>
          </Col>
        </Row>
        <Row gutter={14}>
          <Col className="gutter-row" span={6}>
            <Button disabled>Move to test</Button>
          </Col>
        </Row>

        <Row gutter={22}>
          <Col className="gutter-row" span={16}>
            <Card title="Card title НАСТЯ" bordered={false} style={{}}>
              <p>{props.data.description}</p>
            </Card>
            <Card>
              <UploadFile files={processFiles()}></UploadFile>
            </Card>
            <Card>
                <Comment data={props.data.comments} edit={editShowModal} deleteComment={(id) => {showDeleteConfirm(id)}}></Comment>
              {/*  */}
              <br></br>
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
                label="Comment"
                name="text"
                rules={[
                  {
                    required: true,
                    message: "Please input comment!",
                  },
                ]}
              >
                <TextArea rows={4} placeholder="maxLength is 256" maxLength={256} />
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
              {/* <TextArea rows={4} placeholder="maxLength is 6" maxLength={6} />
              <Button type="primary">Send</Button> */}
            </Card>
          </Col>
          <Col className="gutter-row" span={8}>
            <Card title="Card title" bordered={false} style={{}}>
              <p>Author: {props.data.author}</p>
              <p>Checker: {props.data.checker}</p>
              <p>Date: {props.data.changed}</p>
            </Card>

            <Row>
              <Col span={12}>
                <Card>
                  <Statistic
                    title="Active"
                    value={11.28}
                    precision={2}
                    valueStyle={{
                      color: "#3f8600",
                    }}
                    prefix={<ArrowUpOutlined />}
                    suffix="%"
                  />
                </Card>
              </Col>
              <Col span={12}>
                <Card>
                  <Statistic
                    title="Idle"
                    value={9.3}
                    precision={2}
                    valueStyle={{
                      color: "#cf1322",
                    }}
                    prefix={<ArrowDownOutlined />}
                    suffix="%"
                  />
                </Card>
              </Col>
            </Row>
          </Col>
        </Row>
        <br />
        <br />
      </Content>

      <Modal
        title="Solve"
        open={isModalOpen}
        onOk={handleOk}
        onCancel={handleCancel}
      >
        <Solve></Solve>
      </Modal>
      <Modal
        title="Are you sure to delete?"
        open={isDeleteModalOpen}
        onOk={handleOkDelete}
        onCancel={handleCancelDelete}
      ></Modal>
      <Modal
        title="Edit"
        open={isEditModalOpen}
        onOk={handleOkEdit}
        onCancel={handleCancelEdit}
      >
        <EditComment edit={setCommentText}></EditComment>
      </Modal>
      <Modal
        title="Edit"
        open={isEditTaskModalOpen}
        onOk={handleOkEditTask}
        onCancel={handleCancelEditTask}
      >
        <EditTask></EditTask>
      </Modal>
    </div>
  );
};

const mapStateToProps = (state) => {
    return {
      loading: state.authUser.loading
    }
  }
  
  const mapDispatchToProps = (dispatch) => ({
  addComment: (task_id, text) => dispatch(addComment(task_id, text)),
  deleteComment: (comment_id) => dispatch(deleteComment(comment_id)),
  editComment: (comment_id, text) => dispatch(editComment(comment_id, text))
  })
  
  export default connect(mapStateToProps, mapDispatchToProps)(Task);
