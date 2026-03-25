import CpuChart from "./CpuChart";
import ChartWidget from "./ChartWidget"

const CpuChartWidget = ({ cpu, cpuHistory }) => (
    <ChartWidget dataSeries={cpu}>
        <CpuChart cpu={cpu} CpuHistory={cpuHistory} height={300} />
    </ChartWidget>
)

export default CpuChartWidget;
