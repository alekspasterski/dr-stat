import MemoryChart from "./MemoryChart"
import ChartWidget from "./ChartWidget"

const MemoryChartWidget = ({ memory, memoryHistory }) => (
    <ChartWidget dataSeries={memory}>
        <MemoryChart memory={memory} MemoryHistory={memoryHistory} height={383} />
    </ChartWidget>
)

export default MemoryChartWidget;
