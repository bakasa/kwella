import React from "react";
import { Route, Switch } from "react-router";
import { Link } from "react-router-dom";
import './App.css'
import Login from "./components/Login";
import Signup from "./components/Signup";

function App() {
  return (
    <Switch>
      <Route exact path='/' render={ () => (
        <div>
          <h1>KWELLA</h1>
          <Link to='/signup'>Signup</Link>
          <Link to='/login'>Login</Link>
        </div>
      )} />
      <Route path='/signup' component={Signup} />
      <Route path='/login' component={Login} />
    </Switch>
  );
}

export default App;
