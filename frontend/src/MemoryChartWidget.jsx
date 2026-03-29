import MemoryChart from "./MemoryChart"
import ChartWidget from "./ChartWidget"

const MemoryChartWidget = ({ memory, memoryHistory }) => (
    <ChartWidget dataSeries={memory}>
        <MemoryChart memory={memory} MemoryHistory={memoryHistory} />
    </ChartWidget>
)

export default MemoryChartWidget;
