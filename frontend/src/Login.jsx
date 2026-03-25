import { useState, useEffect } from 'react'
function Login({ setToken }) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [loginFailed, setLoginFailed] = useState("");

    const handleSubmit = (e) => {
        e.preventDefault();
        fetchAPIToken(username, password)
    }

    const fetchAPIToken = (username, password) => {
        fetch("/sysmon/token/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            credentials: "include",
            body: JSON.stringify({
                "username": username,
                "password": password,
            })
        })
            .then(response => {
                if (response.ok) {
                    return response.json();
                }
                else {
                    setLoginFailed("Invalid username or password.");
                    throw new Error("credentials_rejected");
                }
            })
            .then(data => {
                setToken(data.access);
                setLoginFailed("");
            })
            .catch(err => {
                if (err.message !== "credentials_rejected") {
                    setLoginFailed("Cannot reach the server. Please try again later.")
                }
                console.error(err);
            })
    }

    return (
        <>
            {loginFailed && (
                <div className="loginError"><p>{loginFailed}</p></div>
            )}
            <div className="loginModal">
                <p>Log in:</p>
                <form className="loginForm" onSubmit={handleSubmit}>
                    <input placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} name="username" />
                    <input placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} name="password" type="password" />
                    <button type="submit">Log In</button>
                </form>
            </div>
        </>
    );
}

export default Login;
