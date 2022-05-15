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

    subFolders = [name for name in os.listdir(
        folder) if os.path.isdir(os.path.join(folder, name))]

    return jsonify({"data": list(subFolders)})


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

    modName = parsed_html.find('div', attrs={'class': 'workshopItemTitle'}).text

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

    modName = parsed_html.find('div', attrs={'class': 'workshopItemTitle'}).text

    return modName

def SubscribeModItem(modid):
    steamworks.Workshop.SubscribeItem(modid)


def UnsubscribeModItem(modid):
    steamworks.Workshop.UnsubscribeItem(modid)
