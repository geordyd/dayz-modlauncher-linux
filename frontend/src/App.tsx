import React, { useState, useEffect } from "react";
import "./App.css";
import Menu from "./components/Menu/Menu";
import ServerInfo from "./components/ServerInfo/ServerInfo";
import ModInfo from "./components/ModInfo/ModInfo";

function App() {
    const [searchValue, setSearchValue] = useState("");
    const [serverList, setServerList] = useState(Object);
    const [filter, setFilter] = useState("");
    const [showInstalledMods, setShowInstalledMods] = useState(false);
    const [installedModsList, setInstalledModsList] = useState(Object);
    const [playCommand, setPlayCommand] = useState("");

    useEffect(() => {
        const init = async () => {
            await fetch("/steamcmdinit");
            fetch("/createsymlinks");
        };

        init().catch(console.error);
    });

    useEffect(() => {
        let value = filter;

        if (value !== "") {
            value = `"${filter}"`;
        }

        fetch(
            `https://api.battlemetrics.com/servers?filter[game]=dayz&filter[search]=${value}&page[size]=20`
        )
            .then((res) => res.json())
            .then((data) => {
                setServerList(data);
            });
    }, [filter]);

    useEffect(() => {
        if (showInstalledMods) {
            fetch("/getinstalledmods")
                .then((res) => res.json())
                .then((data) => {
                    setInstalledModsList(data);
                });
        }
    }, [showInstalledMods]);

    return (
        <div className="wrapper">
            <div className="menu">
                <Menu
                    searchValue={searchValue}
                    setSearchValue={setSearchValue}
                    setFilter={setFilter}
                    showInstalledMods={showInstalledMods}
                    setShowInstalledMods={setShowInstalledMods}
                />
            </div>
            <div className="browser">
                {!showInstalledMods
                    ? serverList.data !== undefined &&
                      serverList.data.map((data: any) => {
                          return (
                              <ServerInfo
                                  ServerData={data}
                                  setPlayCommand={setPlayCommand}
                              />
                          );
                      })
                    : installedModsList.data !== undefined &&
                      installedModsList.data.map((data: any) => (
                          <ModInfo
                              ModData={data}
                              setInstalledModsList={setInstalledModsList}
                          />
                      ))}
            </div>
            <div className="console">
                {playCommand !== "" && <div>{playCommand}</div>}
            </div>
        </div>
    );
}

export default App;
