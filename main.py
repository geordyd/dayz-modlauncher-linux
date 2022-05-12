from steamworks import STEAMWORKS
import steamworks

steamworks = STEAMWORKS()

steamworks.initialize()

def subscribeItem():
    steamworks.Workshop.SubscribeItem(2770978238)

while True:
    choice = input("Enter a command: ")
    if choice == "1":
        try:
            steamworks.Workshop.SetItemSubscribedCallback(subscribeItem)
            subscribeItem()
            print("subscribed")
        except:
            print("Already subscribed")
    elif choice == "2":
        quit()
    else:
        print("Invalid command") 


