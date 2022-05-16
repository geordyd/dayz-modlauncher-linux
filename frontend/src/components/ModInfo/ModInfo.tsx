import React, { useEffect, useState } from "react";
import "./ModInfo.css";

const ModInfo = (props: any) => {

    return (
        <div className="mod-info">
            <div className="mod-name">Mod name: {props.ModData.name}</div>
            <div className="server-name">Mod id: {props.ModData.id}</div>
        </div>
    );
}

export default ModInfo;