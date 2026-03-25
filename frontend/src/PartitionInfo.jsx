import FilesystemInfo from "./FilesystemInfo";

function PartitionInfo({ partition, index }) {

        return (<div className="partitionCard" key={partition.uuid}>
                <p className="partitionCardTitle">{partition.name}</p>
                <div className="partitionCardContents">
                    <div className="infoRow"><p className="diskLabel">Total size [GB]: </p><p className="diskId">{(partition.total / 1024**3).toFixed(2)}</p></div>
                    <FilesystemInfo filesystem={partition.filesystem_data.filter((fs) => fs.active === true).at(0)} />
                </div>
            </div>
               )
}

export default PartitionInfo;
