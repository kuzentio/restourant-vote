import React from "react";
import axios from "axios";
import Restaurants from "./components/Restaurants";
import {BrowserRouter as Router, Switch, Route} from "react-router-dom";
import RestaurantDetailed from "./components/RestaurantDetailed";

axios.defaults.xsrfHeaderName = "X-CSRFToken";


function App() {
  return (
    <main className="content">
      <Router>
        <Switch>
          <Route exact path="/">
            <Restaurants />
          </Route>
          <Route path="/restaurant/:id" render={(props) => <RestaurantDetailed {...props} /> } >

          </Route>
        </Switch>

      </Router>
    </main>
  );
}

export default App;

