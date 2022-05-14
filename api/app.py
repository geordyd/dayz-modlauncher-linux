from steamworks import STEAMWORKS
import steamworks
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


def SubscribeModItem(modid):
    steamworks.Workshop.SubscribeItem(modid)


def UnsubscribeModItem(modid):
    steamworks.Workshop.UnsubscribeItem(modid)
