import { useState, cloneElement } from "react"
import { Modal } from "@mui/material";

const ChartWidget = ({children, dataSeries}) => {
    const [isOpen, setIsOpen] = useState(false);
    return dataSeries.length > 0 ? (
        <>
            <div className="chartCard" onClick={() => setIsOpen(true)}>
                {children}
            </div>
            <Modal
                open={isOpen}
                onClose={() => setIsOpen(false)}>
                <div className="ModalBox">
                    {isOpen && 
                     cloneElement(children, { height: undefined })
                    }
                </div>
            </Modal>
        </>
    ) : (
        <p>Awaiting more data...</p>
    )
}


export default ChartWidget;
