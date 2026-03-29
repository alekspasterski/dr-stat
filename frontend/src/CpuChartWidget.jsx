import CpuChart from "./CpuChart";
import ChartWidget from "./ChartWidget"

const CpuChartWidget = ({ cpu, cpuHistory }) => (
    <ChartWidget dataSeries={cpu}>
        <CpuChart cpu={cpu} CpuHistory={cpuHistory} />
    </ChartWidget>
)

export default CpuChartWidget;
