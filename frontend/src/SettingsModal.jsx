import { Modal } from "@mui/material";
import './App.css';

function SettingsRow ({children, label}) {
    return (
        <div className="settingsRow">
        <span className="barLabel">{label}</span>
            {children}
        </div>
    )
}

function Blob ({name, isActive, activeClassName, inactiveClassName, onClick}) {
    return (
        <span className={isActive ? activeClassName : inactiveClassName} onClick={onClick}>{name}</span>
    )
}

function ElementToggleBlob( {name, isActive, onClick} ) {
    return (
        <Blob name={name} isActive={isActive} onClick={onClick}
              activeClassName="elementToggle elementToggleActive" inactiveClassName="elementToggle elementToggleInactive"
        />
    )
}

function ElementTogglesList({config}) {
    return (
        <>
        <h2>Toggle elements</h2>
        <div className="togglesContainer">
            {Object.keys(config.enabledElements).map((element) => (
                <ElementToggleBlob
                    key={config.enabledElements[element].name}
                    name={config.enabledElements[element].name}
                    isActive={config.enabledElements[element].enabled}
                    onClick={(e) => config.setEnabledElements((prev) => {return {
                        ...prev,
                        [element]: {
                            ...prev[element],
                            enabled: !prev[element].enabled,
                        } ,
                    }})}
                />
            ))}
        </div>
        </>
    )
}

function CleanupPicker({config}) {
    return (
        <SettingsRow label="History retention period (days, 0 to disable)">
            <input type="number"
                   key = {config.settings.retention_peroid}
                   defaultValue={config.settings.retention_period / 24 / 60 / 60}
                   onChange={config.handleRetentionPeriodChange}/>
        </SettingsRow>
    )
}

function SettingsModal ({open, onClose, config})
{
    const handleTimePeriodChange = (e) => {
        config.setTimePeriod(e.target.value);
    }
    const handlePollingFrequencyChange = (e) => {
        config.setPollingFrequency(e.target.value);
    }

    const handleFilesystemFilteringChange = (e) => {
        config.setFilesystemFiltering(e.target.value === 'true');
    }
    return (
        <Modal
            open={open}
            onClose={onClose}
        >
            <div className="settingsModal">
                <h2>Settings</h2>
                <SettingsRow label="Server-side update frequency">
                    <select name="serverSideUpdateFrequency"
                            id="server-side-update-frequency"
                            defaultValue={config.serverSideUpdateFrequency}
                            onChange={config.handleServerSideUpdateFrequencyChange}>
                        <option value="3">3s</option>
                        <option value="5">5s</option>
                        <option value="10">10s</option>
                        <option value="20">20s</option>
                    </select>
            </SettingsRow>
            <SettingsRow label="Show loop devices">
                <select name="filesystemFiltering"
                        id="filesystem-filtering-select"
                        value={config.filesystemFiltering}
                        onChange={handleFilesystemFilteringChange}>
                    <option value="false">Yes</option>
                    <option value="true">No</option>
                </select>
            </SettingsRow>
            <SettingsRow label="History period">
                <select name="timePeriod"
                        id="time-period-select"
                        value={config.timePeriod}
                        onChange={handleTimePeriodChange}>
                    <option value="2">2m</option>
                    <option value="5">5m</option>
                    <option value="10">10m</option>
                    <option value="30">30m</option>
                    <option value="60">60m</option>
                </select>
            </SettingsRow>
            <SettingsRow label="Polling frequency">
                <select name="pollingFrequency"
                        id="polling-frequency-select"
                        value={config.pollingFrequency}
                        onChange={handlePollingFrequencyChange}>
                    <option value="1">1s</option>
                    <option value="5">5s</option>
                    <option value="10">10s</option>
                    <option value="20">20s</option>
                    <option value="30">30s</option>
                </select>
            </SettingsRow>
            <CleanupPicker config={config} />
            <ElementTogglesList config={config} />
            </div>
        </Modal>
    )
}

export default SettingsModal;
