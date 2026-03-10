import PartitionInfo from './PartitionInfo.jsx'
function DiskInfo({disk}) {

    return (
        <div className="diskCard">
            <span className="diskTitle">{disk.device}</span>
            <hr />
            <div className="infoRow">
                <span className="diskLabel">Hardware ID: </span><span title={disk.hw_id} className="diskId">{disk.hw_id}</span>
            </div>
            {disk.partition_data.map((partition, index) => {
                return (
                    <PartitionInfo partition={partition} index={index+1} key={partition.uuid}/>
                )
            })}
        </div>
    );
}

export default DiskInfo;
