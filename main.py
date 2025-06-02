import tkinter as tk
from tkinter import messagebox
import random


# Tamanho do "mapa"
LARGURA = 30
ALTURA = 10
PASSO = 40  # Tamanho de cada bloco (em pixels)


player = {"x": 0, "y": 0}

inimigo = {"x": 15, "y": 8}

paredes = [
    (3, 3), (3, 4), (3, 5), (4, 6), (5, 3), (5, 4), (5, 5),

    (7, 3), (7, 4), (7, 5), (7, 6),
     
    (9, 3), (9, 4), (9, 5), (9, 6), (10, 3), (10, 6), (11, 3), (11, 6),

    (13, 3), (14, 3), (14, 4), (14, 5), (14, 6), (15, 3),

    (17, 3), (17, 4), (17, 5), (17, 6), (18, 3), (18, 6), (19, 3), (19, 4), (19, 5), (19, 6),

    (21, 3), (21, 4), (21, 5), (21, 6), (22, 3), (22, 5), (23, 3), (23, 4), (23, 6)
]

objetivo = (29, 9)  # canto inferior direito

def walk(direction):
    novo_x = player["x"]
    novo_y = player["y"]

    if direction == "w" and player["y"] > 0:
        novo_y -= 1
    elif direction == "s" and player["y"] < ALTURA - 1:
        novo_y += 1
    elif direction == "a" and player["x"] > 0:
        novo_x -= 1
    elif direction == "d" and player["x"] < LARGURA - 1:
        novo_x += 1

    if (novo_x, novo_y) not in paredes:
        player["x"] = novo_x
        player["y"] = novo_y
        mover_canvas()

    if (player["x"], player["y"]) == objetivo:
        messagebox.showinfo("Vitória!", "Parabéns, você venceu!")
        janela.destroy()

def mover_canvas():
    x = player["x"] * PASSO
    y = player["y"] * PASSO
    canvas.coords(personagem, x, y, x + PASSO, y + PASSO)

def desenhar_grade():
    for y in range(ALTURA):
        for x in range(LARGURA):
            canvas.create_rectangle(
                x * PASSO,
                y * PASSO,
                (x + 1) * PASSO,
                (y + 1) * PASSO,
                outline="gray",  # cor da linha da grade
                fill="white"
            )
        # Desenhar as paredes (obstáculos)
    for parede in paredes:
        px, py = parede
        canvas.create_rectangle(
            px * PASSO, py * PASSO,
            (px + 1) * PASSO, (py + 1) * PASSO,
            fill="black"
        )

        # Desenhar o objetivo
    ox, oy = objetivo
    canvas.create_rectangle(
        ox * PASSO, oy * PASSO,
        (ox + 1) * PASSO, (oy + 1) * PASSO,
        fill="green"
    )



def on_keypress(event):
    tecla = event.keysym.lower()
    walk(tecla)

def mover_inimigo():
    direcoes = ["w", "a", "s", "d"]
    direcao = random.choice(direcoes)

    dx, dy = 0, 0
    if direcao == "w": dy = -1
    elif direcao == "s": dy = 1
    elif direcao == "a": dx = -1
    elif direcao == "d": dx = 1

    novo_x = inimigo["x"] + dx
    novo_y = inimigo["y"] + dy

    if (0 <= novo_x < LARGURA and 0 <= novo_y < ALTURA and (novo_x, novo_y) not in paredes):
        inimigo["x"] = novo_x
        inimigo["y"] = novo_y
        canvas.coords(
            inimigo_sprite,
            inimigo["x"] * PASSO, inimigo["y"] * PASSO,
            (inimigo["x"] + 1) * PASSO, (inimigo["y"] + 1) * PASSO
        )

    verificar_colisao()

    # Chama de novo em 500ms
    janela.after(200, mover_inimigo)

def verificar_colisao():
    if player["x"] == inimigo["x"] and player["y"] == inimigo["y"]:
        messagebox.showerror("Game Over", "Você é um perdedor!")
        janela.destroy()


janela = tk.Tk()
janela.title("PlayMove")

canvas = tk.Canvas(janela, width=LARGURA*PASSO, height=ALTURA*PASSO, bg="white")
canvas.pack()

desenhar_grade()

personagem = canvas.create_rectangle(0, 0, PASSO, PASSO, fill="blue")

inimigo_sprite = canvas.create_rectangle(
    inimigo["x"] * PASSO, inimigo["y"] * PASSO,
    (inimigo["x"] + 1) * PASSO, (inimigo["y"] + 1) * PASSO,
    fill="red"
)

janela.bind("<Key>", on_keypress)

mover_inimigo()
janela.mainloop()