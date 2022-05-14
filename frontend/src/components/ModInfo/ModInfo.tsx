import React from "react";
import "./ModInfo.css";

const ModInfo = (props: any) => {
    return (
        <div className="mod-info">
            <div className="server-name">Mod id: {props.ModData}</div>
        </div>
    );
}

export default ModInfo;