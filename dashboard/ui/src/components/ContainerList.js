import * as React from "react";
import {
  Row,
  Col,
  ListView,
} from "patternfly-react"

class ContainerList extends React.Component {
  renderItem = (item, index) => {
    return (
      <ListView.Item
        key={item.id}
        actions={<div/>}
        leftContent={<ListView.Icon name="file-text-o" />}
        additionalInfo={[]}
        heading={item.repository}
        description={item.title}
      >
        <Row>
          <Col sm={11}>
            Replace this with some expanded information
          </Col>
        </Row>
      </ListView.Item>
    );
  };

  render() {
    return <ListView>{this.props.containers.map(this.renderItem)}</ListView>;
  }
}

export default ContainerList;
