import PartitionInfo from './PartitionInfo.jsx'
import FilesystemInfo from './FilesystemInfo.jsx';
function DiskInfo({disk}) {
    let writes_p_s_b;
    let reads_p_s_b;
    let renderIO = false;
    const last = disk?.disk_usage?.at(-1);
    const prev = disk?.disk_usage?.at(-2);
    if (last && prev) {
        writes_p_s_b = (last.write_bytes - prev.write_bytes) / ((new Date(last.timestamp) - new Date(prev.timestamp)) / 1000);
        reads_p_s_b = (last.read_bytes - prev.read_bytes) / ((new Date(last.timestamp) - new Date(prev.timestamp)) / 1000);
        renderIO = true;
    }
    return (
        <div className="diskCard">
            <span className="diskTitle">{disk.device}</span>
            <hr />
            <div className="infoRow">
                <span className="diskLabel">Hardware ID: </span><span title={disk.hw_id} className="diskId">{disk.hw_id}</span>
            </div>
            {renderIO ? (
                <>
                <div className="infoRow">
                    <span className="diskLabel">Write: </span><span title="writes" className="diskId">{(writes_p_s_b / 1024 / 1024).toFixed(2)} MBps</span>
                </div>
                <div className="infoRow">
                    <span className="diskLabel">Read: </span><span title="reads" className="diskId">{(reads_p_s_b / 1024 / 1024).toFixed(2)} MBps</span>
                </div>
                <div className="infoRow">
                    <span className="diskLabel">Size [GB]: </span><span title="size" className="diskId">{(last.total / 1024 / 1024 / 1024).toFixed(2)}</span>
                </div>
                </>
            ) : (
                <p>Loading data...</p>
            )}
            {disk.filesystem_data.filter((fs) => fs.active === true).length > 0 ? (
                <FilesystemInfo filesystem={disk.filesystem_data.filter((fs) => fs.active).at(0)} />
            ) : (
                disk.partition_data.filter((partition) => partition.active === true).map((partition, index) => {
                return (
                    <PartitionInfo partition={partition} index={index+1} key={partition.uuid}/>
                )
            }))}
        </div>
    );
}

export default DiskInfo;
