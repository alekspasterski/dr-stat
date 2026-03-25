import DiskChart from "./DiskChart";
import ChartWidget from "./ChartWidget"

const DiskChartWidget = ({ disk }) => (
    <ChartWidget dataSeries={disk}>
        <DiskChart disks={disk} height={300} />
    </ChartWidget>
)

export default DiskChartWidget;
