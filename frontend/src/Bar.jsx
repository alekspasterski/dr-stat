import './App.css'
function Bar({ logoutFunction, 
               handleSettingsModalOpen,
}) {
    
    

    return (
        <div className="bar">
            <button
                className="settingsButton"
                onClick={handleSettingsModalOpen}>Settings</button>
            <a className="logoutButton" onClick={logoutFunction}>Log out</a>
        </div>
    )
}


export default Bar;
