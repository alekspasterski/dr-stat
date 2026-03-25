import InfoCard from "./InfoCard";

const MemoryCard = ({ memory }) => (
    <InfoCard title="Memory">
        {memory.length > 0 ? (
            <>
                <p>Total memory: {(memory[memory.length - 1].total / 1024 / 1024).toFixed(2)} GB</p>
                <p>Free memory: {(memory[memory.length - 1].free / 1024 / 1024).toFixed(2)} GB</p>
                <p>Percent used: {((1 - (memory[memory.length - 1].free / memory[memory.length - 1].total)) * 100).toFixed(2)} %</p>
            </>
        ) : (
            <p>Loading...</p>
        )}
    </InfoCard>
);

export default MemoryCard;
