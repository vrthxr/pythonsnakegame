import tkinter as tk
from tkinter import *
from tkinter.font import Font
import random


# Variáveis não modificáveis do jogo, como altura, coloração e velocidade.
GAME_WIDTH = 1200
GAME_HEIGHT = 800
SPEED = 50
SPACE_SIZE = 50
BODY_PARTS = 4
SNAKE_COLOR = "#5A5A5A"
FOOD_COLOR = "white"
BACKGROUND_COLOR = "#000000"


# Classes


class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake"
            )
            self.squares.append(square)


# A classe de comida foi feita com uma divisão do tamanho do jogo/pelo espaço em jogo (Vendo como um board de xadrez, 500/50 me causa 10 espaços possíveis para aparecer a comida).
class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(
            x,
            y,
            x + SPACE_SIZE,
            y + SPACE_SIZE,
            fill=FOOD_COLOR,
            tag="food",
        )


def next_turn(snake, food):
    # Adicionar pedaço de corpo à cobra
    x, y = snake.coordinates[0]
    if direction == "up":
        y -= SPACE_SIZE

    elif direction == "down":
        y += SPACE_SIZE

    elif direction == "left":
        x -= SPACE_SIZE

    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(
        x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR
    )

    snake.squares.insert(0, square)
    # Adicionar pontuação e remover fruta ao comer
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score

        score += 1

        label.config(text="Score:{}".format(score))

        canvas.delete("food")

        food = Food()

    else:
        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

    if check_colissions(snake):
        game_over()

    else:
        window.after(SPEED, next_turn, snake, food)


# Parte para a cobra não fazer um 180 graus, não deixando ir direita/esquerda e cima/baixo diretamente
def change_direction(new_direction):
    global direction

    if new_direction == "left":
        if direction != "right":
            direction = new_direction

    elif new_direction == "right":
        if direction != "left":
            direction = new_direction

    elif new_direction == "up":
        if direction != "down":
            direction = new_direction

    elif new_direction == "down":
        if direction != "up":
            direction = new_direction


# Colisão com a parede ou com ela própria = Game Over
def check_colissions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True

    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True


def game_over():
    canvas.delete(ALL)
    canvas.create_text(
        canvas.winfo_width() / 2,
        canvas.winfo_height() / 2,
        font=("Retro Gaming", 40),
        text="FIM DE JOGO",
        fill="#5A5A5A",
        tag="gameover",
    )


# Botão de reiniciar o jogo adicionado na janela
def restart_game():
    global snake, food, score, direction
    # Resetar o jogo aos seus valores iniciais sem precisar abrir o programa novamente
    canvas.delete(ALL)
    snake = Snake()
    food = Food()
    score = 0
    direction = "down"
    label.config(text="Pontuação: {}".format(score))
    next_turn(snake, food)


# Janela do jogo
window = Tk()
window.title("Snake Game Python")
window.resizable(False, False)
restart_button = Button(
    window, text="Reiniciar", command=restart_game, font=("Retro gaming", 25)
)
restart_button.place(x=0, y=0)

score = 0
direction = "down"

label = Label(window, text="Pontuação: {}".format(score), font=("Retro Gaming", 40))
label.pack()

# Criação do Mapa
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()


# Centralização da janela no centro da tela
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Controles

window.bind("<Left>", lambda event: change_direction("left"))
window.bind("<Right>", lambda event: change_direction("right"))
window.bind("<Up>", lambda event: change_direction("up"))
window.bind("<Down>", lambda event: change_direction("down"))


# Criação da Cobra e da Comida

snake = Snake()
food = Food()

next_turn(snake, food)


window.mainloop()
