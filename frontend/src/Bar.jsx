import './App.css'
function Bar({ logoutFunction, 
               timePeriod, setTimePeriod,
               pollingFrequency, setPollingFrequency,
               filesystemFiltering, setFilesystemFiltering
}) {
    
    const handleTimePeriodChange = (e) => {
        setTimePeriod(e.target.value);
    }
    const handlePollingFrequencyChange = (e) => {
        setPollingFrequency(e.target.value);
    }

    const handleFilesystemFilteringChange = (e) => {
        setFilesystemFiltering(e.target.value === 'true');
    }

    return (
        <div className="bar">
            <label>Show loop devices:
                <select name="filesystemFiltering"
                        id="filesystem-filtering-select"
                        value={filesystemFiltering}
                        onChange={handleFilesystemFilteringChange}>
                    <option value="false">Yes</option>
                    <option value="true">No</option>
                </select>
            </label>
            <label>History period:
                <select name="timePeriod"
                        id="time-period-select"
                        value={timePeriod}
                        onChange={handleTimePeriodChange}>
                    <option value="2">2m</option>
                    <option value="5">5m</option>
                    <option value="10">10m</option>
                    <option value="30">30m</option>
                    <option value="60">60m</option>
                </select>
            </label>
            <label>Polling frequency: 
                <select name="pollingFrequency"
                        id="polling-frequency-select"
                        value={pollingFrequency}
                        onChange={handlePollingFrequencyChange}>
                    <option value="1">1s</option>
                    <option value="5">5s</option>
                    <option value="10">10s</option>
                    <option value="20">20s</option>
                    <option value="30">30s</option>
                </select>
            </label>
            <a className="logoutButton" onClick={logoutFunction}>Log out</a>
        </div>
    )
}


export default Bar;
