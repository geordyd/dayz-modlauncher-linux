const electron = require("electron");
const app = electron.app;
const BrowserWindow = electron.BrowserWindow;
const path = require("path");
const isDev = require("electron-is-dev");
var subpy = require( "child_process" );

let mainWindow;

function createWindow() {
mainWindow = new BrowserWindow({ width: 1280, height: 720 });
    mainWindow.loadURL(isDev ? "http://localhost:3000": 
        `file://${path.join(__dirname, "../build/index.html")}`);

    mainWindow.on("closed", () => {
        mainWindow = null
        subpy.kill( "SIGINT" );
    });
}

app.on("ready", function(){
    subpy.spawn( "python", [ "app.py" ] )
    // var subpy = require( "child_process" ).spawn( "./dist/hello.exe" );
    var rp = require( "request-promise" );
    var mainAddr = "http://127.0.0.1:5000";


    var StartUp = function()
    {
        rp( mainAddr )
        .then(
            function( htmlString )
            {
                console.log( "server started!" );
                createWindow();
            }
        )
        .catch(
            function( err )
            {
                console.log( "waiting for the server start..." );
                // without tail call optimization this is a potential stack overflow
                StartUp();
            }
        );
    };

    // fire!
    StartUp();
});

app.on("window-all-closed", () => {
    if (process.platform !== "darwin") {
        app.quit();
    }
});

app.on("activate", () => {
    if (mainWindow === null) {
        createWindow();
    }
});