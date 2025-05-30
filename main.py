import os

player = {"name": "Python", "x": 0, "y": 0}

def walk(direction):
    if direction == "d":
        player["x"] += 1
    elif direction == "a":
        player["x"] -= 1
    elif direction == "w":
        player["y"] -= 1
    elif direction == "s":
        player["y"] += 1 

while True:
    os.system("cls")
    
    print("---------------------------")
    for y in range(5):
        print("\n")
        for x in range(10):
            if player['x'] == x and player["y"] == y:
                print("🤖", end="")
            else:
                print("⬜", end="")
    print("\n---------------------------")

    direction = input("Próxima direção(W, A, S, D): ")
    walk(direction)
