import React, { useState } from 'react';
import './App.css';
import Menu from './components/Menu/Menu';
function App() {

  // useEffect(() => {
  //   fetch('/time').then(res => res.json()).then(data => {
  //     setCurrentTime(data.time);
  //   });
  // }, []);
  
  const [searchValue, setSearchValue] = useState('test');

  return (
    <div className="wrapper">
      <div className="menu">
        <Menu searchValue={searchValue} setSearchValue={setSearchValue} />
      </div>
      <div className="browser">
        {searchValue}
      </div>
      <div className="console">

      </div>  
    </div>
  );
}

export default App;
