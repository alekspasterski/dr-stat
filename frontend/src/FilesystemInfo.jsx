
function FilesystemInfo({ filesystem, index }) {

    let percent = 0;
    let render = false;
    const last = filesystem?.filesystem_usage?.at(-1);
    if (last) {
        percent = ((filesystem.filesystem_usage.at(-1).size - filesystem.filesystem_usage.at(-1).free) / filesystem.filesystem_usage.at(-1).size) * 100;
        render = true;
    }
    const getBarColor = p => (p > 90 ? '#96384F' : p > 70 ? '#FF9A59' : '#4DD69D')
    if (render) {
        return (<div className="filesystemCard" key={filesystem.uuid}>
            {filesystem.label ? (
                <p className="filesystemCardTitle">Filesystem {filesystem.label}</p>
            ) : (
                <p className="filesystemCardTitle">Unlabeled filesystem</p>
            )}
                    <hr />
            <div className="filesystemCardContents">
                {filesystem.mount_point && (
                    <div className="infoRow"><p className="diskLabel">Mount Point:</p> <p className="diskId">{filesystem.mount_point}</p></div>
                )}
                <div className="infoRow"><p className="diskLabel">Type:</p> <p className="diskId">{filesystem.filesystem_type}</p></div>
                {filesystem.filesystem_type !== 'swap' && (
                    <>
                        <div className="infoRow"><p className="diskLabel">Total size [GB]: </p><p className="diskId">{(filesystem.filesystem_usage.at(-1).size / 1024 ** 3).toFixed(2)}</p></div>
                        <div className="infoRow"><p className="diskLabel">Used space [GB]: </p><p className="diskId">{((filesystem.filesystem_usage.at(-1).size - filesystem.filesystem_usage.at(-1).free) / 1024 ** 3).toFixed(2)}</p></div>
                        <div className="filesystemUsedSpaceBar">
                            <div className="filesystemUsedSpaceBarContents" style={{ width: `${percent}%`, backgroundColor: getBarColor(percent) }}></div>
                            <span className="filesystemBarText">{percent.toFixed(0)}%</span>
                        </div>
                    </>
                )}
            </div>
        </div>
        )
    }
    else {
        return (
            <p>Loading...</p>
        )
    }
}

export default FilesystemInfo;
