import shutil
import subprocess
import tarfile
from bs4 import BeautifulSoup
import requests
import os
from flask import Flask, request
from flask import jsonify
from pathlib import Path

app = Flask(__name__)


@app.route('/steamcmdinit')
def SteamCMDInit():
    if (not SteamCMDInstalled()):
        DownloadSteamCMD()
        ExtractSteamCMD()
        InstallSteamCMD()
    return "Ok"


@app.route("/getinstalledmods", methods=['GET'])
def GetInstalledMods():
    homeDir = str(Path.home())
    dayzModFolder = homeDir + '/.local/share/Steam/steamapps/workshop/content/221100/'

    folders = [f.path for f in os.scandir(dayzModFolder) if f.is_dir()]
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
        dayzModFolder) if os.path.isdir(os.path.join(dayzModFolder, name))]

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

    installCommand = ""

    for mod in content['data']:
        installCommand += f"+workshop_download_item 221100 {mod} "

    installCommand = installCommand[:-1]

    homeFolder = str(Path.home())
    steamCMDFolder = homeFolder + "/steamcmd/"
    os.chdir(steamCMDFolder)
    bashCmd = f"./steamcmd.sh +login anonymous {installCommand} +quit"
    print(bashCmd)
    process = subprocess.run(
        bashCmd, capture_output=True, text=True, shell=True)
    print(process.stdout)
    print(process.stderr)
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
    homeDir = str(Path.home())
    dayzModFolder = homeDir + '/.local/share/Steam/steamapps/workshop/content/221100/'
    folderExists = False
    for folderName in os.scandir(dayzModFolder):
        if(folderName.name == modid):
            folderExists = True
            break

    if not folderExists:
        return jsonify({"data": "Not installed"})
    else:
        return jsonify({"data": "Installed"})


@app.route("/deletemodbyid/<modid>", methods=['GET'])
def DeleteModById(modid):
    homeDir = str(Path.home())
    dayzModFolder = homeDir + '/.local/share/Steam/steamapps/workshop/content/221100/'
    modfolder = dayzModFolder + f"{modid}/"
    if CheckIfFolderExists(modfolder):
        shutil.rmtree(modfolder)
        RemoveSymlinkById(modid)
        return f"{modid} deleted"
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


def DownloadSteamCMD():
    homeFolder = str(Path.home())
    steamCMDUrl = "https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz"
    response = requests.get(steamCMDUrl)
    open(homeFolder + "/steamcmd_linux.tar.gz", "wb").write(response.content)


def ExtractSteamCMD():
    homeFolder = str(Path.home())
    with tarfile.open(homeFolder + "/steamcmd_linux.tar.gz", 'r:gz') as f:
        f.extractall(homeFolder + "/steamcmd")


def InstallSteamCMD():
    homeFolder = str(Path.home())
    steamCMDFolder = homeFolder + "/steamcmd/"
    os.chdir(steamCMDFolder)
    bashCmd = ["./steamcmd.sh", "+quit"]

    process = subprocess.run(bashCmd, capture_output=True, text=True)


def SteamCMDInstalled():
    homeFolder = str(Path.home())
    steamCMDFolder = homeFolder + "/steamcmd/"
    return CheckIfFolderExists(steamCMDFolder)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
