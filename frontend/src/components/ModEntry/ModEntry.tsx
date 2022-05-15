import React, { useEffect, useState } from "react";
import "./ModEntry.css";

const ModEntry = (props: any) => {
    const [modInstalled, setModInstalled] = useState(true);

    useEffect(() => {
        fetch(`/getmodstatebyid/${props.modId}`)
            .then((res) => res.json())
            .then((data) => {
                if (data.data === "Installed") {
                    return setModInstalled(true);
                } else {
                    return setModInstalled(false);
                }
            });
    });

    return (
        <div>
            {modInstalled ? (
                <div className="mod-entry" style={{color: "green"}}>{props.modId}</div>
            ) : (
                <div className="mod-entry" style={{color: "red"}}>{props.modId}</div>
            )}
        </div>
    );
};

export default ModEntry;
