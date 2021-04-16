import React from 'react'
import { Link } from 'react-router-dom'

const Signup = () => {
    return (
        <>
           <Link to='/'>Home</Link> 
            <h1>Signup</h1>
            <p>
                Already have an account? <Link to='/login'>Login</Link>
            </p>
        </>
    )
}

export default Signup
