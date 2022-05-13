import React, { useState, useEffect } from "react";
import "./App.css";
import Menu from "./components/Menu/Menu";
function App() {
    const [searchValue, setSearchValue] = useState("");
    const [serverList, setServerList] = useState(Object);
    const [filter, setFilter] = useState("");

    useEffect(() => {
        let value = filter;

        if (value !== "") {
            value = `"${filter}"`;
        }

        fetch(
            `https://api.battlemetrics.com/servers?filter[game]=dayz&filter[search]=${value}`
        )
            .then((res) => res.json())
            .then((data) => {
                setServerList(data);
                console.log(data);
                console.log(filter);
            });
    }, [filter]);

    return (
        <div className="wrapper">
            <div className="menu">
                <Menu
                    searchValue={searchValue}
                    setSearchValue={setSearchValue}
                    setFilter={setFilter}
                />
            </div>
            <div className="browser">
                {serverList.data !== undefined &&
                    serverList["data"].map((data: any) => {
                        return <div>{data["attributes"]["name"]}</div>;
                    })}
            </div>
            <div className="console"></div>
        </div>
    );
}

export default App;
