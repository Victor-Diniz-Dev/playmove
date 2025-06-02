import tkinter as tk
from tkinter import messagebox
import random


# Tamanho do "mapa"
LARGURA = 43
ALTURA = 25
PASSO = 40  # Tamanho de cada bloco (em pixels)


player = {"x": 1, "y": 1}

inimigo = {"x": 15, "y": 8}

paredes = [
    # Moldura
    *[(x, 0) for x in range(43)],
    *[(x, 24) for x in range(43)],
    *[(0, y) for y in range(25)],
    *[(42, y) for y in range(25)],

    # Paredes horizontais internas
    *[(x, 5) for x in range(2, 41) if x % 3 != 0],
    *[(x, 10) for x in range(1, 42) if x % 4 != 0],
    *[(x, 15) for x in range(2, 41) if x % 5 != 0],

    # Paredes verticais internas
    *[(5, y) for y in range(2, 22) if y % 3 != 0],
    *[(15, y) for y in range(3, 20) if y % 4 != 0],
    *[(30, y) for y in range(1, 24) if y % 5 != 0]
]

objetivo = (31, 4)  # canto inferior direito

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
            fill="#4B4B4B", outline="black"
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
    dx = dy = 0
    dist_x = abs(inimigo["x"] - player["x"])
    dist_y = abs(inimigo["y"] - player["y"])

    # Decide prioridade com base na maior distância
    if dist_x > dist_y:
        direcoes_preferidas = [
            (1 if inimigo["x"] < player["x"] else -1, 0),  # mover no eixo X
            (0, 1 if inimigo["y"] < player["y"] else -1),  # depois no eixo Y
        ]
    else:
        direcoes_preferidas = [
            (0, 1 if inimigo["y"] < player["y"] else -1),  # mover no eixo Y
            (1 if inimigo["x"] < player["x"] else -1, 0),  # depois no eixo X
        ]

    # Adiciona tentativas diagonais e reversas como último recurso
    direcoes_preferidas += [
        (1 if inimigo["x"] < player["x"] else -1, 1 if inimigo["y"] < player["y"] else -1),
        (-direcoes_preferidas[0][0], 0),
        (0, -direcoes_preferidas[1][1])
    ]

    for dx, dy in direcoes_preferidas:
        novo_x = inimigo["x"] + dx
        novo_y = inimigo["y"] + dy

        if (
            0 <= novo_x < LARGURA and
            0 <= novo_y < ALTURA and
            (novo_x, novo_y) not in paredes
        ):
            # Verifica se o movimento é diagonal
            if dx != 0 and dy != 0:
                # Se for, impede se houver parede na horizontal ou vertical adjacente
                if ((inimigo["x"] + dx, inimigo["y"]) in paredes or
                    (inimigo["x"], inimigo["y"] + dy) in paredes):
                    continue  # Pula para a próxima direção

            # Movimento permitido
            inimigo["x"] = novo_x
            inimigo["y"] = novo_y
            canvas.coords(
                inimigo_sprite,
                inimigo["x"] * PASSO, inimigo["y"] * PASSO,
                (inimigo["x"] + 1) * PASSO, (inimigo["y"] + 1) * PASSO
            )
            break



    verificar_colisao()
    janela.after(200, mover_inimigo)


def verificar_colisao():
    if player["x"] == inimigo["x"] and player["y"] == inimigo["y"]:
        messagebox.showerror("Game Over", "Você é um perdedor!")
        janela.destroy()


janela = tk.Tk()
janela.title("playmove")

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

def iniciar_jogo():
    mover_inimigo()

def mostrar_boas_vindas():
    messagebox.showinfo("Bem-vindo!", "Pressione OK para iniciar o jogo.")
    janela.focus_force()
    iniciar_jogo()

# Espera a janela carregar antes de mostrar a messagebox
janela.after(100, mostrar_boas_vindas)

janela.mainloop()