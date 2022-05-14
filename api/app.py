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


# def SubscribeItem(modID):
#     steamworks.Workshop.SubscribeItem(modID)

# def UnsubscribeItem(modID):
#     steamworks.Workshop.UnsubscribeItem(modID)

# res = requests.get('https://api.battlemetrics.com/servers?filter[search]="193.25.252.34')

# response = json.loads(res.text)

# mods = response['data'][0]['attributes']['details']['modIds']

# def RunDayz():
#     subprocess.run(["steam", "-applaunch", "221100", "-connect=195.82.158.110:11500" "-nolauncher" "-world=empty" "-name=marco"])

# while True:
#     print("1: Subscribe\n2: Unsubscribe\n3: Run DayZ\n4: Exit")
#     choice = input("Enter a command: ")
#     if choice == "1":
#         for mod in mods:
#             if steamworks.Workshop.SetItemSubscribedCallback(SubscribeItem):
#                 SubscribeItem(mod)
#                 print("Subscribed to " + str(mod))
#     elif choice == "2":
#         for mod in mods:
#             if steamworks.Workshop.SetItemUnsubscribedCallback(UnsubscribeItem):
#                 UnsubscribeItem(mod)
#                 print("Unsubscribed from " + str(mod))
#     elif choice == "3":
#         RunDayz()
#         exit()
#     elif choice == "4":
#         exit()
#     else:
#         print("Invalid command")
