import React, { Component } from 'react';
import { HashRouter as Router, Route, Redirect } from "react-router-dom";
import './App.css';
import Nav from './Nav';
import Main from './Main';
import ATLchart_date from './ATLchart_date'
import ATLchart_month from './ATLchart_month'
import ATLchart_year from './ATLchart_year'
import DayAheadchart_month from './DayAheadchart_month'
import DayAheadchart_year from './DayAheadchart_year'
import DayAheadchart_date from './DayAheadchart_date'
import AggregatedDate from './AggregatedDate'
import AggregatedMonth from './AggregatedMonth'
import AggregatedYear from './AggregatedYear'
import ATLvsForecastchart_date from './ATLvsForecastchart_date';
import ATLvsForecastchart_month from './ATLvsForecastchart_month';
import ATLvsForecastchart_year from './ATLvsForecastchart_year';
//import Europe from './europe-23571_1280.png'

import Footer from './Footer';
import ATL from './ATL';
import { Login, Logout } from './Auth';
import { UserProvider } from './UserContext';
import Europe from "./europe-23571_1280.png";

class App extends Component {

  constructor(props) {
    super(props)
    this.state = {
      token: props.userData.token,
      username: props.userData.username,
      style: {
        backgroundColor:'#fff',
        height:'10vh'
      },
      setUserData: (token, username) => this.setState({
        token: token,
        username: username
      }),
    };
  }

  renderProtectedComponent(ProtectedComponent) {
    if (this.state.username !== null) {
      return  (props) => <ProtectedComponent {...props} />;
    }
    else {
      return (props) => <Redirect to='/login' />;
    }
  }

  render() {
    return (
        <div style={this.state.style}>
          <UserProvider value={this.state}>
            <Router>
              <div className='container'>
                <Nav />
                <Route path="/" exact render={(props) => {
                  return <h1>Καλωσήρθες {this.state.username === null? '' : this.state.username}!<br></br><br></br><img src={Europe} className="photo"></img></h1>;

                }}/>
                <Route path="/main" render={this.renderProtectedComponent(Main)} />
                <Route path="/login" component={Login} />
                <Route path="/logout" render={this.renderProtectedComponent(Logout)} />
                <Route path="/ATL" render={this.renderProtectedComponent(ATL)} />
                <Route path="/ATLchart_date" render={this.renderProtectedComponent(ATLchart_date)} />
                <Route path="/ATLchart_month" render={this.renderProtectedComponent(ATLchart_month)} />
                <Route path="/ATLchart_year" render={this.renderProtectedComponent(ATLchart_year)} />
                <Route path="/DayAheadchart_month" render={this.renderProtectedComponent(DayAheadchart_month)} />
                <Route path="/DayAheadchart_year" render={this.renderProtectedComponent(DayAheadchart_year)} />
                <Route path="/DayAheadchart_date" render={this.renderProtectedComponent(DayAheadchart_date)} />
                <Route path="/ATLvsForecastchart_date" render={this.renderProtectedComponent(ATLvsForecastchart_date)} />
                <Route path="/ATLvsForecastchart_month" render={this.renderProtectedComponent(ATLvsForecastchart_month)} />
                <Route path="/ATLvsForecastchart_year" render={this.renderProtectedComponent(ATLvsForecastchart_year)} />
                <Route path="/AggregatedYear" render={this.renderProtectedComponent(AggregatedYear)} />
                <Route path="/AggregatedDate" render={this.renderProtectedComponent(AggregatedDate)} />
                <Route path="/AggregatedMonth" render={this.renderProtectedComponent(AggregatedMonth)} />
                <Footer />
              </div>
            </Router>
          </UserProvider>
        </div>
    );
  }
}

export default App;
