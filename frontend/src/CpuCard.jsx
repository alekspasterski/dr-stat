import InfoCard from "./InfoCard";

const CpuCard = ({ cpu, systemInfo }) => (
    <InfoCard title="CPU">
        {cpu.length > 0 ? (
            <>
                <p>CPU Model: {systemInfo.cpu_model}</p>
                <p>Load Average: {cpu[cpu.length - 1].avg_load}</p>
                <h4>CPU Usage:</h4>
                {cpu[cpu.length - 1].cpu_usage.map((item) => (
                    <p key={item.cpu_number}>Core {item.cpu_number}: {item.cpu_usage} %</p>
                ))}
            </>
        ) : (
            <p>Loading...</p>
        )}
    </InfoCard>
)

export default CpuCard;
