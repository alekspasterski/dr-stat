import { useState, useEffect } from "react"
import useSavedState from "./useSavedState";
import { authenticatedFetch, refreshAPIToken } from "./utils";

const useSystemData = (token, setToken) => {
    const [memory, setMemory] = useState([]);
    const [cpu, setCpu] = useState([]);
    const [disks, setDisks] = useState([]);
    const [systemInfo, setSystemInfo] = useState({});
    const [timePeriod, setTimePeriod] = useSavedState("sysmon_time_period", 2);
    const [pollingFrequency, setPollingFrequency] = useSavedState("sysmon_polling_frequency", 5);
    const [filesystemFiltering, setFilesystemFiltering] = useSavedState("sysmon_filesystem_filtering", false);
    const [settings, setSettings] = useState({});
    const [enabledElements, setEnabledElements] = useSavedState("sysmon_enabled_elements", {
        cpu_data: { name: "CPU data", enabled: true },
        memory_data: { name: "Memory data", enabled: true },
        disk_data: { name: "Disk data", enabled: true },
        uptime: { name: "Uptime", enabled: true },
        time: { name: "Time", enabled: true },
        memory_chart: { name: "Memory chart", enabled: true },
        cpu_chart: { name: "CPU chart", enabled: true },
        disk_chart: { name: "Disk chart", enabled: true },
    })

    useEffect(() => {
        if (token) {
            document.title = 'System Monitor';
            const fetchData = (url, setter) => {
                authenticatedFetch(token, url)
                    .then(response => {
                        if (response.status === 401) {
                            refreshAPIToken(setToken);
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
                fetchData(`/sysmon/settings`, setSettings)
            };
            fetchStats();

            const intervalId = setInterval(fetchStats, pollingFrequency * 1000);
            const refreshId = setInterval(() => refreshAPIToken(setToken), 60000);
            return () => {
                clearInterval(intervalId);
                clearInterval(refreshId);
            }
        }
    }, [token, timePeriod, pollingFrequency]);

    const handleServerSideUpdateFrequencyChange = (e) => authenticatedFetch(
        token, "/sysmon/update_data_polling/", 'POST',
        JSON.stringify({
            'interval': e.target.value,
        })
    )

    const handleRetentionPeriodChange = (e) => authenticatedFetch(
        token, "/sysmon/settings/", 'POST',
        JSON.stringify({
            'retention_period': e.target.value * 60 * 60 * 24,
        })
    )

    const config = {
        timePeriod: timePeriod,
        setTimePeriod: setTimePeriod,
        pollingFrequency: pollingFrequency,
        setPollingFrequency: setPollingFrequency,
        filesystemFiltering: filesystemFiltering,
        setFilesystemFiltering: setFilesystemFiltering,
        serverSideUpdateFrequency: systemInfo["task_interval"],
        handleServerSideUpdateFrequencyChange: handleServerSideUpdateFrequencyChange,
        enabledElements: enabledElements,
        setEnabledElements: setEnabledElements,
        settings: settings,
        setSettings: setSettings,
        handleRetentionPeriodChange: handleRetentionPeriodChange,
    }

    return { memory, cpu, disks, systemInfo, config}
}

export default useSystemData;
