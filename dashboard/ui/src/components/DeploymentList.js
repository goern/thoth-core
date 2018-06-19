import * as React from "react";
import {
    Row,
    Col,
    ListView,
} from "patternfly-react"

class DeploymentList extends React.Component {
    renderItem = (item, index) => {
        return ( <ListView.Item key = { item.id }
            actions = { <div /> }
            leftContent = { <ListView.Icon name = "file-text-o" /> }
            additionalInfo = {
                []
            }
            heading = { item.deploymentName }
            description = {
                item.deploymentName
            }>
            <Row>
                <Col sm={11}>JA! Replace this with some expanded information </Col>
            </Row >
            </ListView.Item>
        );
    };

    render() {
        return <ListView>{ this.props.deployments.map(this.renderItem) }</ListView>;
    }
}

export default DeploymentList;