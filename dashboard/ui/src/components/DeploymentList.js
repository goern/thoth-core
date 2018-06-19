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
            leftContent = { <ListView.Icon name="file-text-o" /> }
            additionalInfo = {
                []
            }
            heading = {
                "Deployment: " + item.deployment.containerName
            }
            description = {
                "build from "+item.deployment.pullRequest.title
            }>
            <Row>
                <Col sm={11}>Image: <em>{item.deployment.image.fullRef}</em><br/>
                    Tags: ... <br />
                    Pods: {
                        item.deployment.name
                    } <br /> <br />
                    This has been build from <b>{ item.deployment.pullRequest.title } </b> 
                    opened by <em>{ item.deployment.pullRequest.user_login }</em>, the PR is <em>{ item.deployment.pullRequest.state }</em>.
                </Col>
            </Row >
            </ListView.Item>
        );
    };

    render() {
        return <ListView>{ this.props.deployments.map(this.renderItem) }</ListView>;
    }
}

export default DeploymentList;