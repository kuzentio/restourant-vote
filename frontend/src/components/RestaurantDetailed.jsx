import React from "react";
import axios from "axios";
import {Button, Form, FormGroup, Input, Label} from "reactstrap";
import {Link} from "react-router-dom";


class RestaurantDetailed extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            restaurantReview: {
                rating: null,
                review: null
            }
        }
    }

    componentDidMount() {
        const {id} = this.props.match.params;
        this.loadRestaurant(id)
        this.loadRestaurantReview(id)
    }

    loadRestaurant(id) {
        axios
            .get(`/api/restaurant/${id}/`,)
            .then(res => this.setState({restaurantInfo: res.data}))
            .catch(err => console.log(err));
    }

    async loadRestaurantReview(id) {
        const res = await axios
            .get(`/api/user-rating/${id}/`,)
            .catch(err => console.log(err));
        if (res) {
            this.setState({restaurantReview: res.data})
        }
    }

    handleReviewChange = e => {
        let {name, value} = e.target;
        const restaurantReview = {...this.state.restaurantReview, [name]: value};
        this.setState({restaurantReview});
    }

    handleSubmitReview = item => {
        item.restaurant = this.state.restaurantInfo.id
        axios
            .post(`/api/user-rating/${this.state.restaurantInfo.id}/`, item)
            .then(res => this.loadRestaurantReview(this.state.restaurantInfo.id));
        this.props.history.push(`/`)
        window.location.reload();
    }

    render() {
        const {restaurantInfo} = this.state;
        const {restaurantReview} = this.state;
        if (!restaurantInfo) {
            return (
                <div>loading</div>
            )
        }
        const isAbleToSend =
            this.state.restaurantReview.rating &&
            this.state.restaurantReview.review;

        return (
            <div className={"container"}>
                <p><Link to={"/"}>Getting back to list of restaurants</Link></p>
                <br/>
                <h1>Restaurant detailed page for {restaurantInfo.name}</h1>
                <h4>Restaurant name - {restaurantInfo.name}</h4>
                <h4>Restaurant type - {restaurantInfo.food_type}</h4>
                <h4>Restaurant city - {restaurantInfo.city}</h4>
                <h4>Restaurant address - {restaurantInfo.address}</h4>
                <p></p>
                <h3>Please leave your feedback below</h3>
                <br/>
                <Form>
                    <FormGroup>
                        <Label for="rating">Select stars for restaurant below</Label>
                        <select value={restaurantReview.rating} onChange={this.handleReviewChange}
                                className={"form-control"} name={"rating"}>
                            <option value="1">1</option>
                            <option value="2">2</option>
                            <option value="3">3</option>
                            <option value="4">4</option>
                            <option value="5">5</option>
                        </select>
                    </FormGroup>
                    <FormGroup>
                        <Label for="name">Restaurant review</Label>
                        <Input
                            type="text"
                            name="review"
                            value={restaurantReview.review || ''}
                            onChange={this.handleReviewChange}
                            placeholder="Enter restaurant review"
                        />
                    </FormGroup>
                    <Button onClick={() => this.handleSubmitReview(restaurantReview)} className="btn btn-success" disabled={!isAbleToSend}>
                        Save
                    </Button>
                </Form>
            </div>
        )
    }
}

export default RestaurantDetailed;
