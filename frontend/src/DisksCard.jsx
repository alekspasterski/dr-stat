import DiskInfo from "./DiskInfo";
import InfoCard from "./InfoCard";

const DisksCard = ({ disks }) => (
    <InfoCard title="Disks">
        {disks.length > 0 ?
            disks.filter((disk) => disk.active === true).map((disk) => (
                <DiskInfo disk={disk} key={disk.hw_id} />
            ))
            : (
                <p>Loading...</p>
            )}
    </InfoCard>
)

export default DisksCard;
