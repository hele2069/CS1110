
camera = gamebox.Camera(400, 600)

p_health = gamebox.from_color(200, 20, "Red", 380, 15)

sand = gamebox.from_image(camera.x, camera.y, "sand.png")
sand.size = [400, 600]

player = gamebox.from_image(camera.x, camera.y + 200, "jet.png")
player.scale_by(0.2)

bullets = []
tanks = []
explosions = []
hearts = []

counter = 0
p_health_width = 380
game_on = False
p_speed = 6.5
ticks = 0
score = 0
enemy_speed = 4

start_text = [
    gamebox.from_text(200, 100, "ATARI 2.0", 80, "Light Blue", bold=False),
    gamebox.from_text(100, 150, "Instructions: ", 30, "White", bold=False),
    gamebox.from_text(200, 180, "Control your player with the arrow keys.", 30, "White", bold=False),
    gamebox.from_text(200, 210, "Press the space bar to shoot enemies", 30, "White", bold=False),
    gamebox.from_text(200, 240, "Last as long as you can!", 30, "white", bold=False),
    gamebox.from_text(200, 270, "Press the space bar now to begin!", 30, "Green", bold=False),
    gamebox.from_text(110, 550, "Connor Noble, cpn8ftn", 25, "Grey", bold=False),
    gamebox.from_text(90, 580, "Yingyi Zhu, yz7un", 25, "Grey", bold=False)

]


def tick(keys):
    global counter, p_health_width, game_on, p_speed, score, ticks, enemy_speed,sand

    if not game_on:
        for text in start_text:
            camera.draw(text)
        if pygame.K_SPACE in keys:
            game_on = True
            start_text.clear()
    else:
        if (score//20)%2==1:
            sand=gamebox.from_image(camera.x, camera.y, "space.png")
        camera.draw(sand)
        if (score//20)%2==0:
            sand=gamebox.from_image(camera.x, camera.y, "sand.png")

        camera.draw(gamebox.from_text(200, 50, str(score), 60, "black", bold=True))

        if not p_health.width <= 0:
            ticks += 1
        seconds = str(int((ticks / ticks_per_second))).zfill(3)

        timer = gamebox.from_text(70, 50, "Alive for: " + str(seconds) +(" sec"), 25, "Black", bold=False)
        camera.draw(timer)

        if pygame.K_LEFT in keys:
            player.x -= p_speed
        if pygame.K_RIGHT in keys:
            player.x += p_speed
        if pygame.K_UP in keys:
            player.y -= p_speed
        if pygame.K_DOWN in keys:
            player.y += p_speed

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
                bullets.append(gamebox.from_color(player.x + 1, player.y, "black", 5, 10))

        for bullet in bullets:
            bullet.y -= 5
            if bullet.y <= 0:
                bullets.pop(0)
            camera.draw(bullet)

        if counter % randint(35, 50) == 0 and game_on:
            new_tank = gamebox.from_image(randint(20, 380), 0, "tank.png")
            new_tank.scale_by(0.035)
            tanks.append(new_tank)

        for tank in tanks:
            tank.y += enemy_speed
            camera.draw(tank)

        if counter % randint(150, 250) == 0 and game_on:
            new_heart = gamebox.from_image(randint(20, 380), 0, "heart.png")
            new_heart.scale_by(0.2)
            hearts.append(new_heart)

        for heart in hearts:
            heart.y += 3
            camera.draw(heart)

        for tank in tanks:
            for bullet in bullets:
                if tank.touches(bullet):
                    if len(tanks) >= 1:
                        tanks.pop(tanks.index(tank))
                    bullets.pop(bullets.index(bullet))
                    explosion = gamebox.from_image(tank.x, tank.y, "explosion.png")
                    explosion.scale_by(0.1)
                    explosions.append(explosion)
                    score += 1
                    if score % 4 == 0:
                        enemy_speed += 0.2
            if tank.touches(player):
                if not len(tanks) == 0:
                    tanks.pop(tanks.index(tank))
                p_health_width -= 76
                p_health.size = [p_health_width, 15]
                p_health.x -= 38
            if tank.y >= 600:
                tanks.pop(tanks.index(tank))
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
            game_on = False
            if pygame.K_SPACE in keys:
                score = 0
                p_health_width = 380


            tanks.clear()
            hearts.clear()
            bullets.clear()
            camera.draw(gamebox.from_text(camera.x, camera.y, "GAME OVER", 80, "Red", bold=True))
            camera.draw(
                gamebox.from_text(camera.x, camera.y + 70, "You survived " + str(seconds) + " seconds.", 30, "Red",
                                  bold=False))

        for explosion in explosions:
            camera.draw(explosion)
            if counter % 20 == 0:
                explosions.clear()

        camera.draw(player)
        camera.draw(p_health)

        camera.draw(gamebox.from_text(370, 40, str(int((p_health_width / 380) * 100)), 30, "Red", bold=False))

    camera.display()


ticks_per_second = 30

gamebox.timer_loop(ticks_per_second, tick)