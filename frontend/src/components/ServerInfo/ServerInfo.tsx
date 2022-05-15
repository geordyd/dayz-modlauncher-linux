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

    const SubscribeToMods = () => {
        props.ServerData.attributes.details.modIds.forEach((modId: any) => {
            fetch(`/subscribemod/${modId}`);
        });
    }

    const UnsubscribeFromMods = () => {
        props.ServerData.attributes.details.modIds.forEach((modId: any) => {
            fetch(`/unsubscribemod/${modId}`);
            fetch(`/deletemodbyid/${modId}`)
        });
    }

    const DisplayPlayCommand = () => {
        let modList = "";

        props.ServerData.attributes.details.modIds.forEach((modId: any) => {
            modList += `${modId} `;
        });

        let playCommand = `steam -applaunch 221100 -connect=${props.ServerData.attributes.ip}:${props.ServerData.attributes.port} -nolauncher -world=empty name=Marco \\"-mod=${modList}\\"`;

        props.setPlayCommand(playCommand)

    }


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
                <b>Server name:</b> {props.ServerData.attributes.name}
            </div>
            <div className="server-ip">
                <b>Server ip:</b> {props.ServerData.attributes.ip}
            </div>
            {showServerMods && (
                <div className="modlist">
                    <div style={{ fontWeight: "bold" }}>Mod list: </div>
                    {props.ServerData.attributes.details.modIds.map(
                        (modId: any) => {
                            return <ModEntry modId={modId} key={modId} />;
                        }
                    )}
                </div>
            )}
            <div className="subscribe-button">
                <button onClick={() => SubscribeToMods()}>Subscribe to all server mods</button>
            </div>
            <div className="unsubscribe-button">
                <button onClick={() => UnsubscribeFromMods()}>Unsubscribe and delete all server mods</button>
            </div>

            <div className="play-button">
                <button onClick={() => DisplayPlayCommand()}>Play</button>
            </div>
        </div>
    );
};

export default ServerInfo;
