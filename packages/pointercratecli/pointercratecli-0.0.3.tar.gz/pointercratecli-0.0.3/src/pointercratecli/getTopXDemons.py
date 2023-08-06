import requests
from rich.console import Console

console = Console()
limit = int(input("How many demons do you want to show: "))


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
    demons = getDemonlist()
    demonnames = []
    for i in range(limit):
        console.print(f"{i+1}: {demons[i]['name']}", style="bold cyan")



if __name__ == "__main__":
    main()
