import React from "react";

const Menu = (props:any) => {
    const handleKeyDown = (event:any) => {
        if (event.key === 'Enter') {
          props.setFilter(props.searchValue);
        }
    }
      
    return (
        <div className="menu">
            <h1>Filters</h1>
            <div></div>
            <h2>Search:</h2>
            <input type="text" onChange={e => props.setSearchValue(e.target.value)} onKeyDown={handleKeyDown}>
            </input>
            <button onClick={() => props.setFilter(props.searchValue)}>
                Search
            </button>
        </div>
    );
}


export default Menu;