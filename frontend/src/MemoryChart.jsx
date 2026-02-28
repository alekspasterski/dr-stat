import { LineChart } from '@mui/x-charts/LineChart'
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { Modal } from "@mui/material";
import CssBaseline from '@mui/material/CssBaseline';

function MemoryChart({memory, MemoryHistory, height=0}) {

    return (
        <>
            <h4>Memory chart</h4>
            <LineChart
                xAxis={[{
                    data: MemoryHistory,
                    scaleType: 'time',
                    min: MemoryHistory[0],
                    max: MemoryHistory[MemoryHistory.length-1]
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
                height={height > 0 ? height : undefined}
            />
        </>
    )
}

export default MemoryChart;
