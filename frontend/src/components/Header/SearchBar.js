import React from "react";
import { Link } from "react-router-dom";
import { Layout, Button, Card, Col, Row, Input } from "antd";
const { Search } = Input;


const { Header, Content, Footer, Sider } = Layout;

const SearchBar = ({searchFunc}) => {
    const onSearch = (value) => {
        searchFunc(value);
      };
  return (
    <Content
      style={{
        padding: "10px 0 0 0",
      }}
    >
      <Card bordered={false} style={{}}>
        <Row gutter={14}>
          <Col className="gutter-row" span={6}>
            <Button type="primary">Close</Button>
          </Col>
          <Col className="gutter-row" span={6}>
          <Search
      placeholder="input search text"
      allowClear
      onSearch={onSearch}
      style={{
        width: 200,
      }}
    />
            {/* <MySearch searchFunc={searchFunc}></MySearch> */}
          </Col>
          <Col className="gutter-row" span={6}>
            <Button>Primary Button</Button>
          </Col>
          <Col className="gutter-row" span={6}>
            <Link to="/create_project">
              <Button type="primary">Create Project</Button>
            </Link>
          </Col>
        </Row>
      </Card>
    </Content>
  );
};

export default SearchBar;
