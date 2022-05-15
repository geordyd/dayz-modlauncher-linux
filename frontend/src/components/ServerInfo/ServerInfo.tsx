import React, { useEffect, useState } from "react";
import "./ServerInfo.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
    faChevronRight,
    faChevronDown,
} from "@fortawesome/free-solid-svg-icons";
import ModEntry from "../ModEntry/ModEntry";

const ServerInfo = (props: any) => {
    const [showServerMods, setShowServerMods] = useState(false);

    return (
        <div className="server-info">
            <div
                className="show-server-button"
                onClick={() => setShowServerMods(!showServerMods)}
            >
                {!showServerMods ? (
                    <FontAwesomeIcon icon={faChevronRight} />
                ) : (
                    <FontAwesomeIcon icon={faChevronDown} />
                )}
            </div>
            <div className="server-name">
                Server name: {props.ServerData.attributes.name}
            </div>
            <div className="server-ip">
                Server ip: {props.ServerData.attributes.ip}
            </div>
            {showServerMods && (
                <div className="modlist">
                    <p style={{ fontWeight: "bold" }}>Mod list: </p>
                    {props.ServerData.attributes.details.modIds.map(
                        (modId: any) => {
                            return <ModEntry modId={modId} key={modId} />;
                        }
                    )}
                </div>
            )}
            <div className="subscribe-button">
                <button>Subscribe to all server mods</button>
            </div>
            <div className="unsubscribe-button">
                <button>Unsubscribe and delete all server mods</button>
            </div>

            <div className="play-button">
                <button>Play</button>
            </div>
        </div>
    );
};

export default ServerInfo;
