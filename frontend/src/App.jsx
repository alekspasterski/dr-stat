import { useState, useEffect } from 'react'
import './App.css'
import InfoCard from './InfoCard.jsx'

function App() {
  const [uptime, setUptime] = useState("Loading...");
  const [memory, setMemory] = useState({
    free_memory: -1,
    total_memory: -1,
    used_percent: -1,
  });
  const [cpu, setCpu] = useState({
    avg_load: -1,
    cpu_model: "",
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

  return (
    <div style={{ padding: '50px' }}>
      <h1>System Monitor</h1>
      <InfoCard title="System Uptime">
        <p>{uptime} minutes</p>
      </InfoCard>
      <InfoCard title="Memory">
        <p>Total memory: {(memory.total_memory / 1024 / 1024).toFixed(2)} GB</p>
        <p>Free memory: {(memory.free_memory / 1024 / 1024).toFixed(2)} GB</p>
        <p>Percent used: {memory.used_percent.toFixed(2)} %</p>
      </InfoCard>
      <InfoCard title="CPU">
        <p>CPU Model: {cpu.cpu_model}</p>
        <p>Load Average: {cpu.avg_load}</p>
      </InfoCard>
      <InfoCard title="Time">
        <p>Server time: {new Date(time.date_and_time).toLocaleString()}</p>
        <p>Server timezone: {time.time_zone_name}</p>
      </InfoCard>
    </div>
  )
}

export default App
