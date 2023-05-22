# Akan Ndem xaa8tq
# Steve Kim cae4qn
#
# Description:
# 	This game will be focused on the survival of a spaceship defending Earth that the user controls.
# 	The spaceship is being attacked by the aliens from outer space.
# 	The spaceship however, only has a certain amount of times it can be hit by the aliens before it is destroyed and it is game over.
# 	The aliens spawn in random locations and move towards the spaceship at different speeds.
# 	The spaceship must shoot at the aliens to survive; if the alien gets past, it will attack earth, causing a loss in points.
#
# Required:
# User input
# Use left and right arrows
# Control movement of spaceship
# Space bar shoots a missile
# Game over
# Displays game over screen when the health bar has completely run out
# Small window
# 800x600 Gamebox.camera(800, 600)
# graphics/images
# Possible space background
# Spaceships or enemies look like asteroids/spaceships
#
# Four optional:
# Timer
# game uses a timer to keep score
# timer keeps track of survival time of the user
# Enemies
# Enemies fall down the screen to the player at random locations and speeds
# Health bar
# Keeps track of how many enemies has hit the user
# Useful for coordinating the game restart
# Sprite animation
# spaceship animation changes as the user input on left and right arrow changes
import random
import pygame
import gamebox
camera = gamebox.Camera(800,600)
health_bar = [
   gamebox.from_color(760,30, 'yellow', 20, 20),
   gamebox.from_color(730,30, 'yellow', 20, 20),
   gamebox.from_color(700,30, 'yellow', 20, 20),
   gamebox.from_color(670,30, 'yellow', 20, 20),
    gamebox.from_color(640,30, 'yellow', 20, 20)
   ]
# url for the spaceship sprite sheet: https://png.pngitem.com/pimgs/s/660-6602144_2d-spaceship-pixel-art-hd-png-download.png
spaceship_images = gamebox.load_sprite_sheet('spaceship sprite sheet.png', 1, 5)
spaceship = gamebox.from_image(400,500,spaceship_images[0])
current_frame = 0
missile_list = []
seconds_since_last_missile = 0
# enemy sprite sheet url: https://www.deviantart.com/joonth/art/NDP-Chaos-sprite-sheet-380298986
enemy_list = []
game_on = False
game_over = False
seconds_since_start = 0
seconds_since_last_enemy_spawned = -3
game_over = 'GAME OVER'
def create_enemies():
    '''
    This function creates the enemies displayed in the main game
    :return: this function returns nothing
    '''
    enemy_spawn_point = random.randint(40,760)
    enemy_images = gamebox.load_sprite_sheet('enemy sprite sheet.png', 4, 10)
    enemy = gamebox.from_image(enemy_spawn_point, 50, enemy_images[11])
    enemy_speed = random.randint(5, 15)
    enemy.speedy = enemy_speed
    enemy_list.append(enemy)
def create_missile():
    '''
    this function creates the missiles fired by the user
    :return: this function returns nothing
    '''
    missile = gamebox.from_color(spaceship.x, spaceship.y - 40, 'red', 10, 10)
    missile_list.append(missile)
    missile_velocity = -8
    missile.yspeed = missile_velocity
    missile.move_speed()
def tick(keys):
    '''
    This function is the main game loop which controls whether the game is on and what the screen is displaying. This
    function controls the movement of the user and the firing of missiles.
    :param keys: user input of keys on the keyboard
    :return: this function returns nothing
    '''
    global seconds_since_start, seconds_since_last_enemy_spawned, game_on, seconds_since_last_missile, game_over


    if pygame.K_s in keys:
        game_on = True


    if game_on:
        seconds_since_start += 1/30
        camera.clear('black')
        # main game background url: https://www.istockphoto.com/photo/earth-in-space-gm186859418-14773161
        background_main_game = gamebox.from_image(400, 300, 'main game background.jpg')
        camera.draw(background_main_game)
        if seconds_since_start - seconds_since_last_enemy_spawned >= 1.75:
            seconds_since_last_enemy_spawned = seconds_since_start
            create_enemies()


        for enemy in enemy_list:
            camera.draw(enemy)

            if enemy.y == 600:
                enemy_list.remove(enemy)
        for enemy in enemy_list:
            enemy.move_speed()

        global current_frame
        spaceship_move = False
        if pygame.K_RIGHT in keys:
            spaceship.x += 18
            spaceship_move = True
        if pygame.K_LEFT in keys:
            spaceship.x -= 18
            spaceship_move = True

        if spaceship_move:
            current_frame += 0.3
            if current_frame >= 3:
                current_frame = 3
            spaceship.image = spaceship_images[int(current_frame)]
        else:
            spaceship.image = spaceship_images[0]


        if pygame.K_SPACE in keys:
            if seconds_since_start - seconds_since_last_missile >= 0.5:
                seconds_since_last_missile = seconds_since_start
                create_missile()

        for missile in missile_list:
            missile.move_speed()
            camera.draw(missile)
        for missile in missile_list:
            for enemy in enemy_list:
                if missile.touches(enemy):
                    enemy_list.remove(enemy)
                if enemy.touches(missile):
                    missile_list.remove(missile)

        camera.draw(gamebox.from_text(610,30,'Health: ', 20, 'yellow'))

        for bar in health_bar:
            camera.draw(bar)

        for health in health_bar:
            for enemy in enemy_list:
                if enemy.touches(spaceship):
                    health_bar.remove(health)
                    enemy_list.remove(enemy)
                if enemy.y >= 600:
                    health_bar.remove(health)
                    enemy_list.remove(enemy)
                if len(health_bar) == 0:
                    game_on == False
                    if game_on != True:
                        camera.clear('black')
                        camera.draw(gamebox.from_text(400, 300, "GAME OVER!", 40, "Yellow", bold=True))
                        gamebox.pause()

        if spaceship.x - spaceship.width / 2 < 0:
            spaceship.x = spaceship.width / 2
        if spaceship.x + spaceship.width / 2 > 800:
            spaceship.x = 800 - spaceship.width / 2

        camera.draw(spaceship)

        score_keeper = gamebox.from_text(20, 570, str(int(seconds_since_start)), 40, "Yellow", bold=True)
        camera.draw(score_keeper)

    else:
        camera.clear('black')
        # title fram background url: https://en.wikipedia.org/wiki/Andromeda_Galaxy
        background = gamebox.from_image(400, 300, 'main screen image.jpg')
        camera.draw(background)
        camera.draw(gamebox.from_text(400, 300, "PLANET PROTECTORS", 80, "Yellow", bold=True))
        camera.draw(gamebox.from_text(400, 330, 'Press \'S\' to start the game', 30, 'white', bold=True))
        camera.draw(gamebox.from_text(400, 350, 'Use LEFT and RIGHT arrows to move the spaceship and avoid enemies',20,'white', bold = True))

    if len(health_bar) == 0:
        game_over = True
        camera.clear('black')
        background_main_game = gamebox.from_image(400, 300, 'main game background.jpg')
        camera.draw(background_main_game)
        camera.draw(gamebox.from_text(400, 300, "GAME OVER!", 40, "Yellow", bold=True))
        camera.draw(gamebox.from_text(400, 350, "Your survival time: " + str(int(seconds_since_start)) +" seconds", 30, 'Yellow'))
        gamebox.pause()


    camera.display()




gamebox.timer_loop(30, tick)
