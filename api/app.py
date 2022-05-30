import shutil
import subprocess
from bs4 import BeautifulSoup
import requests
import os
from flask import Flask, request, jsonify
from pathlib import Path
from steamCMD import SteamCMD

steamCMD = SteamCMD()

app = Flask(__name__)

dayzDir = ""

dayzModDir = ""


@app.route('/steamcmdinit')
def SteamCMDInit():
    steamCMD.Init()

    global dayzDir
    global dayzModDir

    if dayzDir == "" or dayzModDir == "":
        dayzDir = SteamCMD.GetDayzDir()
        dayzModDir = dayzDir.removesuffix(
            'common/DayZ') + "workshop/content/221100/"

    return "Ok"


@app.route("/getinstalledmods", methods=['GET'])
def GetInstalledMods():

    global dayzModDir

    folders = [f.path for f in os.scandir(dayzModDir) if f.is_dir()]
    modNames = []
    for folderName in folders:
        fileName = os.path.join(folderName, 'meta.cpp')
        if os.path.exists(fileName):
            with open(fileName, 'r') as f:
                for line in f:
                    if 'name' in line:
                        modName = line.split('"')[1]
                        modNames.append(modName)
                        break
        else:
            modNames.append("Name not available")

    subFolders = [name for name in os.listdir(
        dayzModDir) if os.path.isdir(os.path.join(dayzModDir, name))]

    modsInfo = []
    for index, subFolder in enumerate(subFolders):
        modInfo = {}
        modInfo['name'] = modNames[index]
        modInfo['id'] = subFolder
        modsInfo.append(modInfo)

    return jsonify({"data": list(modsInfo)})


@app.route("/installmods", methods=['GET', 'POST'])
def InstallMods():
    content = request.get_json()

    installCommand = []

    for mod in content['data']:
        installCommand.append(f"+workshop_download_item 221100 {mod}")

    homeFolder = str(Path.home())
    steamCMDFolder = homeFolder + "/steamcmd/"
    os.chdir(steamCMDFolder)
    bashCmd = ["./steamcmd.sh", "+login anonymous"]

    for command in installCommand:
        bashCmd.append(command)

    bashCmd.append("+quit")

    print(bashCmd)

    process = subprocess.Popen(
        bashCmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    for line in iter(process.stdout.readline, b''):
        print(">>> " + str(line.rstrip()))

    return jsonify({"data": "Mods installed"})


@app.route("/installmod/<modid>", methods=['GET'])
def SubscribeMod(modid):
    homeFolder = str(Path.home())
    steamCMDFolder = homeFolder + "/steamcmd/"
    os.chdir(steamCMDFolder)
    bashCmd = ["./steamcmd.sh", "+login anonymous",
               "+workshop_download_item 221100 " + modid, "+quit"]

    process = subprocess.run(bashCmd, capture_output=True, text=True)

    return f"Subscribed to {modid}"


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

    global dayzModDir

    folderExists = False
    for folderName in os.scandir(dayzModDir):
        if(folderName.name == modid):
            folderExists = True
            break

    if not folderExists:
        return jsonify({"data": "Not installed"})
    else:
        return jsonify({"data": "Installed"})


@app.route("/deletemodbyid/<modid>", methods=['GET'])
def DeleteModById(modid):

    global dayzModDir

    modfolder = dayzModDir + f"{modid}/"
    if CheckIfFolderExists(modfolder):
        shutil.rmtree(modfolder)
        RemoveSymlinkById(modid)
        return f"{modid} deleted"
    return f"{modid} does not exist"


@app.route("/createsymlinks")
def CreateSymLinks():

    global dayzDir

    folders = [f.path for f in os.scandir(dayzModDir) if f.is_dir()]

    for folderName in folders:
        modName = folderName.split('/')[-1]
        try:
            os.symlink(folderName, dayzDir + f"@{modName}")
        except:
            continue

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
    global dayzDir

    try:
        os.remove(dayzDir + f"@{modid}")
    except:
        print(f"Symlink of {modid} does not exist")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
