import requests
from rich.console import Console

console = Console()
listType = int(input("Show main (1) or extended (2): "))


def getDemonlistSize():
    demonlist = "https://pointercrate.com/api/v1/list_information"
    response = requests.get(demonlist)
    list = response.json()
    return list

if listType == 1:
    list = getDemonlistSize()
    console.print(f"Main demonlist size: {list['list_size']}", style="bold red")
elif listType == 2:
    list = getDemonlistSize()
    console.print(f"Extended demonlist size: {list['extended_list_size']}", style="bold red")
else:
    console.print("Invalid input!", style="bold red")
