import { useState, useEffect } from 'react'
import './App.css'
import InfoCard from './InfoCard.jsx'
import { LineChart } from '@mui/x-charts/LineChart'
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { Modal } from "@mui/material";
import CssBaseline from '@mui/material/CssBaseline';

const darkTheme = createTheme({
    palette: {
        mode: 'dark',
    },
});

function App() {
    // State for the modal windows
    const [memoryChartModalOpen, setMemoryChartModalOpen] = useState(false);
    const [CpuChartModalOpen, setCpuChartModalOpen] = useState(false);
    const handleMemoryChartModalOpen = () => setMemoryChartModalOpen(true);
    const handleMemoryChartModalClose = () => setMemoryChartModalOpen(false);
    const handleCpuChartModalOpen = () => setCpuChartModalOpen(true);
    const handleCpuChartModalClose = () => setCpuChartModalOpen(false);
    // State for the API calls
    const [uptime, setUptime] = useState("Loading...");
    const [memory, setMemory] = useState([]);
    const [cpu, setCpu] = useState([]);
    const [time, setTime] = useState({
        date_and_time: -1,
        time_zone_name: "",
        time_zone_offset: 0,
    });
    useEffect(() => {
        document.title = 'System Monitor';
        const fetchData = () => {
            fetch("/sysmon/uptime")
                .then(response => response.json())
                .then(data => setUptime(data.uptime_minutes))
                .catch(err => console.error(err))
            fetch("/sysmon/memory/2.json")
                .then(response => response.json())
                .then(data => {setMemory(data);})
                .catch(err => console.error(err))
            fetch("/sysmon/cpu/2.json")
                .then(response => response.json())
                .then(data => {setCpu(data);})
                .catch(err => console.error(err))
            fetch("/sysmon/time")
                .then(response => response.json())
                .then(data => {setTime(data);})
                .catch(err => console.error(err))

        };
        fetchData();

        const intervalId = setInterval(fetchData, 4000);
        return () => clearInterval(intervalId);
    }, []);

    let history = memory.map(memObject => new Date(memObject.timestamp));
    let CpuHistory = Object.keys(cpu).length > 0 ?
        Object.values(cpu).map(cpuObject => new Date(cpuObject.timestamp)) : [];

    return (
        <div style={{
                 padding: '10px',
             }}>
            <h1>System Monitor</h1>
            <div className="chartsContainer">
                {memory.length > 0 ? (
                    <ThemeProvider theme={darkTheme}>
                        <div className="chartCard">
                        <h4>Memory chart</h4>
                            
                        <LineChart
                            onClick={handleMemoryChartModalOpen}
                            xAxis={[{
                                data: history,
                                scaleType: 'time',
                                min: history[0],
                                max: history[history.length-1]
                            }]}
                            yAxis={[{
                                min: 0,
                                max: 100,
                                label: 'memory usage [%]'
                            }]}
                            series={[
                                {
                                    data : memory.map(mem => (100* (1 - (mem.free / mem.total))).toFixed(2) ),
                                    area : true,
                                    baseline: 'min',
                                    showMark: false,
                                    valueFormatter: (v) => (v === null ? '' : `${v}%`),
                                    label: 'Used memory',
                                },
                            ]}
                            height={383}
                        />
                            </div>
                    </ThemeProvider>
                ) : (
                    <p>Awaiting more data...</p>
                )}
                {Object.keys(cpu).length > 0 ? (
                    <ThemeProvider theme={darkTheme}>
                        <div className="chartCard">
                        <h4>CPU usage chart</h4>
                        <LineChart
                            onClick={handleCpuChartModalOpen}
                            xAxis={[{
                                data: CpuHistory,
                                scaleType: 'time',
                                min: CpuHistory[0],
                                max: CpuHistory[CpuHistory.length -1]
                            }]}
                            yAxis={[{
                                min: 0,
                                max: 100,
                                label: 'CPU usage [%]'
                            }]}
                            series={
                                cpu[0].cpu_usage.map((cpuUsageData) => ({
                                    data :  cpu.map((item) => (item.cpu_usage[cpuUsageData.cpu_number].cpu_usage)),
                                        area : false,
                                        baseline: 'min',
                                        showMark: false,
                                        valueFormatter: (v) => (v === null ? '' : `${v}%`),
                                        label: `Core ${cpuUsageData.cpu_number} usage`,
                            }))
                                }
                            height={300}
                        />
                    </div>
                    </ThemeProvider>
                ) : (
                    <p>Awaiting more data...</p>
                )}
            </div>
            <div className="mainContainer">
                <InfoCard title="System Uptime">
                    <p>{uptime} minutes</p>
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
                    <p>CPU Model: {cpu.cpu_model}</p>
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
                <InfoCard title="Time">
                    <p>Server time: {new Date(time.date_and_time).toLocaleString()}</p>
                    <p>Server timezone: {time.time_zone_name}</p>
                </InfoCard>
            </div>
            <Modal
                open={memoryChartModalOpen}
                onClose={handleMemoryChartModalClose}>
                <div className="ModalBox">
                    <ThemeProvider theme={darkTheme}>
                        <h4>Memory chart</h4>
                        <LineChart
                            xAxis={[{
                                data: history,
                                scaleType: 'time',
                                min: history[0],
                                max: history[history.length -1]
                            }]}
                            yAxis={[{
                                min: 0,
                                max: 100,
                                label: 'memory usage [%]'
                            }]}
                            series={[
                                {
                                    data : memory.map(mem => (100* (1 - (mem.free / mem.total))).toFixed(2) ),
                                    area : true,
                                    baseline: 'min',
                                    showMark: false,
                                    valueFormatter: (v) => (v === null ? '' : `${v}%`),
                                    label: 'Used memory',
                                },
                            ]}
                        />
                    </ThemeProvider>
                    </div>
            </Modal>
            <Modal
                open={CpuChartModalOpen}
                onClose={handleCpuChartModalClose}>
                <div className="ModalBox">
                    <ThemeProvider theme={darkTheme}>
                        <h4>CPU usage chart</h4>
                        <LineChart
                            xAxis={[{
                                data: CpuHistory,
                                scaleType: 'time',
                                min: CpuHistory[0],
                                max: CpuHistory[CpuHistory.length -1]
                            }]}
                            yAxis={[{
                                min: 0,
                                max: 100,
                                label: 'CPU usage [%]'
                            }]}
                            series={
                                cpu[0].cpu_usage.map((cpuUsageData) => ({
                                    data :  cpu.map((item) => (item.cpu_usage[cpuUsageData.cpu_number].cpu_usage)),
                                        area : false,
                                        baseline: 'min',
                                        showMark: false,
                                        valueFormatter: (v) => (v === null ? '' : `${v}%`),
                                        label: `Core ${cpuUsageData.cpu_number} usage`,
                            }))
                                }
                        />
                    </ThemeProvider>
                    </div>
            </Modal>
        </div>
    )
}

export default App
