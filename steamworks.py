from steamworks import STEAMWORKS
import steamworks
import requests
import json
import subprocess

steamworks = STEAMWORKS()

steamworks.initialize()

def SubscribeItem(modID):
    steamworks.Workshop.SubscribeItem(modID)

def UnsubscribeItem(modID):
    steamworks.Workshop.UnsubscribeItem(modID)

res = requests.get('https://api.battlemetrics.com/servers?filter[search]="193.25.252.34')

response = json.loads(res.text)

mods = response['data'][0]['attributes']['details']['modIds']

def RunDayz():
    subprocess.run(["steam", "-applaunch", "221100", "-connect=195.82.158.110:11500" "-nolauncher" "-world=empty" "-name=marco"])

while True:
    print("1: Subscribe\n2: Unsubscribe\n3: Run DayZ\n4: Exit")
    choice = input("Enter a command: ")
    if choice == "1":
        for mod in mods:
            if steamworks.Workshop.SetItemSubscribedCallback(SubscribeItem):
                SubscribeItem(mod)
                print("Subscribed to " + str(mod))
    elif choice == "2":
        for mod in mods:
            if steamworks.Workshop.SetItemUnsubscribedCallback(UnsubscribeItem):
                UnsubscribeItem(mod)
                print("Unsubscribed from " + str(mod))
    elif choice == "3":
        RunDayz()
        exit()
    elif choice == "4":
        exit()
    else:
        print("Invalid command")