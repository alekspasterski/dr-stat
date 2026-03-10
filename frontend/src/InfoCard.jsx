function InfoCard({ title, children }) {

    return (
        <div className="infoCard">
            <h3 style={{ borderBottom: '1px solid #555', paddingBottom: '5px' }}>
                {title}
            </h3>
            <div>{children}</div>
        </div>
    );
}

export default InfoCard;
