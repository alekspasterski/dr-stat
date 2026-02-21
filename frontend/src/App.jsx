import { useState, useEffect } from 'react'
import './App.css'
import InfoCard from './InfoCard.jsx'
import { LineChart } from '@mui/x-charts/LineChart'
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';

function App() {

    const darkTheme = createTheme({
        palette: {
            mode: 'dark',
        },
    });
    const [uptime, setUptime] = useState("Loading...");
    const [memory, setMemory] = useState({
        free_memory: -1,
        total_memory: -1,
        used_percent: -1,
        history: {},
    });
    const [cpu, setCpu] = useState({
        avg_load: -1,
        cpu_model: "",
        cpu_usage: [],  
    });
    const [time, setTime] = useState({
        date_and_time: -1,
        time_zone_name: "",
        time_zone_offset: 0,
    });
    useEffect(() => {
        const fetchData = () => {
            fetch("/sysmon/uptime")
                .then(response => response.json())
                .then(data => setUptime(data.uptime_minutes))
                .catch(err => console.error(err))
            fetch("/sysmon/memory")
                .then(response => response.json())
                .then(data => {setMemory(data);})
                .catch(err => console.error(err))
            fetch("/sysmon/cpu")
                .then(response => response.json())
                .then(data => {setCpu(data);})
                .catch(err => console.error(err))
            fetch("/sysmon/time")
                .then(response => response.json())
                .then(data => {setTime(data);})
                .catch(err => console.error(err))

        };
        fetchData();

        const intervalId = setInterval(fetchData, 3000);
        return () => clearInterval(intervalId);
    }, []);

    let history = Object.keys(memory.history).map(date => new Date(date));

    return (
        <div style={{
                 padding: '10px',
             }}>
            <h1>System Monitor</h1>
            <div className="mainContainer">
                <InfoCard title="System Uptime">
                    <p>{uptime} minutes</p>
                </InfoCard>
                <InfoCard title="Memory">
                    <p>Total memory: {(memory.total_memory / 1024 / 1024).toFixed(2)} GB</p>
                    <p>Free memory: {(memory.free_memory / 1024 / 1024).toFixed(2)} GB</p>
                    <p>Percent used: {memory.used_percent.toFixed(2)} %</p>
                    {Object.keys(memory.history).length > 0 ? (
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
                                        data : Object.values(memory.history).map(mem => (100* (1 - (mem / memory.total_memory))).toFixed(2) ),
                                        area : true,
                                        baseline: 'min',
                                        showMark: false,
                                        valueFormatter: (v) => (v === null ? '' : `${v}%`),
                                        label: 'Used memory',
                                    },
                                ]}
                                height={300}
                            />
                        </ThemeProvider>
                    ) : (
                        <p>Awaiting more data...</p>
                    )}
                </InfoCard>
                <InfoCard title="CPU">
                    <p>CPU Model: {cpu.cpu_model}</p>
                    <p>Load Average: {cpu.avg_load}</p>
                    <h4>CPU Usage:</h4>
                    {cpu.cpu_usage.map((item, index) => (
                        <p key={index}>Core {index}: {item} %</p>
                    ))}
                </InfoCard>
                <InfoCard title="Time">
                    <p>Server time: {new Date(time.date_and_time).toLocaleString()}</p>
                    <p>Server timezone: {time.time_zone_name}</p>
                </InfoCard>
            </div>
        </div>
    )
}

export default App
