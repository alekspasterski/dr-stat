import './App.css'
function Bar({logoutFunction}) {

    return (
        <div className="bar">
            <a className="logoutButton" onClick={logoutFunction}>Log out</a>
        </div>
    )
}


export default Bar;
