import { LineChart } from '@mui/x-charts/LineChart'
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { Modal } from "@mui/material";
import CssBaseline from '@mui/material/CssBaseline';

function DiskChart({disks, height=0}) {

    const timestamps = disks[0].disk_usage.map(du => new Date (du.timestamp)).slice(1);
    return (
        <>
            <h4>Disk IO chart</h4>
            <LineChart
                xAxis={[{
                    data: timestamps,
                    scaleType: 'time',
                    min: timestamps[0],
                    max: timestamps[timestamps.length-1]
                }]}
                yAxis={[{
                    min: 0,
                    label: 'disk IO [MB/s]'
                }]}
                series={
                    disks.map(disk => ({
                        data : disk.disk_usage.map((du, index, arr) => {
                            if (index === 0) return null;
                            const prev = arr[index - 1];
                            const bytesDiff = du.write_bytes - prev.write_bytes;
                            const timeDiffSeconds = (new Date(du.timestamp) - new Date(prev.timestamp)) / 1000
                            const speed = (bytesDiff / timeDiffSeconds) / 1024 / 1024;
                            return Number(speed.toFixed(2))
                        } ).slice(1),
                        area : false,
                        baseline: 'min',
                        showMark: false,
                        valueFormatter: (v) => (v === null ? '' : `${v} MB/s`),
                        label: `${disk.device}: Writes`,
                    })).concat(
                        disks.map(disk => ({
                        data : disk.disk_usage.map((du, index, arr) => {
                            if (index === 0) return null;
                            const prev = arr[index - 1];
                            const bytesDiff = du.read_bytes - prev.read_bytes;
                            const timeDiffSeconds = (new Date(du.timestamp) - new Date(prev.timestamp)) / 1000
                            const speed = (bytesDiff / timeDiffSeconds) / 1024 / 1024;
                            return Number(speed.toFixed(2))
                        } ).slice(1),
                        area : false,
                        baseline: 'min',
                        showMark: false,
                        valueFormatter: (v) => (v === null ? '' : `${v} MB/s`),
                        label: `${disk.device}: Reads`,
                        })))
                }
                height={height > 0 ? height : undefined}
            />
        </>
    )
}

export default DiskChart;
