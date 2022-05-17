import shutil
from bs4 import BeautifulSoup
import requests
from steamworks import STEAMWORKS
import os
from flask import Flask
from flask import jsonify
from pathlib import Path

app = Flask(__name__)

steamworks = STEAMWORKS()

steamworks.initialize()


@app.route("/getsubscribedmods", methods=['GET'])
def GetSubscribedMods():
    subscribedItems = steamworks.Workshop.GetSubscribedItems()
    return jsonify({"data": list(subscribedItems)})


@app.route("/getinstalledmods", methods=['GET'])
def GetInstalledMods():
    homeDir = str(Path.home())
    dayzModFolder = homeDir + '/.local/share/Steam/steamapps/workshop/content/221100/'

    folders = [f.path for f in os.scandir(dayzModFolder) if f.is_dir()]
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
        dayzModFolder) if os.path.isdir(os.path.join(dayzModFolder, name))]

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
            RemoveSymlinkById(modid)
            return f"{modid} deleted"
        except:
            return f"{modid} does not exist"

    return f"{modid} does not exist"

@app.route("/createsymlinks")
def CreateSymLinks():
    homeDir = str(Path.home())
    dayzModFolder = homeDir + '/.local/share/Steam/steamapps/workshop/content/221100/'
    
    stringToRemove = 'workshop/content/221100/'
    stringToAdd = 'common/DayZ/'
    dayzFolder = dayzModFolder.replace(stringToRemove, '')
    dayzFolder += stringToAdd

    folders = [f.path for f in os.scandir(dayzModFolder) if f.is_dir()]

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

def RemoveSymlinkById(modid):
    homeDir = str(Path.home())
    dayzModFolder = homeDir + '/.local/share/Steam/steamapps/workshop/content/221100/'
    
    stringToRemove = 'workshop/content/221100/'
    stringToAdd = 'common/DayZ/'
    dayzFolder = dayzModFolder.replace(stringToRemove, '')
    dayzFolder += stringToAdd

    try:
        os.remove(dayzFolder + f"@{modid}")
    except:
        print(f"Symlink of {modid} does not exist")


def SubscribeModItem(modid):
    steamworks.Workshop.SubscribeItem(modid)


def UnsubscribeModItem(modid):
    steamworks.Workshop.UnsubscribeItem(modid)
