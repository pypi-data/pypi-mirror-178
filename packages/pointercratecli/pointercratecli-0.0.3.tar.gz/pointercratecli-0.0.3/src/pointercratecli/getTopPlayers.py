import requests
from rich.console import Console

console = Console()
console.print("Here you can find the current top players: ", style="bold red")

def getTopPlayers():
    playerLimit = int(input("How many players do you want to see (Max: 500): "))
    if playerLimit <= 100:
        TOP100URL = "https://pointercrate.com/api/v1/players/ranking/?limit=100"
        response = requests.get(TOP100URL)
        players = response.json()
        return players, playerLimit
    elif playerLimit <= 200 and playerLimit > 100:
        TOP100URL = "https://pointercrate.com/api/v1/players/ranking/?limit=100"
        TOP200URL = "https://pointercrate.com/api/v1/players/ranking/?limit=100&after=100"
        response100 = requests.get(TOP100URL)
        response200 = requests.get(TOP200URL)
        players100 = response100.json()
        players200 = response200.json()
        players = players100 + players200
        return players, playerLimit
    elif playerLimit <= 300 and playerLimit > 200:
        TOP100URL = "https://pointercrate.com/api/v1/players/ranking/?limit=100"
        TOP200URL = "https://pointercrate.com/api/v1/players/ranking/?limit=100&after=100"
        TOP300URL = "https://pointercrate.com/api/v1/players/ranking/?limit=100&after=200"
        response100 = requests.get(TOP100URL)
        response200 = requests.get(TOP200URL)
        response300 = requests.get(TOP300URL)
        players100 = response100.json()
        players200 = response200.json()
        players300 = response300.json()
        players = players100 + players200 + players300
        return players, playerLimit
    elif playerLimit <= 400 and playerLimit > 300:
        TOP100URL = "https://pointercrate.com/api/v1/players/ranking/?limit=100"
        TOP200URL = "https://pointercrate.com/api/v1/players/ranking/?limit=100&after=100"
        TOP300URL = "https://pointercrate.com/api/v1/players/ranking/?limit=100&after=200"
        TOP400URL = "https://pointercrate.com/api/v1/players/ranking/?limit=100&after=300"
        response100 = requests.get(TOP100URL)
        response200 = requests.get(TOP200URL)
        response300 = requests.get(TOP300URL)
        response400 = requests.get(TOP400URL)
        players100 = response100.json()
        players200 = response200.json()
        players300 = response300.json()
        players400 = response400.json()
        players = players100 + players200 + players300 + players400
        return players, playerLimit
    elif playerLimit <= 500 and playerLimit > 400:
        TOP100URL = "https://pointercrate.com/api/v1/players/ranking/?limit=100"
        TOP200URL = "https://pointercrate.com/api/v1/players/ranking/?limit=100&after=100"
        TOP300URL = "https://pointercrate.com/api/v1/players/ranking/?limit=100&after=200"
        TOP400URL = "https://pointercrate.com/api/v1/players/ranking/?limit=100&after=300"
        TOP500URL = "https://pointercrate.com/api/v1/players/ranking/?limit=100&after=400"
        response100 = requests.get(TOP100URL)
        response200 = requests.get(TOP200URL)
        response300 = requests.get(TOP300URL)
        response400 = requests.get(TOP400URL)
        response500 = requests.get(TOP500URL)
        players100 = response100.json()
        players200 = response200.json()
        players300 = response300.json()
        players400 = response400.json()
        players500 = response500.json()
        players = players100 + players200 + players300 + players400 + players500
        return players, playerLimit
    else:
        print("You can only see up to 500 players.")
        getTopPlayers()

def main():
    players, playerLimit = getTopPlayers()
    playerNames = []
    print("Top " + str(playerLimit) + " players:")
    for player in players:
        playerNames.append(player["name"])
    for i in range(playerLimit):
        print(str(i + 1) + ". " + playerNames[i])


if __name__ == "__main__":
    main()
