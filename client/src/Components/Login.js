import React from 'react'
import { Link } from 'react-router-dom'

function Login() {
    return (
        <>
          <Link to="/">Home</Link>  
          <p>
              Don't have an account? <Link to="/signup">SignUp</Link>
          </p>
        </>
    )
}

export default Login
