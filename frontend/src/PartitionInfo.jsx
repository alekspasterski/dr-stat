function PartitionInfo({ partition, index }) {

    let percent = 0;
    let render = false;
    const last = partition?.partition_usage?.at(-1);
    if (last) {
        percent = ((partition.partition_usage.at(-1).total - partition.partition_usage.at(-1).free ) / partition.partition_usage.at(-1).total) * 100;
        render = true;
    }
    const getBarColor = p => (p > 90 ? '#96384F' : p > 70 ? '#FF9A59' : '#4DD69D')
    if (render) {
        return (<div className="partitionCard" key={partition.uuid}>
                <p className="partitionCardTitle">{partition.name}</p>
                <div className="partitionCardContents">
                    {partition.mount_point && (
                        <div className="infoRow"><p className="diskLabel">Mount Point:</p> <p className="diskId">{partition.mount_point}</p></div>
                    )}
                    <div className="infoRow"><p className="diskLabel">Filesystem:</p> <p className="diskId">{partition.filesystem}</p></div>
                    <div className="infoRow"><p className="diskLabel">Total size [GB]: </p><p className="diskId">{(partition.partition_usage.at(-1).total / 1024**3).toFixed(2)}</p></div>
                    <div className="infoRow"><p className="diskLabel">Used space [GB]: </p><p className="diskId">{((partition.partition_usage.at(-1).total - partition.partition_usage.at(-1).free ) / 1024**3).toFixed(2)}</p></div>
                    {}
                    <div className="partitionUsedSpaceBar">
                        <div className="partitionUsedSpaceBarContents" style={{width: `${percent}%`, backgroundColor : getBarColor(percent)}}></div> 
                        <span className="partitionBarText">{percent.toFixed(0)}%</span>
                    </div>
                </div>
            </div>
               )}
    else {
        return (
            <p>Loading...</p>
        )
    }
}

export default PartitionInfo;
