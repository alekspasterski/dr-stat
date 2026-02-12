function InfoCard({ title, children }) {
    const cardStyle = {
        border: '1px solid #444',
        padding: '15px',
        margin: '10px 0',
        borderRadius: '8px',
        backgroundColor: '#2a2a2a',
        color: '#e0e0e0',
        fontFamily: 'monospace'
    };

    return (
        <div style={cardStyle}>
            <h3 style={{ borderBottom: '1px solid #555', paddingBottom: '5px' }}>
                {title}
            </h3>
            <div>{children}</div>
        </div>
    );
}

export default InfoCard;
