import requests
import sys
import os


def getdemonlist():
    print("Getting demonlist... Please wait.")
    top100_url = "https://pointercrate.com/api/v2/demons/listed/?limit=100"
    top100_to200_url = "https://pointercrate.com/api/v2/demons/listed/?limit=100&after=100"
    top200_to300_url = "https://pointercrate.com/api/v2/demons/listed/?limit=100&after=200"
    top300_to400_url = "https://pointercrate.com/api/v2/demons/listed/?limit=100&after=300"
    top400_tomax_url = "https://pointercrate.com/api/v2/demons/listed/?limit=100&after=400"
    response100 = requests.get(top100_url)
    response200 = requests.get(top100_to200_url)
    response300 = requests.get(top200_to300_url)
    response400 = requests.get(top300_to400_url)
    responsemax = requests.get(top400_tomax_url)
    demonsfinal = response100.json()+response200.json()+response300.json()+response400.json()+responsemax.json()

    if sys.platform == "win32":
        os.system("clear")
    else:
        os.system("clear")

    return demonsfinal


def menu(demonlist):
    print("Demonlist Search")
    print("1. Search by name")
    print("2. Search by position")
    print("3. Search by publisher")
    print("4. Search by verifier")
    print("5. Search by list requirement")
    print("6. Search by ID")
    print("7. Search by level ID")

    choice = input("Enter your choice: ")
    if choice == "1":
        namesearch(demonlist)
    elif choice == "2":
        possearch(demonlist)
    elif choice == "3":
        pubsearch(demonlist)
    elif choice == "4":
        versearch(demonlist)
    elif choice == "5":
        reqsearch(demonlist)
    elif choice == "6":
        idsearch(demonlist)
    elif choice == "7":
        levelSearch(demonlist)
    else:
        print("Invalid choice")
        menu(demonlist)


def namesearch(demons):
    found = False
    name = input("Enter demon name: ")
    for demon in demons:
        if name.lower() in demon["name"].lower():
            printDemon(demon)
            found = True
    if not found:
        print("Level not found")
    menu(demons)


def possearch(demons):
    found = False
    pos = input("Enter level position: ")
    try:
        if int(pos) > 447:
            print("Invalid position")
        else:
            for demon in demons:
                if demon["position"] == int(pos):
                    printDemon(demon)
                    found = True
            if not found:
                print("Demon not found")
    except ValueError:
        print("Invalid position")
    menu(demons)


def pubsearch(demons):
    found = False
    pub = input("Enter level publisher: ")
    for demon in demons:
        if pub.lower() in demon["publisher"]["name"].lower():
            printDemon(demon)
            found = True
    if not found:
        print("Level not found")
    menu(demons)


def versearch(demons):
    found = False
    ver = input("Enter level verifier: ")
    for demon in demons:
        if ver.lower() in demon["verifier"]["name"].lower():
            printDemon(demon)
            found = True
    if not found:
        print("Level not found")
    menu(demons)


def reqsearch(demons):
    found = False
    req = input("Enter list requirement: ")
    try:
        for demon in demons:
            if demon["requirement"] == int(req):
                printDemon(demon)
                found = True
        if not found:
            print("Level not found")
    except ValueError:
        print("Invalid requirement")
    menu(demons)


def idsearch(demons):
    found = False
    id = input("Enter demon ID: ")
    try:
        for demon in demons:
            if demon["id"] == int(id):
                printDemon(demon)
                found = True
        if not found:
            print("Level not found")
    except ValueError:
        print("Invalid ID", style="bold red")
    menu(demons)


def levelSearch(demons):
    found = False
    level = input("Enter demon level ID: ")
    try:
        for demon in demons:
            if demon["level"] == int(level):
                printDemon(demon)
                found = True
        if not found:
            print("Level not found")
    except ValueError:
        print("Invalid level ID")
    menu(demons)


def printDemon(demon):
    print("\n")
    print(f"Name: {demon['name']}")
    print(f"Position: {demon['position']}")
    print(f"Publisher: {demon['publisher']['name']}")
    print(f"Verifier: {demon['verifier']['name']}")

    if demon["position"] > 150:
        print(f"List Requirement: N/A (Legacy)")
    elif demon['position'] <= 75 or demon['requirement'] == 100:
        print(f"List Requirement: {demon['requirement']}%")
    else:
        print(f"List Requirement: 100%")

    print(f"ID: {demon['id']}")
    print(f"Level ID: {demon['level_id']}")
    print(f"Video: {demon['video']}")
    print(f"Thumbnail: {demon['thumbnail']}")
    print("\n")


if __name__ == "__main__":
    demons = getdemonlist()
    menu(demons)
