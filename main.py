import pygame, math, random, time
from pygame.locals import *

pygame.init()

bg = (10, 0, 60)
black = (5, 0, 30)

bg_menu = (10, 0, 50)
ctext = (220, 220, 220)
ctextbg = (0, 80, 150)

ww = 800
wh = 600

window = pygame.display.set_mode((ww, wh))
pygame.display.set_caption("Don't hit the asteroids!!!")

pygame.mouse.set_visible(0)
window.fill(bg)

fps = 60

difficulty = 2 # 0 = Hard, 1 = Normal, 2 = Easy урровень сложности при запуске в меню
diff_bgs = ((200, 0, 0), (180, 180, 0), (0, 200, 0)) # цвет текста для сложности
diff_str = ("Hard", "Normal", "Easy")
diff_spawn = (1 * fps, 1.5 * fps, 2 * fps) # секунды * частота кадров = кадры

# текстовые шрифты
text_title = pygame.font.SysFont(None, 125)
text_subt = pygame.font.SysFont(None, 75)
text_subt2 = pygame.font.SysFont(None, 25)

player_img = pygame.image.load("player_1.png")

#Игрок в стартовом положении
player_x = ww / 2
player_y = wh / 2

player = pygame.Rect(player_x, player_y, player_img.get_rect().width, player_img.get_rect().height)
player_radius = player.width / 2
p_pos = [player.left, player.top] # Я использую его для более точного (диагонального) перемещения игрока

pygame.mixer.music.load("noise.mp3")


# импорт игровых изображений
asteroid_6 = pygame.image.load("asteroid_6.png")
asteroid_5 = pygame.image.load("asteroid_5.png")
asteroid_4 = pygame.image.load("asteroid_4.png")
asteroid_1 = pygame.image.load("asteroid_1.png")
asteroid_2 = pygame.image.load("asteroid_2.png")
asteroid_3 = pygame.image.load("asteroid_3.png")

asteroid_radius = asteroid_1.get_rect().width / 2
w_aster = asteroid_radius * 2
h_aster = w_aster

explosion = pygame.image.load("explosion.png")

# Тексты главного меню
title = text_title.render("@LIEN", True, ctext)

subt1 = text_subt.render("Press [Space] to start.", True, ctext, ctextbg)
subt2 = text_subt.render("Press [Esc] to exit game.", True, ctext, ctextbg)

subt4 = text_subt2.render("Use arrow keys to change.", True, ctext)
subt5 = text_subt.render("Difficulty:", True, ctext)
subt6 = text_subt2.render("Press [F1] and [F2] to change Fullscreen", True, ctext)


game = 1
while game == 1:

    #Настройка астероидов

    bilder_asteroids = [asteroid_1, asteroid_2, asteroid_3, asteroid_4, asteroid_5, asteroid_6]
    asteroids = []
    angle_asteroids = []

    time_counter = 0 #измеряет время, необходимое для появления нового астероида

    angle_player = 0
    pr_player = False

    player_rot = 0
    turnrate = 300 / fps

    mvsp = 210 / fps
    mvsp_asteroids = 240 / fps #Скорость перемещения (пиксель на кадр)

    health = 1

    clock = pygame.time.Clock()
    time_count = 0  # измерение времени во время игры

    x = 1
    x2 = 1
    end = 0

    # Main Menu
    while x2 == 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                x = 0
                x2 = 0
                game = 0

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    x = 0
                    x2 = 0
                    game = 0

 #клавиши для изменения экрана, начало, выхода
                if event.key == K_F1:
                    window = pygame.display.set_mode((ww, wh), FULLSCREEN)
                if event.key == K_F2:
                    window = pygame.display.set_mode((ww, wh))

                if event.key == K_SPACE:
                    x2 = 0

                if event.key == K_DOWN:
                    difficulty += (difficulty < 2)

                if event.key == K_UP:
                    difficulty -= (difficulty > 0)

        diff_bg = diff_bgs[difficulty]
        diff_text = diff_str[difficulty]
        spawn_count = diff_spawn[difficulty]

        window.fill(bg_menu)
        window.blit(title, (100, 50))

        mvsp_asteroids = (300 - difficulty * 30) / fps
        health = difficulty + 1

        subt3 = text_subt.render(diff_text, True, ctext, diff_bg)

        window.blit(subt1, (100, 325))
        window.blit(subt2, (100, 400))
        window.blit(subt3, (500, 100))
        window.blit(subt4, (500, 210))
        window.blit(subt5, (500, 10))
        window.blit(subt6, (100, 550))

        pygame.draw.polygon(window, ctext, ((500, 90), (525, 65), (550, 90)))
        pygame.draw.polygon(window, ctext, ((500, 167), (525, 192), (550, 167)))

        pygame.display.update()

    # in-GAME

    while x == 1:
        time_count += 1

        angle_player += player_rot

        # Движение игрока
        if pr_player == True:
            b = math.cos(math.radians(angle_player)) * mvsp # Вычисляет длину катетов
            a = math.sin(math.radians(angle_player)) * mvsp # Вычисляет длину гипоетнузы

            p_pos[1] += b
            p_pos[0] += a

        player.left = p_pos[0]
        player.top = p_pos[1]

        # ввод игрока
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                x = 0

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    x = 0
                if event.key == K_UP or event.key == K_w:
                    pr_player = True

                if event.key == K_LEFT or event.key == K_a:
                    player_rot += turnrate

                if event.key == K_RIGHT or event.key == K_d:
                    player_rot -= turnrate

            if event.type == KEYUP:
                if event.key == K_UP or event.key == K_w:
                    pr_player = False

                if event.key == K_LEFT or event.key == K_a:
                    player_rot -= turnrate

                if event.key == K_RIGHT or event.key == K_d:
                    player_rot += turnrate

        # Движение астероидов
        for i in range(len(asteroids)):

            if asteroids[i].top <= 0 or asteroids[i].bottom >= wh:
                angle_asteroids[i] = 360 - angle_asteroids[i]


            elif asteroids[i].left <= 0 or asteroids[i].right >= ww:
                angle_asteroids[i] = 180 - angle_asteroids[i]

            b = math.cos(math.radians(angle_asteroids[i])) * mvsp_asteroids
            a = math.sin(math.radians(angle_asteroids[i])) * mvsp_asteroids

            asteroids[i].left += b
            asteroids[i].top += a

        window.fill(bg)

        # определяет центр нового повернутого изображения игрока
        player_rect = player_img.get_rect().center
        player_neu = pygame.transform.rotate(player_img, angle_player - 180)
        player_neu.get_rect().center = player_rect

        player_rect = player_img.get_rect()
        player_center_neu = player_neu.get_rect().center
        player_center_diff = (player.center[0] - player_center_neu[0], player.center[1] - player_center_neu[1])

        for i in range(len(asteroids)):
            window.blit(bilder_asteroids[i], asteroids[i])

        window.blit(player_neu, player_center_diff)

        time_counter += 1

        # порождает новый астероид
        if time_counter >= spawn_count:

            edges = ["x", "y"]
            sedge = edges[random.randint(0, 1)]  # рандомно выбирается край (верхний нижний или левый правый край) -> "x" или "y"

            if sedge == "x":
                spawnx = random.randint(0, ww - w_aster)
                edgex = random.randint(0, 1) * (ww - w_aster - 20) + 10 #-20 +10, чтобы переместить астероид на 10 пикселей от края ( +10 ИЛИ (-20+10) = -10)

                asteroids.append(pygame.Rect(spawnx, edgex, w_aster, h_aster))

            if sedge == "y":
                spawny = random.randint(0, wh - h_aster)
                edgey = random.randint(0, 1) * (wh - h_aster - 20) + 10

                asteroids.append(pygame.Rect(spawny, edgey, w_aster, h_aster))

            bilder_asteroids.append(bilder_asteroids[random.randint(0, 2)])
            angle_asteroids.append(random.randint(0, 360))

            time_counter = 0

        # Столкновение (требуется список индексов для удаления элементов списка астероидов)
        del_list = []
        for i, ast in enumerate(asteroids):

            # столкновение с кругом более точно для вращающихся объектов
            dist = ((ast.center[0] - player.center[0]) ** 2 + (ast.center[1] - player.center[1]) ** 2) ** (1 / 2)
            if dist < (player_radius + asteroid_radius):
                health -= 1
                del_list.append(i)

        del_list.reverse()

        for i in del_list:  # удаляет элементы
            del asteroids[i]
            del bilder_asteroids[i]
            del angle_asteroids[i]

        # игрок взрывается
        if health <= 0:
            window.blit(explosion, (
            player.left - explosion.get_rect().width / 2 + 12, player.top - explosion.get_rect().height / 2 + 12))
            pygame.display.update()
            pygame.mixer.music.play()
            time.sleep(1.5)
            x = 0
            end = 1
            p_pos = [ww / 2 - player.width / 2, wh / 2 - player.height / 2]
            player.left, player.top = p_pos

        # переключайте положение игрока при столкновении с краем экрана
        p_pos[0] += (player.left <= 0) * ww - (player.right >= ww) * ww
        p_pos[1] += (player.top <= 0) * wh - (player.bottom >= wh) * wh

        # показ очков здоровья
        txt_hp = text_subt2.render("Shield:          x {}".format(health - 1), True, ctext)

        window.blit(txt_hp, (10, wh - 20))

 #рисую круг для игрока, чтобы потом проходила проверка на урон, коснулся ли враг круга -> -1хп
        pygame.draw.circle(window, (120, 180, 180), (90, wh - 15), 14, 2)

        if health > 1:
            pygame.draw.circle(window, (120, 180, 180), player.center, 20, 3)

        pygame.display.update()
        clock.tick(fps)

    # # Игра окончена экран:
    if end == 1:
        waiting = True
        x = 1

        basicFont = pygame.font.SysFont(None, 100)
        text = basicFont.render("You Died", True, ctext)
        text_time = text_subt.render("survived: " + str(round(time_count / fps, 2)) + " seconds", True, ctext)
        text_Esc = text_subt.render("Press any key to continue.", True, ctext)

        while x == 1:
            window.fill(bg_menu)

            window.blit(text, (50, 100))
            window.blit(text_time, (75, 300))
            window.blit(text_Esc, (75, 500))
            pygame.display.update()

            if waiting == True: # избегайте прямого изменения экрана, чтобы игрок мог видеть свой результат
                time.sleep(1.25)
                waiting = False

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    x = 0

pygame.quit()
