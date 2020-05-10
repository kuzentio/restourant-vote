import React, {Component} from "react";
import {
    Button,
    Modal,
    ModalHeader,
    ModalBody,
    ModalFooter,
    Form,
    FormGroup,
    Input,
    Label
} from "reactstrap";

class CustomModal extends Component {
    constructor(props) {
        super(props);
        this.state = {
            activeItem: this.props.activeItem
        }
    }

    handleChange = e => {
        let {name, value} = e.target;
        const activeItem = {...this.state.activeItem, [name]: value};
        this.setState({activeItem});
    }

    render() {
        const {toggle, onSave} = this.props;

        return (
            <Modal isOpen={true} toggle={toggle}>
                <ModalHeader toggle={toggle}> Restaurant </ModalHeader>
                <ModalBody>
                    <Form>
                        <FormGroup>
                            <Label for="name">Restaurant name</Label>
                            <Input
                                type="text"
                                name="name"
                                value={this.state.activeItem.name || ''}
                                onChange={this.handleChange}
                                placeholder="Enter restaurant name"
                            />
                        </FormGroup>
                        <FormGroup>
                            <Label for="city">City</Label>
                            <Input
                                type="text"
                                name="city"
                                value={this.state.activeItem.city}
                                onChange={this.handleChange}
                                placeholder="Enter city"
                            />
                        </FormGroup>
                        <FormGroup>
                            <Label for="address">Address</Label>
                            <Input
                                type="text"
                                name="address"
                                value={this.state.activeItem.address}
                                onChange={this.handleChange}
                                placeholder="Enter restaurant address"
                            />
                        </FormGroup>
                        <FormGroup>
                            <Label for="food_type">Select restaurant type</Label>
                            <select value={this.state.activeItem.food_type || ""} onChange={this.handleChange}
                                    className={"form-control"} name={"food_type"}>
                                <option value=""></option>
                                <option value="Casual">Casual</option>
                                <option value="Fine Dining">Fine Dining</option>
                                <option value="Fast Food">Fast Food</option>
                                <option value="Buffet">Buffet</option>
                                <option value="Pub">Pub</option>
                            </select>
                        </FormGroup>
                    </Form>
                </ModalBody>
                <ModalFooter>
                    <Button color="success" onClick={() => onSave(this.state.activeItem)}>
                        Save
                    </Button>
                </ModalFooter>
            </Modal>
        );
    }
}

export default CustomModal;