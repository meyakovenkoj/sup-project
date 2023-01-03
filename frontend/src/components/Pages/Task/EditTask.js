import React, { useLayoutEffect } from "react";
import { Button, Form, Select, Typography } from "antd";
import { Input } from "antd";
import { connect } from "react-redux";
import { addComment, getUsers, setTaskExecutor, setTaskTester } from "../../../redux/actions/actions";

const { Title } = Typography;
const { TextArea } = Input;

const EditTask = (props) => {

    const onChange = (value) => {
        console.log(`selected ${value}`);
      };

    useLayoutEffect(() => {
        props.getUsers();
      }, []);
      const onFinish = (values) => {
        if (values.comment){
            props.addComment(props.task_id, values.comment )
        }
          if (values.executor){
              props.setTaskExecutor(props.task_id, values.executor)
          }
          if (values.tester){
              props.setTaskTester(props.task_id, values.tester)
          }
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
                    label="Executor"
                    name="executor"
                  >
                        <Select
          showSearch
          placeholder="Select executor"
          optionFilterProp="children"
          onChange={onChange}
          filterOption={(input, option) =>
            (option?.username ?? "").toLowerCase().includes(input.toLowerCase())
          }
          options={props.users}
        />
                  </Form.Item>

                  <Form.Item
                    label="Tester"
                    name="tester"
                  >
                        <Select
          showSearch
          placeholder="Select tester"
          optionFilterProp="children"
          onChange={onChange}
          filterOption={(input, option) =>
            (option?.username ?? "").toLowerCase().includes(input.toLowerCase())
          }
          options={props.users}
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
    getUsers: () => dispatch(getUsers()),
  addComment: (task_id, text) => dispatch(addComment(task_id, text)),
  setTaskExecutor: (task_id, pp_id) => dispatch(setTaskExecutor(task_id, pp_id)),
  setTaskTester: (task_id, pp_id) => dispatch(setTaskTester(task_id, pp_id)),
  })
  
  export default connect(mapStateToProps, mapDispatchToProps)(EditTask);