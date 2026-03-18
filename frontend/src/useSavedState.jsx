import { useState, useEffect } from "react"

function useSavedState(key, initialValue) {
    const [value, setValue] = useState(() => {
        const savedValue = localStorage.getItem(key);
        // if present in LocalStorage
        if (savedValue !== null) {
            try {
                return JSON.parse(savedValue);
            }
            catch {
                return savedValue;
            }
        } else {
            return initialValue;
        }
    })
    useEffect(() => {
        localStorage.setItem(key, JSON.stringify(value))
    }, [key, value])
    return [value, setValue];
}

export default useSavedState;
