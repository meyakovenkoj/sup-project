import React from "react";
import { Col, List, Row, Layout, Card, Input, Typography } from "antd";
import { connect } from "react-redux";

const { Meta } = Card;
const { Header, Content, Footer, Sider } = Layout;

const People = ({ data }) => {

  return (
    <div>
      <Content
        style={{
          padding: "0 50px",
        }}
      >
        <Row gutter={16}>
          <Col>
            <Card
              hoverable
              style={{
                width: 240,
              }}
              cover={
                <img
                  alt="example"
                  src="https://cs7.pikabu.ru/post_img/big/2019/03/26/11/1553625291161446207.jpg"
                />
              }
            >
              <Meta
                title={<div>{data.name} {data.surname}</div>}
              />
            </Card>
          </Col>
          <Col>
                  <Typography.Text mark>[ITEM]</Typography.Text> {data.username}
                  <List
              header={<div>Projects</div>}
              bordered
              dataSource={data.projects}
              renderItem={(item) => (
                <List.Item>
                  <Typography.Text mark>[ITEM]</Typography.Text> {item}
                </List.Item>
              )}
            />

          </Col>
        </Row>
      </Content>
    </div>
  );
};

const mapStateToProps = (state) => {
  return {
    loading: state.authUser.loading
  }
}

const mapDispatchToProps = (dispatch) => ({
})

export default connect(mapStateToProps, mapDispatchToProps)(People);
