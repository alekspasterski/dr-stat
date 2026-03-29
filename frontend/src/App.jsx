import { useState, useEffect } from 'react'
import './App.css'
import InfoCard from './InfoCard.jsx'
import Bar from './Bar.jsx'
import SettingsModal from './SettingsModal.jsx'
import Login from './Login.jsx'
import { ThemeProvider, createTheme } from '@mui/material/styles';
import MemoryCard from './MemoryCard.jsx'
import CpuCard from './CpuCard.jsx'
import DisksCard from './DisksCard.jsx'
import TimeCard from './TimeCard.jsx'
import MemoryChartWidget from './MemoryChartWidget.jsx'
import CpuChartWidget from './CpuChartWidget.jsx'
import DiskChartWidget from './DiskChartWidget.jsx'
import useSystemData from './useSystemData.jsx'
import { refreshAPIToken, authenticatedFetch } from './utils.js'

const darkTheme = createTheme({
    palette: {
        mode: 'dark',
    },
});

function App() {
    // State for login
    const [token, setToken] = useState("");
    const [isCheckingAuth, setIsCheckingAuth] = useState(true)
    // State for the modal windows
    const [settingsModalOpen, setSettingsModalOpen] = useState(false);
    // State for the API calls
    const { memory, cpu, disks, systemInfo, config } = useSystemData(token, setToken);

    // Check if we have a valid refresh token in cookies
    useEffect(() => {
        refreshAPIToken(setToken).finally(() => {
            setIsCheckingAuth(false);
        })
    }, []) // Run only once
    const loggedIn = Boolean(token);

    const logout = () => authenticatedFetch(
        token, "/sysmon/logout", 'GET',
    ).then(() => { setToken("") })

    if (!loggedIn) {
        return (
            <Login setToken={setToken} />
        )
    }

    if (isCheckingAuth || memory.length === 0 || cpu.length === 0 || disks.length === 0 || Object.keys(systemInfo).length === 0) {
        return (<div className="loader"></div>)
    }

    const disksToDisplay = disks.filter((disk) => {
        return config.filesystemFiltering ? disk.type !== 'LOOP' && !disk.device.includes('loop') : true
    }).filter(disk => (disk.active === true));

    if (loggedIn) {
        let memoryHistory = memory.map(memObject => new Date(memObject.timestamp));
        let cpuHistory = Object.keys(cpu).length > 0 ?
            Object.values(cpu).map(cpuObject => new Date(cpuObject.timestamp)) : [];

        return (
            <ThemeProvider theme={darkTheme}>
                <Bar logoutFunction={logout} handleSettingsModalOpen={() => setSettingsModalOpen(true)} />
                <div className="topContainer">
                    <div className="monitorContainer">
                        <h1>System Monitor</h1>
                        <div className="hostContainer">
                            <h2>{systemInfo.hostname}</h2>
                            <div className="chartsContainer">
                                {config.enabledElements.memory_chart.enabled && (
                                    <MemoryChartWidget memory={memory} memoryHistory={memoryHistory} />
                                )}
                                {config.enabledElements.cpu_chart.enabled && (
                                    <CpuChartWidget cpu={cpu} cpuHistory={cpuHistory} />
                                )}
                                {config.enabledElements.disk_chart.enabled && (
                                    <DiskChartWidget disk={disksToDisplay} />
                                )}
                            </div>
                            <div className="mainContainer">
                                {config.enabledElements.uptime.enabled && (
                                    <InfoCard title="System Uptime">
                                        <p>{systemInfo['uptime']} minutes</p>
                                    </InfoCard>
                                )}
                                {config.enabledElements.memory_data.enabled && (
                                    <MemoryCard memory={memory} />
                                )}
                                {config.enabledElements.cpu_data.enabled && (
                                    <CpuCard cpu={cpu} systemInfo={systemInfo} />
                                )}
                                {config.enabledElements.disk_data.enabled && (
                                    <DisksCard disks={disksToDisplay} />
                                )}
                                {config.enabledElements.time.enabled && (
                                    <TimeCard systemInfo={systemInfo} />
                                )}
                            </div>
                            <SettingsModal
                                open={settingsModalOpen}
                                onClose={() => setSettingsModalOpen(false)}
                                config={config}
                            />
                        </div>
                    </div>
                </div>
            </ThemeProvider>
        )
    }
}

export default App
