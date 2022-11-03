# yh9vhg

"""
This game is a vertical shooting game, in which the player controls a jet and tries to destroy enemies.

Required features:
User Input: keyboard inputs
Graphics/Images: the images of the characters will be in a jet (player) and missiles (enemies)
Start screen: Game has a start screen with game name, student name (and ID), and instructions.
Small enough window: The game window is gamebox.Camera(400, 600)

Optional Features:
Enemies: characters that move around the screen toward the player’s jet
Collectibles: heart items that the user may collect to restore health
Timer: counts how long the user survives
Health bar: across the top of the screen that decreases every time the user comes in contact with
            the enemies
"""

import gamebox
import pygame
from random import randint

"""
main page when users open the game
"""
start_text = [
    gamebox.from_text(200, 200, "Phoenix Retro", 79, "Gold", bold=False),
    gamebox.from_text(200, 280, "Control your jet with arrow keys.", 27, "White", bold=False),
    gamebox.from_text(200, 310, "Press space bar to shoot enemies", 27, "White", bold=False),
    gamebox.from_text(200, 340, "Pick up the heart objects to restore health!", 27, "white", bold=False),
    gamebox.from_text(200, 370, "Press space bar to begin!", 27, "Red", bold=False),
    gamebox.from_text(100, 570, "Yiwei He, yh9vhg", 25, "Grey", bold=False),
]

start = False
screen = gamebox.Camera(400, 600)

# basic settings
bullets = []
enemies = []
explosions = []
hearts = []
counter = 0
ticks = 0
score = 0
enemy_speed = 8

player = gamebox.from_image(screen.x, screen.y + 250, "jet.png")
player_speed = 7
player.scale_by(0.1)

background = gamebox.from_image(screen.x, screen.y, "moon.png")
background.size = [400, 600]

p_health = gamebox.from_color(200, 20, "Red", 380, 15)
p_health_width = 380

""" 
main game function including scoring, collectible(heart), keyboard input, 
health bar, background change, timer, enemy speed, player speed, health reduction, score count
"""
def game(keys):
    global start, score, background, p_health_width, ticks, counter, player_speed, enemy_speed, player, p_health

    if not start:
        for text in start_text:
            screen.draw(text)
        if pygame.K_SPACE in keys:
            start = True
            start_text.clear()
    else:
        if (score//20) % 2 == 0:
            background = gamebox.from_image(screen.x, screen.y, "moon.png")
        if (score//20) % 2 == 1:
            background = gamebox.from_image(screen.x, screen.y, "galaxy.png")
        screen.draw(background)
        screen.draw(gamebox.from_text(200, 50, str(score), 60, "white", bold=True))

        if not p_health.width <= 0:
            ticks += 1
        seconds = str(int((ticks / ticks_per_sec))).zfill(3)

        timer = gamebox.from_text(75, 50, "Alive for: " + str(seconds) +(" sec"), 25, "white", bold=False)
        screen.draw(timer)

        if pygame.K_LEFT in keys:
            player.x -= player_speed
        if pygame.K_RIGHT in keys:
            player.x += player_speed
        if pygame.K_UP in keys:
            player.y -= player_speed
        if pygame.K_DOWN in keys:
            player.y += player_speed

        if player.x >= 400:
            player.x = 0
        elif player.x <= 0:
            player.x = 400
        if player.y >= 600:
            player.y = 600
        elif player.y <= 0:
            player.y = 0

        counter += 1

        if pygame.K_SPACE in keys:
            if counter % 4 == 0:
                bullets.append(gamebox.from_color(player.x + 1, player.y, "Green", 5, 10))

        for bullet in bullets:
            bullet.y -= 50
            if bullet.y <= 0:
                bullets.pop(0)
            screen.draw(bullet)

# floating objects
        if counter % randint(35, 50) == 0 and start:
            new_missile = gamebox.from_image(randint(20, 380), 0, "missile.png")
            new_missile.scale_by(0.1)
            enemies.append(new_missile)

        for missile in enemies:
            missile.y += enemy_speed
            screen.draw(missile)

        if counter % randint(150, 250) == 0 and start:
            new_heart = gamebox.from_image(randint(20, 380), 0, "heart.png")
            new_heart.scale_by(0.04)
            hearts.append(new_heart)

        for heart in hearts:
            heart.y += 9
            screen.draw(heart)

        for missile in enemies:
            for bullet in bullets:
                if missile.touches(bullet):
                    if len(enemies) >= 1:
                        enemies.pop(enemies.index(missile))
                    bullets.pop(bullets.index(bullet))
                    explosion = gamebox.from_image(missile.x, missile.y, "explosion.png")
                    explosion.scale_by(0.1)
                    explosions.append(explosion)
                    score += 1
                    if score % 4 == 0:
                        enemy_speed += 0.2
            if missile.touches(player):
                if not len(enemies) == 0:
                    enemies.pop(enemies.index(missile))
                p_health_width -= 76
                p_health.size = [p_health_width, 15]
                p_health.x -= 38
            if missile.y >= 600:
                enemies.pop(enemies.index(missile))
                p_health_width -= 38
                p_health.size = [p_health_width, 15]
                p_health.x -= 19

        for heart in hearts:
            if player.touches(heart) and not p_health_width == 380:
                hearts.pop(hearts.index(heart))
                p_health_width += 38
                p_health.size = [p_health_width, 15]
                p_health.x += 19
            if heart.y >= 600:
                hearts.pop(hearts.index(heart))

        if p_health.width <= 0:
            score = 0
            start = False
            if pygame.K_SPACE in keys:
                score = 0
                p_health_width = 380
            bullets.clear()
            enemies.clear()
            hearts.clear()
            screen.draw(gamebox.from_text(screen.x, screen.y, "GAME OVER", 80, "Red", bold=True))
            screen.draw(gamebox.from_text(screen.x, screen.y + 70, "You survived " + str(seconds) + " seconds", 30, "Red", bold=True))

        for explosion in explosions:
            screen.draw(explosion)
            if counter % 20 == 0:
                explosions.clear()

        screen.draw(player)
        screen.draw(p_health)
        screen.draw(gamebox.from_text(370, 40, str(int((p_health_width / 380) * 100)), 30, "Red", bold=False))

    screen.display()

ticks_per_sec = 30
gamebox.timer_loop(ticks_per_sec, game)