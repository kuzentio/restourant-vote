import React, {Component} from "react";
import Modal from "./Modal";
import axios from "axios";
import {Link} from "react-router-dom";


class Restaurants extends Component {
    constructor(props) {
        super(props);
        this.state = {
            activeItem: {},
            restaurantList: [],
            orderBy: 'recommended'
        };
    }

    componentDidMount() {
        this.refreshList();
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        if (this.state.orderBy !== prevState.orderBy) {
            this.refreshList();
        }
    }

    refreshList = () => {
        const {orderBy} = this.state;
        axios
            .get("/api/restaurant/all/", {params: {'order_by': orderBy}})
            .then(res => this.setState({restaurantList: res.data}))
            .catch(err => console.log(err));
    }

    renderItems = () => {
        return this.state.restaurantList.map(item => (
            <tr key={item.id}>
                <td title={item.id}>{item.id}</td>
                <td title={item.name}>
                    <Link to={"/restaurant/" + item.id}>{item.name}</Link>
                </td>
                <td title={item.city}>{item.city}</td>
                <td title={item.address}>{item.address}</td>
                <td title={item.food_type}>{item.food_type}</td>
                <td title={item.average_rating}>{item.average_rating}</td>
                <td>
                    <button onClick={() => this.editItem(item)} className="btn btn-secondary">
                        {" "}
                        Edit{" "}
                    </button>
                </td>
                <td>
                    <button onClick={() => this.handleDelete(item)} className="btn btn-danger">
                        Delete{" "}
                    </button>
                </td>
            </tr>
        ));
    }

    toggle = () => {
        this.setState({modal: !this.state.modal});
    }

    handleSubmit = item => {
        this.toggle();
        if (item.id) {
            axios
                .put(`/api/restaurant/${item.id}/`, item)
                .then(res => this.refreshList());
            return;
        }
        axios
            .post("/api/restaurant/all/", item)
            .then(res => this.refreshList());
    }

    handleDelete = item => {
        axios
            .delete(`/api/restaurant/${item.id}`)
            .then(res => this.refreshList());
    }

    createItem = item => {
        this.setState({activeItem: item, modal: !this.state.modal});
    }

    editItem = item => {
        this.setState({activeItem: item, modal: !this.state.modal});
    }

    onOrderChange = event => {
        const value = event.target.value;

        this.setState({
            orderBy: value
        });
    }

    render() {
        return (
            <main className="content">
                <h1 className="text-white text-uppercase text-center">Restaurant app</h1>
                <div className="row ">
                    <div className="col-md-6 col-sm-10 mx-auto p-0">
                        <div className="form-group row">
                            <div className="col-xs-2">
                                <button onClick={this.createItem} className="btn btn-primary">
                                    Add restaurant
                                </button>
                            </div>
                            <div className="col-xs-3">
                                <select value={this.state.orderBy} onChange={this.onOrderChange} className={"form-control"}>
                                    <option value="recommended">Top Rated</option>
                                    <option value="default">Newest</option>
                                </select>
                            </div>
                            <table className="table">
                                <thead>
                                <tr>
                                    <th>Restaurant ID</th>
                                    <th>Restaurant Name</th>
                                    <th>Restaurant City</th>
                                    <th>Restaurant Address</th>
                                    <th>Restaurant Type</th>
                                    <th>Restaurant Rating</th>
                                    <th></th>
                                    <th></th>
                                </tr>
                                </thead>
                                <tbody>
                                {this.renderItems()}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
                {this.state.modal && (
                    <Modal
                        activeItem={this.state.activeItem}
                        toggle={this.toggle}
                        onSave={this.handleSubmit}
                    />
                )}
            </main>
        );
    }
}

export default Restaurants;
