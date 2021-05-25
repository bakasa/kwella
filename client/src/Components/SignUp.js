import { Link } from 'react-router-dom'

const SignUp = () => {
    return (
        <>
            <Link to="/">Home</Link>
            <h2>SignUp</h2>
            <p>
                if you already have an account <Link to="/login">Login</Link>
            </p>
        </>
    )
}

export default SignUp
