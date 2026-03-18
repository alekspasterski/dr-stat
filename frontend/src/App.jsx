import { useState, useEffect } from 'react'
import useSavedState from './useSavedState.jsx'
import './App.css'
import InfoCard from './InfoCard.jsx'
import CpuChart from './CpuChart.jsx'
import DiskChart from './DiskChart.jsx'
import DiskInfo from './DiskInfo.jsx'
import Bar from './Bar.jsx'
import MemoryChart from "./MemoryChart.jsx"
import Login from './Login.jsx'
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { Modal } from "@mui/material";

const darkTheme = createTheme({
    palette: {
        mode: 'dark',
    },
});

function App() {
    // State for login
    const [token, setToken] = useState("");
    const [loginFailed, setLoginFailed] = useState("");
    const [isCheckingAuth, setIsCheckingAuth] = useState(true)
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
    const refreshAPIToken = () => {
        return fetch("sysmon/token/refresh/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            credentials: "include",
        })
            .then(response => response.json())
            .then(data => {
                setToken(data.access);
            })
            .catch(err => {
                setToken("");
                console.error(err);
            })
    }
    // State for the modal windows
    const [memoryChartModalOpen, setMemoryChartModalOpen] = useState(false);
    const [CpuChartModalOpen, setCpuChartModalOpen] = useState(false);
    const [DiskChartModalOpen, setDiskChartModalOpen] = useState(false);
    const handleMemoryChartModalOpen = () => setMemoryChartModalOpen(true);
    const handleMemoryChartModalClose = () => setMemoryChartModalOpen(false);
    const handleCpuChartModalOpen = () => setCpuChartModalOpen(true);
    const handleCpuChartModalClose = () => setCpuChartModalOpen(false);
    const handleDiskChartModalOpen = () => setDiskChartModalOpen(true);
    const handleDiskChartModalClose = () => setDiskChartModalOpen(false);
    // State for the API calls
    const [memory, setMemory] = useState([]);
    const [cpu, setCpu] = useState([]);
    const [disks, setDisks] = useState([]);
    const [systemInfo, setSystemInfo] = useState({});
    const [timePeriod, setTimePeriod] = useSavedState("sysmon_time_period",2);
    const [pollingFrequency, setPollingFrequency] = useSavedState("sysmon_polling_frequency", 5);
    // Check if we have a valid refresh token in cookies
    useEffect(() => {
        refreshAPIToken().finally(() => {
            setIsCheckingAuth(false);
        })
    }, []) // Run only once
    const loggedIn = Boolean(token);
    useEffect(() => {
        if (loggedIn) {
            document.title = 'System Monitor';
            const fetchData = (url, setter) => {
                fetch(url, {
                    headers: {
                        "Authorization": "Bearer " + token,
                    },
                    credentials: "include",
                })
                    .then(response => {
                        if (response.status === 401) {
                            refreshAPIToken();
                            throw new Error("Token Expired");
                        }
                        if (!response.ok) {
                            throw new Error(response.statusText);
                        }
                        return response.json();
                    })
                    .then(data => { setter(data); })
                    .catch(err => console.error(err))
            };
            const fetchStats = () => {
                fetchData(`/sysmon/memory/${timePeriod}.json`, setMemory);
                fetchData(`/sysmon/cpu/${timePeriod}.json`, setCpu);
                fetchData(`/sysmon/disk/${timePeriod}.json`, setDisks);
                fetchData(`/sysmon/system_info`, setSystemInfo);
            };
            fetchStats();


            const intervalId = setInterval(fetchStats, pollingFrequency * 1000);
            const refreshId = setInterval(refreshAPIToken, 60000);
            return () => {
                clearInterval(intervalId);
                clearInterval(refreshId);
            }
        }
    }, [token, timePeriod, pollingFrequency]);

    const logout = () => {
        fetch('/sysmon/logout/', {
            headers: {
                "Authorization": "Bearer " + token,
            },
            credentials: "include",
        }).then(() => {
            setToken("");
        }).catch((err) => console.log(err))
    }
    
    if (!loggedIn) {
        return (
            <>
                {loginFailed && <div className="loginError"><p>{loginFailed}</p></div>}
                <Login action={fetchAPIToken} loginFailed={loginFailed} />
            </>
        )
    }

    if (isCheckingAuth || memory.length === 0 || cpu.length === 0 || disks.length === 0 || Object.keys(systemInfo).length === 0) {
        return (<div className="loader"></div>)
    }

    if (loggedIn) {
        let history = memory.map(memObject => new Date(memObject.timestamp));
        let CpuHistory = Object.keys(cpu).length > 0 ?
            Object.values(cpu).map(cpuObject => new Date(cpuObject.timestamp)) : [];

        return (
            <div className="topContainer">
                <Bar logoutFunction={logout} timePeriod={timePeriod} setTimePeriod={setTimePeriod}
                pollingFrequency={pollingFrequency} setPollingFrequency={setPollingFrequency}/>
                <div className="monitorContainer">
                    <h1>System Monitor</h1>
                    <div className="hostContainer">
                        <h2>{systemInfo.hostname}</h2>
                        <div className="chartsContainer">
                            {memory.length > 0 ? (
                                <ThemeProvider theme={darkTheme}>
                                    <div className="chartCard" onClick={handleMemoryChartModalOpen}>
                                        <MemoryChart memory={memory} MemoryHistory={history} height={383} />
                                    </div>
                                </ThemeProvider>
                            ) : (
                                <p>Awaiting more data...</p>
                            )}
                            {cpu.length > 0 ? (
                                <ThemeProvider theme={darkTheme}>
                                    <div className="chartCard" onClick={handleCpuChartModalOpen}>
                                        <CpuChart cpu={cpu} CpuHistory={CpuHistory} height={300} />
                                    </div>
                                </ThemeProvider>
                            ) : (
                                <p>Awaiting more data...</p>
                            )}
                            {disks.length > 0 ? (
                                <ThemeProvider theme={darkTheme}>
                                    <div className="chartCard" onClick={handleDiskChartModalOpen}>
                                        <DiskChart disks={disks} height={300} />
                                    </div>
                                </ThemeProvider>
                            ) : (
                                <p>Awaiting more data...</p>
                            )}
                        </div>
                        <div className="mainContainer">
                            <InfoCard title="System Uptime">
                                <p>{systemInfo['uptime']} minutes</p>
                            </InfoCard>
                            {memory.length > 0 ? (
                                <InfoCard title="Memory">
                                    <p>Total memory: {(memory[memory.length - 1].total / 1024 / 1024).toFixed(2)} GB</p>
                                    <p>Free memory: {(memory[memory.length - 1].free / 1024 / 1024).toFixed(2)} GB</p>
                                    <p>Percent used: {((1 - (memory[memory.length - 1].free / memory[memory.length - 1].total)) * 100).toFixed(2)} %</p>
                                </InfoCard>
                            ) : (
                                <InfoCard title="Memory">
                                    <p>Loading...</p>
                                </InfoCard>
                            )}
                            {cpu.length > 0 ? (
                                <InfoCard title="CPU">
                                    <p>CPU Model: {systemInfo.cpu_model}</p>
                                    <p>Load Average: {cpu[cpu.length - 1].avg_load}</p>
                                    <h4>CPU Usage:</h4>
                                    {cpu[cpu.length - 1].cpu_usage.map((item) => (
                                        <p key={item.cpu_number}>Core {item.cpu_number}: {item.cpu_usage} %</p>
                                    ))}
                                </InfoCard>
                            ) : (
                                <InfoCard title="CPU">
                                    <p>Loading...</p>
                                </InfoCard>
                            )}
                            <InfoCard title="Disks">
                                {disks.length > 0 ? (
                                    disks.map((disk) => (
                                        <DiskInfo disk={disk} key={disk.hw_id} />
                                    ))
                                ) : (
                                    <p>Loading...</p>
                                )}
                            </InfoCard>
                            <InfoCard title="Time">
                                <p>Server time: {new Date(systemInfo.system_time).toLocaleString()}</p>
                                <p>Server timezone: {systemInfo.system_time_zone}</p>
                            </InfoCard>
                        </div>
                        <Modal
                            open={memoryChartModalOpen}
                            onClose={handleMemoryChartModalClose}>
                            <div className="ModalBox">
                                <ThemeProvider theme={darkTheme}>
                                    <MemoryChart memory={memory} MemoryHistory={history} />
                                </ThemeProvider>
                            </div>
                        </Modal>
                        <Modal
                            open={CpuChartModalOpen}
                            onClose={handleCpuChartModalClose}>
                            <div className="ModalBox">
                                <ThemeProvider theme={darkTheme}>
                                    <CpuChart cpu={cpu} CpuHistory={CpuHistory} />
                                </ThemeProvider>
                            </div>
                        </Modal>
                        <Modal
                            open={DiskChartModalOpen}
                            onClose={handleDiskChartModalClose}>
                            <div className="ModalBox">
                                <ThemeProvider theme={darkTheme}>
                                    <DiskChart disks={disks} />
                                </ThemeProvider>
                            </div>
                        </Modal>
                    </div>
                </div>
            </div>
        )
    }
}

export default App
