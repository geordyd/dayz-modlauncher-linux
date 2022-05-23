import os
from pathlib import Path
import subprocess
import tarfile
import requests


class SteamCMD:
    def Init(self):
        if not self.IsInstalled():
            self.Download()
            self.Extract()
            self.Install()

    def Download(self):
        homeFolder = str(Path.home())
        steamCMDUrl = "https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz"
        response = requests.get(steamCMDUrl)
        open(homeFolder + "/steamcmd_linux.tar.gz", "wb").write(response.content)

    def Extract(self):
        homeFolder = str(Path.home())
        with tarfile.open(homeFolder + "/steamcmd_linux.tar.gz", 'r:gz') as f:
            f.extractall(homeFolder + "/steamcmd")

    def Install(self):
        homeFolder = str(Path.home())
        steamCMDFolder = homeFolder + "/steamcmd/"
        os.chdir(steamCMDFolder)
        bashCmd = ["./steamcmd.sh", "+quit"]

        process = subprocess.run(bashCmd, capture_output=True, text=True)

    def IsInstalled(self):
        homeFolder = str(Path.home())
        steamCMDFolder = homeFolder + "/steamcmd/"
        return self.CheckIfFolderExists(steamCMDFolder)

    def CheckIfFolderExists(self, folderPath):
        if os.path.exists(folderPath):
            return True
        else:
            return False
