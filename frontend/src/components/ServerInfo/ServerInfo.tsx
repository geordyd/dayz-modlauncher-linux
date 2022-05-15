import React, { useState } from "react";
import "./ServerInfo.css";



const ServerInfo = (props: any) => {

    const [showServerMods, setShowServerMods] = useState(false);

    return (
        <div className="server-info">
            <div className="server-name">Server name: {props.ServerData.attributes.name}</div>
            <div className="server-ip">Server ip: {props.ServerData.attributes.ip}</div>
            
        </div>
    );
}

export default ServerInfo;