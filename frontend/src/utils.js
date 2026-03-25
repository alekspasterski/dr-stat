export const authenticatedFetch = (token, url, method = 'GET', body = null) => {
    return fetch(url,
        {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token,
            },
            credentials: 'include',
            body: body,
        }).catch(err => console.log(err))
}
export const refreshAPIToken = (setToken) => {
        return fetch("sysmon/token/refresh/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            credentials: "include",
        })
            .then(response => response.json())
            .then(data => {
                setToken(data.access);
            })
            .catch(err => {
                setToken("");
                console.error(err);
            })
    }
