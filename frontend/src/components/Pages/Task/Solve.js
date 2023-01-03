import React from "react";
import { Select, Divider, Input, Typography, Form, Button } from "antd";
import { addComment, changeStatusTask, getUsers } from "../../../redux/actions/actions";
import { connect } from "react-redux";

const { Title } = Typography;
const { TextArea } = Input;

const onChange = (value) => {
  console.log(`selected ${value}`);
};
const onSearch = (value) => {
  console.log("search:", value);
};


const Solve = (props) => {
  const onFinish = (values) => {
    props.addComment(props.task_id, values.comment )
    props.changeStatusTask(values.status, props.task_id)
    console.log("Success:", values);
  };
  return (
  <>
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
                name="comment"
              >
                <Input />
              </Form.Item>

              <Form.Item
                label="Status"
                name="status"
              >
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
          value: "reopen",
          label: "Reopen",
        },
        {
          value: "verify",
          label: "Ready",
        },
        {
          value: "request_correction",
          label: "Verification",
        },
        {
          value: "finish",
          label: "Finish",
        },
        {
          value: "close",
          label: "Close",
        },
      ]}
    />
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


    <Divider></Divider>
  </>
);
    };

const mapStateToProps = (state) => {
  return {
    loading: state.authUser.loading,
    users: state.authUser.users,

  }
}

const mapDispatchToProps = (dispatch) => ({
  addComment: (task_id, text) => dispatch(addComment(task_id, text)),
  getUsers: () => dispatch(getUsers()),
  changeStatusTask: (task_status, task_id ) => dispatch(changeStatusTask(task_status, task_id ))
})

export default connect(mapStateToProps, mapDispatchToProps)(Solve);
