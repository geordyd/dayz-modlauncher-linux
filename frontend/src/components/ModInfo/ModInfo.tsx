import "./ModInfo.css";

const ModInfo = (props: any) => {
    const GetInstalledMods = async (modId: any) => {
        await fetch(`/deletemodbyid/${modId}`);
        await fetch("/getinstalledmods")
            .then((res) => res.json())
            .then((data) => {
                props.setInstalledModsList(data);
            });
    };

    return (
        <div className="mod-info">
            <div className="mod-name">
                <b>Mod name: </b>
                {props.ModData.name}
            </div>
            <div className="server-name">
                <b>Mod id: </b>
                {props.ModData.id}
            </div>
            <button onClick={() => GetInstalledMods(props.ModData.id)}>
                Remove mod
            </button>
        </div>
    );
};

export default ModInfo;
