import InfoCard from "./InfoCard";

const TimeCard = ({ systemInfo }) => (
            <InfoCard title="Time">
                {systemInfo ? (
                    <>
                        <p>Server time: {new Date(systemInfo.system_time).toLocaleString()}</p>
                        <p>Server timezone: {systemInfo.system_time_zone}</p>
                    </>
                ) : (
                    <p>Loading...</p>
                )}
            </InfoCard>
);

export default TimeCard;
