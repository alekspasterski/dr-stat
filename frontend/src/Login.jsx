
import { useState, useEffect } from 'react'
function Login({action, loginFailed}) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const handleSubmit = (e) => {
        e.preventDefault();
        action(username, password)
    }
    return (
        <div className="loginModal">
            <p>Log in:</p>
            <form className="loginForm" onSubmit={handleSubmit}>
                <input placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} name="username" />
                <input placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} name="password" type="password" />
                <button type="submit">Log In</button>
            </form>
        </div>
    );
}

export default Login;
