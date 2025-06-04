import tkinter as tk
from tkinter import messagebox
import random

# Tamanho lógico do mapa (número de colunas e linhas)
LARGURA = 43
ALTURA  = 25

# (Não usamos mais PASSO fixo neste trecho, pois vamos recalcular abaixo!)
# PASSO = 40  # <-- removido, será substituído por block_size

player = {"x": 1, "y": 1}
inimigo = {"x": 15, "y": 8}

paredes = [
    # Moldura externa
    *[(x, 0) for x in range(LARGURA)],
    *[(x, ALTURA - 1) for x in range(LARGURA)],
    *[(0, y) for y in range(ALTURA)],
    *[(LARGURA - 1, y) for y in range(ALTURA)],

    # Paredes horizontais internas (exemplo de labirinto)
    *[(x, 5)  for x in range(2, 41) if x % 3 != 0],
    *[(x, 10) for x in range(1, 42) if x % 4 != 0],
    *[(x, 15) for x in range(2, 41) if x % 5 != 0],

    # Paredes verticais internas
    *[(5, y)  for y in range(2, 23) if y % 3 != 0],
    *[(15, y) for y in range(3, 21) if y % 4 != 0],
    *[(30, y) for y in range(1, 24) if y % 5 != 0]
]

# Objetivo para vencer
objetivo = (31, 4)


# --------------------------------------
#   Funções de lógica do jogo (sem mudanças)
# --------------------------------------

def walk(direction, block_size):
    """
    Move o jogador ("player") uma célula em w/a/s/d, 
    mas só se não houver parede.
    """
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

    # Se a nova posição não for parede, atualiza
    if (novo_x, novo_y) not in paredes:
        player["x"] = novo_x
        player["y"] = novo_y
        mover_canvas(block_size)

    # Verifica vitória
    if (player["x"], player["y"]) == objetivo:
        messagebox.showinfo("Vitória!", "Parabéns, você venceu!")
        janela.destroy()


def mover_canvas(block_size):
    """
    Depois de atualizar player["x"], player["y"], 
    reposiciona o retângulo do personagem no Canvas.
    """
    x = player["x"] * block_size
    y = player["y"] * block_size
    canvas.coords(personagem, x, y, x + block_size, y + block_size)


def desenhar_grade(block_size):
    """
    Desenha toda a grade: fundo branco + linhas cinza + paredes + objetivo.
    """
    # 1) Grade (linhas horizontais e verticais) — optei por desenhar cada célula branca
    for y in range(ALTURA):
        for x in range(LARGURA):
            canvas.create_rectangle(
                x * block_size,
                y * block_size,
                (x + 1) * block_size,
                (y + 1) * block_size,
                outline="gray",
                fill="white"
            )

    # 2) Paredes (fundo cinza escuro, contorno preto)
    for px, py in paredes:
        canvas.create_rectangle(
            px * block_size, py * block_size,
            (px + 1) * block_size, (py + 1) * block_size,
            fill="#4B4B4B", outline="black"
        )

    # 3) Objetivo (fundo verde)
    ox, oy = objetivo
    canvas.create_rectangle(
        ox * block_size, oy * block_size,
        (ox + 1) * block_size, (oy + 1) * block_size,
        fill="green", outline="black"
    )


def on_keypress(event, block_size):
    """
    Ao apertar tecla, chamamos walk() para W/A/S/D.
    """
    tecla = event.keysym.lower()
    if tecla in ("w", "a", "s", "d"):
        walk(tecla, block_size)


def mover_inimigo(block_size):
    """
    Inimigo persegue o jogador. A cada 200 ms, recalcula o próximo passo.
    Evita atravessar paredes em diagonal.
    """
    dx = dy = 0
    dist_x = abs(inimigo["x"] - player["x"])
    dist_y = abs(inimigo["y"] - player["y"])

    # 1) Decide prioridade de movimento (maior distância de coord)
    if dist_x > dist_y:
        direcoes_preferidas = [
            (1 if inimigo["x"] < player["x"] else -1, 0),
            (0, 1 if inimigo["y"] < player["y"] else -1),
        ]
    else:
        direcoes_preferidas = [
            (0, 1 if inimigo["y"] < player["y"] else -1),
            (1 if inimigo["x"] < player["x"] else -1, 0),
        ]

    # 2) Adiciona diagonal e sentido oposto como último recurso
    direcoes_preferidas += [
        (1 if inimigo["x"] < player["x"] else -1, 1 if inimigo["y"] < player["y"] else -1),
        (-direcoes_preferidas[0][0], 0),
        (0, -direcoes_preferidas[1][1])
    ]

    # 3) Tenta cada direção até achar uma válida
    for dx, dy in direcoes_preferidas:
        novo_x = inimigo["x"] + dx
        novo_y = inimigo["y"] + dy

        if (0 <= novo_x < LARGURA and 0 <= novo_y < ALTURA and (novo_x, novo_y) not in paredes):
            # Impede atravessar diagonal sobre parede
            if dx != 0 and dy != 0:
                if ((inimigo["x"] + dx, inimigo["y"]) in paredes or
                    (inimigo["x"], inimigo["y"] + dy) in paredes):
                    continue

            # Movimento permitido: aplica no canvas
            inimigo["x"] = novo_x
            inimigo["y"] = novo_y
            canvas.coords(
                inimigo_sprite,
                inimigo["x"] * block_size, inimigo["y"] * block_size,
                (inimigo["x"] + 1) * block_size, (inimigo["y"] + 1) * block_size
            )
            break

    verificar_colisao()
    # 4) Chama de novo após 200 ms
    janela.after(200, lambda: mover_inimigo(block_size))


def verificar_colisao():
    if player["x"] == inimigo["x"] and player["y"] == inimigo["y"]:
        messagebox.showerror("Game Over", "Você foi pego pelo inimigo!")
        janela.destroy()


# --------------------------------------
#           Início do programa
# --------------------------------------

janela = tk.Tk()
janela.title("PlayMove")

# 1) Coloca a janela em modo fullscreen (sem bordas)
janela.attributes("-fullscreen", True)

#   (Opcional) Apertar ESC para sair do fullscreen
def sair_fullscreen(event=None):
    janela.attributes("-fullscreen", False)

janela.bind("<Escape>", sair_fullscreen)

# 2) Descobre a resolução real da tela (largura × altura)
screen_w = janela.winfo_screenwidth()
screen_h = janela.winfo_screenheight()

# 3) Calcula block_size para caber 43×25 blocos na tela inteira
block_size = min(screen_w // LARGURA, screen_h // ALTURA)

# 4) Determina o tamanho exato do Canvas (será block_size × LARGURA, block_size × ALTURA)
canvas_w = block_size * LARGURA
canvas_h = block_size * ALTURA

# 5) Cria um Canvas menor que a tela, mas que cabe tudo
canvas = tk.Canvas(janela, width=canvas_w, height=canvas_h, bg="white")
#    Centraliza o Canvas dentro da janela fullscreen
canvas.place(x=(screen_w - canvas_w)//2, y=(screen_h - canvas_h)//2)

# 6) Desenha grade, paredes e objetivo usando o block_size calculado
desenhar_grade(block_size)

# 7) Cria o "personagem" e o "inimigo" já nos lugares iniciais
personagem = canvas.create_rectangle(
    player["x"] * block_size, player["y"] * block_size,
    (player["x"] + 1) * block_size, (player["y"] + 1) * block_size,
    fill="blue"
)

inimigo_sprite = canvas.create_rectangle(
    inimigo["x"] * block_size, inimigo["y"] * block_size,
    (inimigo["x"] + 1) * block_size, (inimigo["y"] + 1) * block_size,
    fill="red"
)

# 8) Bind de teclado (chama on_keypress passando block_size)
janela.bind("<Key>", lambda ev: on_keypress(ev, block_size))

# 9) Funções para mostrar a MessageBox de boas-vindas e iniciar o inimigo
def iniciar_jogo():
    mover_inimigo(block_size)

def mostrar_boas_vindas():
    messagebox.showinfo("Bem-vindo!", "Pressione OK para iniciar o jogo.")
    janela.focus_force()
    iniciar_jogo()

# Aguarda ~100 ms para a janela aparecer antes de mostrar o popup
janela.after(100, mostrar_boas_vindas)

# 10) Inicia o loop principal
janela.mainloop()