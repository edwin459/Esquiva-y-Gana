import pygame
import sys
import random
from pygame.locals import *

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Esquiva y Gana')

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Reloj para controlar la velocidad de actualización
clock = pygame.time.Clock()

# Variables del juego
player_pos = [200, 540]  # posición inicial del jugador
obstacles = []  # lista para almacenar los obstáculos
obstacle_speed = 5  # velocidad de movimiento de los obstáculos
score = 0  # puntaje inicial

# Generar imágenes por defecto usando Pygame
player_img = pygame.Surface((50, 50), pygame.SRCALPHA)
pygame.draw.rect(player_img, RED, (0, 0, 50, 50))

obstacle_img = pygame.Surface((30, 30), pygame.SRCALPHA)
pygame.draw.circle(obstacle_img, BLUE, (15, 15), 15)

explosion_img = pygame.Surface((50, 50), pygame.SRCALPHA)
pygame.draw.circle(explosion_img, YELLOW, (25, 25), 25)


# Función para crear obstáculos
def create_obstacle(obstacles, screen_width):
    x = random.randint(0, screen_width - 30)
    y = -30
    obstacles.append([x, y])


# Función para mover y eliminar obstáculos
def update_obstacles(obstacles, speed):
    for obstacle in obstacles:
        obstacle[1] += speed
    obstacles[:] = [obstacle for obstacle in obstacles if obstacle[1] < SCREEN_HEIGHT]


# Función para dibujar los obstáculos en pantalla
def draw_obstacles(screen, obstacles):
    for obstacle in obstacles:
        screen.blit(obstacle_img, obstacle)


# Función para verificar colisiones entre el jugador y los obstáculos
def collision_check(player_pos, obstacles):
    player_rect = pygame.Rect(player_pos[0], player_pos[1], 50, 50)
    for obstacle in obstacles:
        obstacle_rect = pygame.Rect(obstacle[0], obstacle[1], 30, 30)
        if player_rect.colliderect(obstacle_rect):
            return True
    return False


# Función para mostrar el menú principal
def show_menu():
    menu_font = pygame.font.Font(None, 36)
    start_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 250, 200, 50)
    exit_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 310, 200, 50)

    while True:
        screen.fill(WHITE)

        # Mostrar título del juego
        title_text = menu_font.render('Esquiva y Gana', True, RED)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - 120, 50))

        # Mostrar opciones del menú con efectos de hover
        start_color = BLUE
        exit_color = BLUE

        # Detectar interacción del mouse con los botones
        mouse_pos = pygame.mouse.get_pos()
        if start_button_rect.collidepoint(mouse_pos):
            start_color = YELLOW
            if pygame.mouse.get_pressed()[0]:  # Click en "Jugar"
                return True
        if exit_button_rect.collidepoint(mouse_pos):
            exit_color = YELLOW
            if pygame.mouse.get_pressed()[0]:  # Click en "Salir"
                pygame.quit()
                sys.exit()

        # Dibujar botones del menú
        pygame.draw.rect(screen, start_color, start_button_rect)
        pygame.draw.rect(screen, exit_color, exit_button_rect)

        # Texto de los botones
        start_text = menu_font.render('Jugar', True, WHITE)
        exit_text = menu_font.render('Salir', True, WHITE)
        screen.blit(start_text, (SCREEN_WIDTH // 2 - 40, 260))
        screen.blit(exit_text, (SCREEN_WIDTH // 2 - 30, 320))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


# Función principal del juego
def main():
    global player_pos, obstacles, score

    while True:
        if not show_menu():  # Mostrar el menú principal
            pygame.quit()
            return

        # Reiniciar variables del juego
        player_pos = [200, 540]
        obstacles = []
        score = 0

        game_over = False

        while not game_over:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            if keys[K_LEFT] and player_pos[0] > 0:
                player_pos[0] -= 5
            if keys[K_RIGHT] and player_pos[0] < SCREEN_WIDTH - 50:
                player_pos[0] += 5

            screen.fill(WHITE)

            # Generar y mover obstáculos
            if random.randint(1, 100) < 10:
                create_obstacle(obstacles, SCREEN_WIDTH)

            update_obstacles(obstacles, obstacle_speed)

            # Dibujar jugador
            screen.blit(player_img, player_pos)

            # Dibujar obstáculos
            draw_obstacles(screen, obstacles)

            # Detectar colisiones
            if collision_check(player_pos, obstacles):
                game_over = True
                screen.blit(explosion_img, player_pos)
                pygame.display.update()
                pygame.time.wait(500)  # Espera corta para mostrar la explosión

            # Mostrar puntaje
            score += len(obstacles)  # Incrementar puntaje según cantidad de obstáculos esquivados
            font = pygame.font.Font(None, 36)
            score_text = font.render(f'Puntaje: {score}', True, BLUE)
            screen.blit(score_text, (10, 10))

            pygame.display.update()
            clock.tick(30)

        # Mostrar pantalla de Game Over
        font = pygame.font.Font(None, 72)
        game_over_text = font.render('GAME OVER', True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 160, SCREEN_HEIGHT // 2 - 50))
        pygame.display.update()
        pygame.time.wait(2000)  # Espera 2 segundos antes de cerrar el juego


if __name__ == '__main__':
    main()