import React from 'react'
import { Link } from 'react-router-dom'

const Login = () => {
    return (
        <div>
            <Link to='/'>Home</Link>
            <h1>Login</h1>
            <p>
                Don't have an account yet? <Link to='/signup'>Signup</Link>
            </p>
        </div>
    )
}

export default Login
