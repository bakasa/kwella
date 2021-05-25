import { Route, Link, Switch } from 'react-router-dom'
import Login from './Components/Login'
import SignUp from './Components/SignUp'


function App() {
  return (
    <Switch>
      <Route exact path='/' render={() => (
        <>
          <h1>Welcome to Kwella</h1>
          <Link to="/signup">SignUp</Link>
          <Link to="/login">Login</Link>
        </>
      )} />

      <Route path="/signup" render={ SignUp } />
      <Route path="/login" render={ Login } />
    </Switch>
  );
}

export default App;
