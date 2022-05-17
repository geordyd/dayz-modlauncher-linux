import shutil
from bs4 import BeautifulSoup
import requests
from steamworks import STEAMWORKS
import os
from flask import Flask
from flask import jsonify

app = Flask(__name__)

steamworks = STEAMWORKS()

steamworks.initialize()


@app.route( "/" )
def hello():
    return "Hello World! This is powered by a Python backend."

@app.route("/getsubscribedmods", methods=['GET'])
def GetSubscribedMods():
    subscribedItems = steamworks.Workshop.GetSubscribedItems()
    return jsonify({"data": list(subscribedItems)})


@app.route("/getinstalledmods", methods=['GET'])
def GetInstalledMods():
    subscribedMod = steamworks.Workshop.GetSubscribedItems(1)
    modInstallInfo = steamworks.Workshop.GetItemInstallInfo(subscribedMod[0])
    installFolderMod = modInstallInfo['folder']
    installFolderWithoutMod = installFolderMod.replace(
        f"{subscribedMod[0]}", '')
    folder = installFolderWithoutMod

    folders = [f.path for f in os.scandir(folder) if f.is_dir()]
    modNames = []
    for folderName in folders:
        # get file by filename from folder
        fileName = os.path.join(folderName, 'meta.cpp')
        if os.path.exists(fileName):
            # read the file
            with open(fileName, 'r') as f:
                for line in f:
                    if 'name' in line:
                        modName = line.split('"')[1]
                        modNames.append(modName)
                        break

    subFolders = [name for name in os.listdir(
        folder) if os.path.isdir(os.path.join(folder, name))]

    modsInfo = []
    for index, subFolder in enumerate(subFolders):
        modInfo = {}
        modInfo['name'] = modNames[index]
        modInfo['id'] = subFolder
        modsInfo.append(modInfo)

    return jsonify({"data": list(modsInfo)})


@app.route("/subscribemod/<modid>", methods=['GET'])
def SubscribeMod(modid):
    steamworks.Workshop.SetItemSubscribedCallback(SubscribeModItem)
    steamworks.Workshop.SubscribeItem(int(modid))
    return f"Subscribed to {modid}"


@app.route("/unsubscribemod/<modid>", methods=['GET'])
def UnsubscribeMod(modid):
    steamworks.Workshop.SetItemUnsubscribedCallback(UnsubscribeModItem)
    steamworks.Workshop.UnsubscribeItem(int(modid))
    return f"Unsubscribed from {modid}"


@app.route("/getmodnamebyid/<modid>", methods=['GET'])
def GetModNameById(modid):
    res = requests.get(
        f'https://steamcommunity.com/sharedfiles/filedetails/?id={modid}')
    html = res.text

    parsed_html = BeautifulSoup(html, 'html.parser')

    modName = parsed_html.find(
        'div', attrs={'class': 'workshopItemTitle'}).text

    return jsonify({"data": modName})


@app.route("/getmodstatebyid/<modid>", methods=['GET'])
def GetModStatusById(modid):
    modstate = steamworks.Workshop.GetItemInstallInfo(int(modid))
    if modstate == {}:
        return jsonify({"data": "Not installed"})
    else:
        if CheckIfFolderExists(modstate['folder']):
            return jsonify({"data": "Installed"})
        else:
            return jsonify({"data": "Not installed"})


@app.route("/deletemodbyid/<modid>", methods=['GET'])
def DeleteModById(modid):
    modstate = steamworks.Workshop.GetItemInstallInfo(int(modid))
    if modstate != {}:
        modfolder = modstate['folder']
        try:
            shutil.rmtree(modfolder)
            return f"{modid} deleted"
        except:
            return f"{modid} does not exist"

    return f"{modid} does not exist"

@app.route("/createsymlinks")
def CreateSymLinks():
    subscribedMod = steamworks.Workshop.GetSubscribedItems(1)
    modInstallInfo = steamworks.Workshop.GetItemInstallInfo(subscribedMod[0])
    installFolderMod = modInstallInfo['folder']
    installFolderWithoutMod = installFolderMod.replace(
        f"{subscribedMod[0]}", '')
    folder = installFolderWithoutMod
    
    stringToRemove = 'workshop/content/221100/'
    stringToAdd = 'common/DayZ/'
    dayzFolder = folder.replace(stringToRemove, '')
    dayzFolder += stringToAdd

    folders = [f.path for f in os.scandir(folder) if f.is_dir()]

    for folderName in folders:
        modName = folderName.split('/')[-1]
        try:
            os.symlink(folderName, dayzFolder + f"@{modName}")
        except:
            print(f"Symlink of {modName} already exists")

    return "Ok"

def CheckIfFolderExists(folderPath):
    if os.path.exists(folderPath):
        return True
    else:
        return False


def GetInstalledModNamesById(modid):
    res = requests.get(
        f'https://steamcommunity.com/sharedfiles/filedetails/?id={modid}')
    html = res.text

    parsed_html = BeautifulSoup(html, 'html.parser')

    modName = parsed_html.find(
        'div', attrs={'class': 'workshopItemTitle'}).text

    return modName


def SubscribeModItem(modid):
    steamworks.Workshop.SubscribeItem(modid)


def UnsubscribeModItem(modid):
    steamworks.Workshop.UnsubscribeItem(modid)

if __name__ == "__main__":
    print( "oh hello" )
    #time.sleep(5)
    app.run( host = "127.0.0.1", port = 5000 )