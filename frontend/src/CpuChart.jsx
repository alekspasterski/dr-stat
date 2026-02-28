import { LineChart } from '@mui/x-charts/LineChart'
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { Modal } from "@mui/material";
import CssBaseline from '@mui/material/CssBaseline';

function CpuChart({cpu, CpuHistory, height=0}) {

    return (
        <>
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
                height={height > 0 ? height : undefined}
            />
        </>
    )
}

export default CpuChart;
