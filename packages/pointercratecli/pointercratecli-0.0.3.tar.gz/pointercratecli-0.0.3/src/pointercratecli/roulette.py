import requests
import random
from rich.console import Console

console = Console()
console.print("Welcome to the demonlist randomizer!", style="bold red")

def getDemonlist():
    TOP100URL = "https://pointercrate.com/api/v2/demons/listed/?limit=100"
    TOP100TO150URL = "https://pointercrate.com/api/v2/demons/listed/?after=100"
    response100 = requests.get(TOP100URL)
    response150 = requests.get(TOP100TO150URL)
    demons100 = response100.json()
    demons150 = response150.json()
    demons = demons100 + demons150
    return demons


def main():
    percent = 1
    demons = getDemonlist()
    demonnames = []
    for demon in demons:
        demonnames.append(demon["name"])

    while percent <= 100:
        i = random.randint(0, len(demonnames) - 1)
        stringpercent = str(percent) + "%"
        console.print(stringpercent+ f": {demonnames[i]}", style="bold cyan")
        del demonnames[i]

        percent += 1


if __name__ == "__main__":
    main()
