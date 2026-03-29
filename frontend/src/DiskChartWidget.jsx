import DiskChart from "./DiskChart";
import ChartWidget from "./ChartWidget"

const DiskChartWidget = ({ disk }) => (
    <ChartWidget dataSeries={disk}>
        <DiskChart disks={disk} />
    </ChartWidget>
)

export default DiskChartWidget;
