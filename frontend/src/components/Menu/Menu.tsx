import React from "react";



const Menu = (props:any) => {
    return (
        <div className="menu">
            <h1>Filters</h1>
            <div></div>
            <h2>Search:</h2>
            <input type="text" onChange={e => props.setSearchValue(e.target.value)}>
            </input>
            <button onClick={() => props.setFilter(props.searchValue)}>
                Search
            </button>
        </div>
    );
}

export default Menu;