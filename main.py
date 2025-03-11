import pygame
import sys
import math

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Point Shape at Mouse")

# setup images sprite and resize them
cat = pygame.image.load("cat.png")
cat_size = cat.get_size()
size = (cat_size[0] // 2, cat_size[1] // 2)
cat = pygame.transform.scale(cat, size)
cat_size = (size[0] - 40, size[1] - 40)

cat2 = pygame.image.load("cat_game_over.png")
cat2_size = cat2.get_size()
size = (cat2_size[0] // 2, cat2_size[1] // 2)
cat2 = pygame.transform.scale(cat2, size)
cat2_size = (size[0] - 40, size[1] - 40)

grass = pygame.image.load("grass.png")
grass_size = grass.get_size()
size = (grass_size[0] // 2, grass_size[1] // 2)
grass = pygame.transform.scale(grass, size)

spike = pygame.image.load("spike.png")
spike_size = spike.get_size()
size = (spike_size[0] // 2, spike_size[1] // 2)
spike = pygame.transform.scale(spike, size)

end = pygame.image.load("end.png")
end_size = end.get_size()
size = (end_size[0] // 2, end_size[1] // 2)
end = pygame.transform.scale(end, size)

# load sounds
jump_sound = pygame.mixer.Sound('Jump.wav')

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY = (0, 200, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# set up fonts
font1 = pygame.font.Font(None, 100)
font2 = pygame.font.Font(None, 50)


# title and menu
title = font1.render("Tower Hopper", True, GREEN)
start_txt = font2.render("Play", True, BLUE)
start_rect = pygame.Rect(
    50, 200, start_txt.get_size()[0], start_txt.get_size()[1]
)


def exit():
    pygame.quit()
    sys.exit()


show_hitboxes = False
highlight = False
game_scene = "title"
end_level = False
invincible = False

# title screen
while game_scene == "title":
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("process exited")
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_rect.collidepoint(mouse_pos):
                game_scene = "game"

        if start_rect.collidepoint(mouse_pos):
            highlight = True

        else:
            highlight = False

    screen.fill(SKY)
    if highlight:
        pygame.draw.rect(screen, (0, 230, 255), start_rect)

    screen.blit(title, (10, 10))
    screen.blit(start_txt, (50, 200))
    screen.blit(grass, (372.5, 370))
    screen.blit(cat, (365, 300))
    pygame.display.flip()

# main game
while True:
    level_y = 0
    player_x, player_y = 382, 200
    player_hitbox = pygame.Rect(
        player_x + 25, (player_y + level_y) + 30, cat_size[0], cat_size[1]
    )
    spikes = []
    touching_spike = False

    def save_game(file_path, line, data):
        with open(file_path, "r") as file:
            lines = file.readlines()
        if 0 <= line < len(lines):
            lines[line] = str(data) + "\n"
        with open(file_path, "w") as file:
            file.writelines(lines)

    def load_game():
        global level_num
        with open("save_data.txt", "r") as file:
            lines = file.readlines()
        level_num = int(lines[0])

    def find_level(file_path, level_num):
        with open(file_path, "r") as file:
            for index, line in enumerate(file):
                if str(level_num) in line:
                    return index
        return -1

    def scan_level(file_path, level_index, level_num):
        global level, spikes
        level = []
        spikes = []
        index = 0
        with open(file_path, "r") as file:
            for line in file:
                if line.strip() == "#" and index >= level_index:
                    return level[level_index:]
                if not line.strip() == str(level_num):
                    level.append(line.strip())
                index += 1
            return level[level_index:]

    def draw_line(line_num, x, y):
        global level, spikes, touching_spike, end_level
        index = 0
        line = list(level[line_num])
        for i in range(len(line)):
            screen.blit(grass, (x, y))
            if line[index] == "B" and y <= 700:
                screen.blit(grass, (x, y))
                x += 53
            elif line[index] == "S" and y <= 700:
                screen.blit(spike, (x, y))
                spike_rect = pygame.Rect(x, y, 60.5, 60.5)
                if show_hitboxes:
                    pygame.draw.rect(screen, (255, 0, 0), spike_rect, 2)
                if spike_rect.colliderect(player_hitbox):
                    touching_spike = True
                x += 53
            elif line[index] == "E" and y <= 700:
                screen.blit(end, (x + 2, y + 3))
                end_rect = pygame.Rect(x, y, 60.5, 60.5)
                if show_hitboxes:
                    pygame.draw.rect(screen, (0, 255, 0), end_rect, 2)
                if end_rect.colliderect(player_hitbox):
                    end_level = True
                x += 53
            index += 1

    def load_level(level_num):
        global level_index, level
        level_index = find_level("levels.txt", level_num)
        level = scan_level("levels.txt", level_index, level_num)

    def draw_level(x, y):
        global level_y, level_num
        line = 0
        for i in range(len(level)):
            draw_line(line, x, y)
            line += 1
            y += 53

    def game_over():
        if not invincible:
            global RED, game_scene, level_num, level_y, player_x, player_y, player_hitbox, touching_spike
            game_scene = "game over"
            screen.fill(SKY)
            game_over = font1.render("Game Over", True, RED)
            draw_level(125, 270 + level_y)
            screen.blit(cat2, (player_x, player_y + level_y))
            screen.blit(game_over, (212, 200))
            pygame.display.flip()
            level_y = 0
            player_x, player_y = 382, 200
            player_hitbox = pygame.Rect(
                player_x + 25,
                (player_y + level_y) + 30,
                cat_size[0],
                cat_size[1],
            )
            spikes = []
            touching_spike = False
            score = 0
            pygame.time.delay(2000)
            game_scene = "game"

    def next_level(level):
        global stars, level_num, level_y, player_x, player_y, font1, game_scene, end_level, invincible
        game_scene = "complete"
        screen.fill(SKY)
        complete_txt = font1.render("Level Complete!", True, (0, 255, 0))
        draw_level(125, 270 + level_y)
        screen.blit(cat, (player_x, player_y + level_y))
        size = complete_txt.get_size()
        screen.blit(complete_txt, (400 - (size[0] / 2), -600))
        pygame.display.flip()
        if level_num <= 2:
            level_num += 1
        else:
            level_num = 1
        load_level(level_num)
        level_y = 0
        player_y += 26.6
        player_hitbox = pygame.Rect(
            player_x + 25, (player_y + level_y) + 30, cat_size[0], cat_size[1]
        )
        player_x, player_y = 382, 200
        player_hitbox = pygame.Rect(
            player_x + 25, (player_y + level_y) + 30, cat_size[0], cat_size[1]
        )
        spikes = []
        touching_spike = False
        end_level = False
        invincible = True
        score = 0
        level = []
        load_level(level_num)
        save_game("save_data.txt", 0, level_num)
        pygame.time.delay(2000)
        pygame.display.update()
        game_scene = "game"

    level_num = 1
    load_game()
    score = 0
    stars = 0
    load_level(int(level_num))
    screen.fill(SKY)
    while game_scene == "game":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            # controls
            keys = pygame.key.get_pressed()
            if event.type == pygame.KEYDOWN:
                if keys[pygame.K_s]:
                    player_y += 53
                    score += 1
                    jump_sound.play()

                if keys[pygame.K_a]:
                    player_x -= 53

                if keys[pygame.K_d]:
                    player_x += 53

        # move the level up if the player reaches the bottom of the screen
        if player_y + level_y >= 500:
            level_y -= 53

        # draw the level and update the player's hitbox
        screen.fill(SKY)
        draw_level(125, 270 + level_y)
        player_hitbox = pygame.Rect(
            player_x + 20, (player_y + level_y) + 30, cat_size[0], cat_size[1]
        )

        if touching_spike and not end_level and not invincible:
            game_over()

        # draw the player
        screen.blit(cat, (player_x, player_y + level_y))

        if show_hitboxes:
            pygame.draw.rect(screen, (0, 0, 255), player_hitbox, 2)

        # check if the player has reached the goal
        if end_level:
            next_level(level_num)
            while player_y + level_y >= 500:
                invincible = True

        # check if the player has reached the top of the screen
        if player_y + level_y <= 0 and not invincible:
            game_over()

        # move the level
        level_y -= 1

        pygame.display.flip()
