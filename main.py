import tkinter as tk

# Tamanho do "mapa"
LARGURA = 10
ALTURA = 5
PASSO = 40  # Tamanho de cada bloco (em pixels)


player = {"x": 0, "y": 0}

def walk(direction):
    if direction == "w" and player["y"] > 0:
        player["y"] -= 1
    elif direction == "s" and player["y"] < ALTURA - 1:
        player["y"] += 1
    elif direction == "a" and player["x"] > 0:
        player["x"] -= 1
    elif direction == "d" and player["x"] < LARGURA - 1:
        player["x"] += 1

    mover_canvas()


def mover_canvas():
    x = player["x"] * PASSO
    y = player["y"] * PASSO
    canvas.coords(personagem, x, y, x + PASSO, y + PASSO)

def on_keypress(event):
    tecla = event.keysym.lower()
    walk(tecla)

janela = tk.Tk()
janela.title("Movimento do Personagem")

canvas = tk.Canvas(janela, width=LARGURA*PASSO, height=ALTURA*PASSO, bg="white")
canvas.pack()

personagem = canvas.create_rectangle(0, 0, PASSO, PASSO, fill="blue")

janela.bind("<Key>", on_keypress)

janela.mainloop()