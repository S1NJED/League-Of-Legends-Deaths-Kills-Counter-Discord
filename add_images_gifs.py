import json, os

print("Add images or gifs to the config.json file for the embedded discord message when you die or kill\n")
EXTENSIONS = ["gif", "png", "jpg", "jpeg", "bmp", "webp"]
CWD = os.path.dirname(__file__)
CONFIG_JSON_ABS_PATH = os.path.join(CWD, 'config.json')
CONFIG = json.loads( open(CONFIG_JSON_ABS_PATH, 'r').read() )
URLS = {}

while True:
    print("* Choose a eventType:\n")
    print("[1] DEATHS")
    print("[2] KILLS")
    print("[3] exit.")
    print("Press 1 or 2")
    
    choice = str(input("> "))
    
    # exit
    if choice == "3":
        break
    if choice not in ["1", "2", "3"]:
        print("Make sure to choose between 1 or 2\n")
        continue
    
    eventType = ""
    if choice == "1": # DEATHS
        eventType = "DEATHS"
    else:
        eventType = "KILLS"

    while True:
        print("Enter a valid images/gifs url, make sure it finish by a valid extension:")
        print("(Type exit to exit)")
        url = str(input("> "))
        if url == "exit": 
            break
        
        if not any(url.endswith(ext) for ext in EXTENSIONS):
            print("The url you provided do not specify a valid extensions name")
            print("Make sure it finish by theses ones: " + ', '.join(EXTENSIONS))
            continue
        
        again = False
        while True:
            print("Are you sure ? ")
            print("y or n")
            confirm = str(input("> ")).lower()
            if not confirm in ['y', 'n']:
                continue
            if confirm == "n":
                again = True
            break
        if again:
            continue

        with open(CONFIG_JSON_ABS_PATH, 'w') as file:
            CONFIG[eventType + "_MESSAGE_IMAGES_GIFS_URLS"].append(url)
            try:
                json.dump(CONFIG, file, indent=4)
                print(f"Sucessfully add {url} to {eventType}_MESSAGE_IMAGES_GIFS_URLS")
            except Exception as err:
                print(err)
            