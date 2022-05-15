import React, { useEffect, useState } from "react";
import "./ModInfo.css";

const ModInfo = (props: any) => {

    const [modName, setModName] = useState("Loading...");

    useEffect(() => {
        if(modName === "Loading...") {
        fetch(`/getmodnamebyid/${props.ModData}`)
            .then((res) => res.json())
            .then((data) => {
               setModName(data.data);
            });
        }
    });

    return (
        <div className="mod-info">
            <div className="mod-name">Mod name: {modName}</div>
            <div className="server-name">Mod id: {props.ModData}</div>
        </div>
    );
}

export default ModInfo;