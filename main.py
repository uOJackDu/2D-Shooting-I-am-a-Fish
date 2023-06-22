#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 16:06:49 2021

@author: jackdu
"""
import pygame
import sys
import traceback
import random
import player
import enemy
import bullet
import supply

from pygame.locals import *

pygame.init()

bg_size = bg_width, bg_height = 960, 700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("2D Shooting - By Jack Du")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 250, 83)


def draw_HP_bar(each, hp_remain):
    # Draw the black line
    length = each.rect.right - each.rect.left
    pygame.draw.line(screen, BLACK, \
                     (each.rect.left, each.rect.top-5), \
                     (each.rect.right, each.rect.top-5), 4)
    # Let HP bar be green if energy is larger than 20%, else let it be red
    if (hp_remain < 0.2) or (each.hp == 1):
        hp_color = RED
    else:
        hp_color = GREEN
    pygame.draw.line(screen, hp_color, \
                     (each.rect.left, each.rect.top-5), \
                     (each.rect.left+hp_remain*length, \
                      each.rect.top-5), 4)


def increase_speed(target, inc):
    for each in target:
        each.speed += inc


def in_window(target, bg_size):
    if (target.rect.right>=0) and (target.rect.left<=bg_size[0]) and \
        (target.rect.bottom>=0) and (target.rect.top<=bg_size[1]):
        return True
    else:
        return False


def enemy_move(target, freeze):
    if target.facing == 1:
        target.moveRight(freeze)
    elif target.facing == 2:
        target.moveUp(freeze)
    elif target.facing == 3:
        target.moveLeft(freeze)
    elif target.facing == 4:
        target.moveDown(freeze)


def move(target):
    if target.facing == 1:
        target.moveRight()
    elif target.facing == 2:
        target.moveUp()
    elif target.facing == 3:
        target.moveLeft()
    elif target.facing == 4:
        target.moveDown()


def check_life(me, SHIELD_TIME):
    if me.hp <= 0:
        me.life -= 1
        if me.life == 0:
            me.active = False
        else:
            me.reset()
            me.invincible = True
            pygame.time.set_timer(SHIELD_TIME, 5*1000)


def main():
    # Generate the background
    bg = player.Background(bg_size)
    # Generate the player
    me = player.Player(bg_size)
    # Generate the enemies group
    enemies = pygame.sprite.Group()
    # Generate the small enemy
    small_enemies = pygame.sprite.Group()
    for i in range(0, 8):
        enemy1 = enemy.SmallEnemy(bg_size)
        small_enemies.add(enemy1)
        enemies.add(enemy1)
    # Generate dinosaurs
    dinosaurs = pygame.sprite.Group()
    for i in range(0, 2):
        dinosaur = enemy.Dinosaur(bg_size)
        dinosaurs.add(dinosaur)
        enemies.add(dinosaur)
    # Generate the boss
    bosses = pygame.sprite.Group()
    boss1 = enemy.Boss(bg_size)
    bosses.add(boss1)
    enemies.add(boss1)
    # Generate the player's bullets
    bullet1 = []
    bullet1_index = 0
    BULLET1_NUM = 12
    for i in range(BULLET1_NUM):
        bullet1.append(bullet.Bullet1(bg_size, me.rect.center))
    # Generate the boss's bullets
    bullet2_group = pygame.sprite.Group()
    bullet2 = []
    bullet2_index = 0
    BULLET2_NUM = 12
    for i in range(BULLET2_NUM):
        bullet2.append(bullet.Bullet2(bg_size, boss1.rect.center))
        bullet2_group.add(bullet2[i])
    
    delay = 200
    switch_image = True  # Switch image of the small enemy
    switch_shield = False
    switch_super_speed = False    
    
    score = 0
    score_font = pygame.font.Font("fonts/Papyrus.ttc", 36)
    
    paused = False
    pause_image = pygame.image.load("images/pause.png").convert_alpha()
    pause_pressed_image = pygame.image.load("images/pause_pressed.png").convert_alpha()
    resume_image = pygame.image.load("images/resume.png").convert_alpha()
    resume_pressed_image = pygame.image.load("images/resume_pressed.png").convert_alpha()
    paused_rect = pause_image.get_rect()
    paused_rect.left = bg_width - paused_rect.width - 10
    paused_rect.top = 5
    paused_image = pause_image
    
    level = 1
    promt_font = pygame.font.Font("fonts/Papyrus.ttc", 48)
    freeze = False
    game_mode = 0  # Daytime
    
    life_image = pygame.image.load("images/life.png").convert_alpha()
    life_rect = life_image.get_rect()
    
    FIRE_CD = USEREVENT
    cooled = True
    
    LV_UP = USEREVENT + 1
    lv_up = False    
    BOSS_COMING = USEREVENT + 2
    boss_coming = False
    boss_battle = False
    shift_direction = 1
    
    SUPER_SPEED_TIME = USEREVENT + 3
    is_super_speed = False
    SHIELD_TIME = USEREVENT + 4
    
    # Generate the food
    apple = supply.Apple(bg_size)
    pizza = supply.Pizza(bg_size)
    food = pygame.sprite.Group()
    food.add(apple)
    food.add(pizza)
    # Set the food timer
    FOOD_TIME = USEREVENT + 5
    food_interval = random.randint(5, 20)
    pygame.time.set_timer(FOOD_TIME, food_interval*1000)
    
    NIGHT_TIME = USEREVENT + 6
    night_interval = random.randint(60, 120)
    pygame.time.set_timer(NIGHT_TIME, night_interval*1000)
    NIGHT_OVER = USEREVENT + 7
    
    chest = supply.Chest(bg_size)
    chest_touched = False
    # Initialize money
    game_record_r = open("game_record.txt", "r")
    for line in game_record_r:
        money = int(line.strip().split()[1])
    game_record_r.close()
    
    restart_image = pygame.image.load("images/restart.png").convert_alpha()
    restart_rect = restart_image.get_rect()
    quit_image = pygame.image.load("images/quit_game.png").convert_alpha()
    quit_rect = quit_image.get_rect()
    gameover_centerx = bg_width//2+130
    restart_rect.centerx = gameover_centerx
    restart_rect.top = bg_height//2
    quit_rect.centerx = gameover_centerx
    quit_rect.top = bg_height//2+100
    recorded = False
    
    clock = pygame.time.Clock()
    running = True
    screen.blit(bg.image_day, bg.rect)
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if (event.button == 1) and (paused_rect.collidepoint(event.pos)):
                    paused = not paused
                    if paused:
                        paused_image = resume_image
                    else:
                        paused_image = pause_image
            elif event.type == MOUSEMOTION:
                if paused_rect.collidepoint(event.pos):
                    if paused:
                        paused_image = resume_pressed_image
                    else:
                        paused_image = pause_pressed_image
                else:
                    if paused:
                        paused_image = resume_image
                    else:
                        paused_image = pause_image
            elif event.type == FIRE_CD:
                cooled = True
            elif event.type == LV_UP:
                lv_up = False
                pygame.time.set_timer(LV_UP, 0)
                boss_coming = True
                freeze = True
                pygame.time.set_timer(BOSS_COMING, 3*1000)
            elif event.type == BOSS_COMING:
                boss_coming = False
                pygame.time.set_timer(BOSS_COMING, 0)
                boss_battle = True
                for each in bosses:
                    each.active = True
            elif event.type == FOOD_TIME:
                food_index = random.choice([0, 1])
                if food_index == 0:
                    if not apple.active:
                        apple.reset()
                elif food_index == 1:
                    if not pizza.active:
                        pizza.reset()
            elif event.type == SUPER_SPEED_TIME:
                is_super_speed = False
                pygame.time.set_timer(SUPER_SPEED_TIME, 0)
            elif event.type == SHIELD_TIME:
                me.invincible = False
                pygame.time.set_timer(SHIELD_TIME, 0)
            elif event.type == NIGHT_TIME:
                game_mode = 1
                pygame.time.set_timer(NIGHT_OVER, 20*1000)
            elif event.type == NIGHT_OVER:
                game_mode = 0
        
        if not paused:
            if game_mode == 0:
                screen.blit(bg.image_day, bg.rect)
            elif game_mode == 1:
                screen.blit(bg.image_night, bg.rect)
            key_pressed = pygame.key.get_pressed()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                me.moveRight()
                me.facing = 1
            if key_pressed[K_w] or key_pressed[K_UP]:
                me.moveUp()
                me.facing = 2
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                me.moveLeft()
                me.facing = 3
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                me.moveDown()
                me.facing = 4     
            if key_pressed[K_SPACE]:  # Shoot a bullet
                if is_super_speed:
                    fire_interval = 100
                else:
                    fire_interval = 250                
                if cooled:
                    bullet1[bullet1_index].reset((me.rect.centerx-5, me.rect.centery))
                    bullet1[bullet1_index].facing = me.facing
                    bullet1_index = (bullet1_index+1) % BULLET1_NUM         
                    cooled = False
                    pygame.time.set_timer(FIRE_CD, fire_interval)
            if key_pressed[K_f]:
                if chest_touched:
                    chest_touched = False
                    chest.active = False
                    money += random.randint(1, 2500)
                    freeze = False
            
            # Increase difficulty as level increases
            if (level == 1) and (score >= 100):
                level = 2
                food_interval = 15
                pygame.time.set_timer(FOOD_TIME, food_interval*1000)
                pygame.time.set_timer(LV_UP, 3*1000)
                lv_up = True
            elif (level == 2) and (score >= 800):
                level = 3
                dinosaur = enemy.Dinosaur(bg_size)
                dinosaurs.add(dinosaur)
                enemies.add(dinosaur)
                increase_speed(small_enemies, 1)
                food_interval = 8
                pygame.time.set_timer(FOOD_TIME, food_interval*1000)
                pygame.time.set_timer(LV_UP, 3*1000)
                lv_up = True
            elif (level == 3) and (score >= 1600):
                level = 4
                increase_speed(dinosaurs, 1)
                food_interval = 5
                pygame.time.set_timer(FOOD_TIME, food_interval*1000)
                pygame.time.set_timer(LV_UP, 3*1000)
                lv_up = True
            elif (level == 4) and (score >= 3200):
                level = 5
                increase_speed(small_enemies, 1)
                pygame.time.set_timer(LV_UP, 3*1000)
                lv_up = True
            
            # Draw chest and check if it is obtained by the player
            if chest.active:
                if delay % 2 == 0:
                    chest.move()
                screen.blit(chest.image, chest.rect)
                if pygame.sprite.collide_mask(chest, me):
                    chest_touched = True
                else:
                    chest_touched = False
            # Draw apple and check if it is obtained by the player
            if apple.active:
                if delay % 2 == 0:
                    move(apple)
                    apple.shift()
                screen.blit(apple.image, apple.rect)
                if pygame.sprite.collide_mask(apple, me):
                    if game_mode == 0:
                        is_super_speed = True
                        pygame.time.set_timer(SUPER_SPEED_TIME, 8*1000)
                        apple.active = False
                    elif game_mode == 1:
                        if not me.invincible:
                            me.hp -= 1
                            check_life(me, SHIELD_TIME)
            # Draw pizza and check if it is obtained by the player
            if pizza.active:
                if delay % 2 == 0:
                    move(pizza)
                    pizza.shift()
                screen.blit(pizza.image, pizza.rect)
                if pygame.sprite.collide_mask(pizza, me):
                    if game_mode == 0:
                        me.invincible = True
                        pygame.time.set_timer(SHIELD_TIME, 8*1000)
                        pizza.active = False
                    elif game_mode == 1:
                        if not me.invincible:
                            me.hp -= 1
                            check_life(me, SHIELD_TIME)
            
            # Shoot the boss's bullets
            for each in bosses:
                if each.rect.bottom > 0:
                    if delay % 30 == 0:
                        bullet2[bullet2_index].reset((each.rect.centerx-18, each.rect.bottom))
                        bullet2_index = (bullet2_index+1) % BULLET2_NUM
            
            # Check collisions between bullets and enemies
            for b in bullet1:
                if b.active:
                    move(b)
                    screen.blit(b.image, b.rect)
                    enemy_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                    if enemy_hit:
                        b.active = False
                        for e in enemy_hit:
                            if (e in dinosaurs) or (e in bosses):
                                e.hit = True
                                e.hp -= 1
                                if e.hp == 0:
                                    e.active = False
                            else:
                                e.active = False
            # Check if the player is hit by the boss's bullets
            for b in bullet2_group:
                if b.active:
                    move(b)
                    screen.blit(b.image, b.rect)
            bullet_hit = pygame.sprite.spritecollide(me, bullet2_group, False, pygame.sprite.collide_mask)
            if bullet_hit:
                for b_hit in bullet_hit:
                    if (not me.invincible) and (b_hit.active):
                        me.hp -= 1
                        check_life(me, SHIELD_TIME)
                    b_hit.active = False
                            
            
            # Draw the Boss
            if boss_battle == True:
                for each in bosses:
                    if each.active:
                        hp_remain = each.hp / enemy.Boss.hp                   
                        if each.rect.top < 10:
                            each.move()
                        each.shift(shift_direction)
                        if delay % 60 == 0:
                            shift_direction = random.choice([1, 2])
                        if delay % 30 == 0:
                            if each.rect.centerx > me.rect.centerx:
                                shift_direction = 1
                            elif each.rect.centerx < me.rect.centerx:
                                shift_direction = 2
                        screen.blit(each.image, each.rect)
                        draw_HP_bar(each, hp_remain)
                    else:  # Boss is destroyed
                        score += 100
                        money += random.randint(1, 200)
                        boss_battle = False
                        each.reset()
                        chest.reset()
            
            # Draw the dinosaur
            for each in dinosaurs:
                if each.active:
                    if in_window(each, bg_size):
                        each.entered = True 
                    if game_mode == 0:
                        move(each)
                    if each.facing == 1:
                        screen.blit(each.image_right, each.rect)
                    elif each.facing == 3:
                        screen.blit(each.image_left, each.rect)
                    hp_remain = each.hp / enemy.Dinosaur.hp
                    if each.hit:  # Draw the hp bar only after the dinosaur is hit
                        draw_HP_bar(each, hp_remain)
                else:  # Destroy
                    if delay % 3 == 0:
                        score += 50
                        money += random.randint(1, 100)
                        each.reset()
            
            # Draw the small enemy
            for each in small_enemies:
                if each.active:
                    if in_window(each, bg_size):
                        each.entered = True 
                    if ((not freeze) or (each.entered)) and (game_mode == 0):
                        enemy_move(each, freeze)
                    
                    if each.facing == 2:
                        screen.blit(each.image_up, each.rect)
                    elif each.facing == 4:
                        screen.blit(each.image_down, each.rect)
                else:  # Destroy
                    if delay % 3 == 0:
                        score += 10
                        money += random.randint(1, 50)
                        each.reset()
            
            # Draw the player
            if me.active:                
                if me.facing == 1:
                    screen.blit(me.image_right, me.rect)
                elif me.facing == 2:
                    screen.blit(me.image_up, me.rect)
                elif me.facing == 3:
                    screen.blit(me.image_left, me.rect)
                elif me.facing == 4:
                    screen.blit(me.image_down, me.rect)
                # Update the player's mask according to facing
                if (me.facing == 1) or (me.facing == 3):
                    me.mask = pygame.mask.from_surface(me.image_right)
                elif (me.facing == 2) or (me.facing == 4):
                    me.mask = pygame.mask.from_surface(me.image_up)
                
                if me.invincible:
                    if switch_shield:
                        screen.blit(me.shield1, me.rect)
                    else:
                        screen.blit(me.shield2, me.rect)
                if is_super_speed:
                    if switch_super_speed:
                        screen.blit(me.super_speed1, me.rect)
                    else:
                        screen.blit(me.super_speed2, me.rect)
                hp_remain = me.hp / player.Player.hp
                draw_HP_bar(me, hp_remain)
            else:  # Destroy the player
                print("Game over.")
                paused = True
            
            # Check collision of the player
            enemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)
            if enemies_down:
                for e in enemies_down:
                    if (game_mode == 0) or (e in bosses):
                        if (not me.invincible) and (e.active):
                            if e in bosses:
                                me.hp -= 1
                                check_life(me, SHIELD_TIME)
                            else:
                                me.hp -= 16
                                check_life(me, SHIELD_TIME)
                    elif game_mode == 1:
                        money += random.randint(1, 200)
                    if e not in bosses:
                        e.active = False
        if me.life <= 0:  # Display Game Over messages
            screen.blit(bg.image_day, bg.rect)
            if not recorded:
                recorded = True
                game_record_r = open("game_record.txt", "r")
                for line in game_record_r:
                    highest_score = int(line.strip().split()[0])
                    if score > highest_score:
                        highest_score = score
                game_record_r.close()
                game_record_w = open("game_record.txt", "w")
                game_record_w.write("{} {}".format(str(highest_score), str(money)))
                game_record_w.close()
            gameover_text = promt_font.render("GAME OVER", True, RED)
            yourscore_text = promt_font.render("Your score: {}".format(str(score)), True, BLACK)
            highestscore_text = promt_font.render("Highest score: {}".format(str(highest_score)), True, BLACK)
            gameover_text_rect = gameover_text.get_rect()
            yourscore_text_rect = yourscore_text.get_rect()
            highestscore_text_rect = highestscore_text.get_rect()
            gameover_text_rect.centerx, gameover_text_rect.top = gameover_centerx, 100
            yourscore_text_rect.centerx, yourscore_text_rect.top = gameover_centerx, 170
            highestscore_text_rect.centerx, highestscore_text_rect.top = gameover_centerx, 240
            screen.blit(gameover_text, gameover_text_rect)
            screen.blit(yourscore_text, yourscore_text_rect)
            screen.blit(highestscore_text, highestscore_text_rect)
            # Draw the restart and quit button, and check if they are pressed
            screen.blit(restart_image, restart_rect)
            screen.blit(quit_image, quit_rect)
            if pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()
                if (mouse_pos[0]>restart_rect.left) and (mouse_pos[0]<restart_rect.right) \
                    and (mouse_pos[1]>restart_rect.top) and (mouse_pos[1]<restart_rect.bottom):
                        main()
                elif (mouse_pos[0]>quit_rect.left) and (mouse_pos[0]<quit_rect.right) \
                    and (mouse_pos[1]>quit_rect.top) and (mouse_pos[1]<quit_rect.bottom):
                        pygame.quit()
                        sys.exit()
        else:
            # Display score  
            score_text = score_font.render("Score: {}".format(score), True, BLACK)
            screen.blit(score_text, (150, 5))
            # Display lives left
            for i in range(0, me.life):
                screen.blit(life_image, (bg_width-165-45*i, 15))
            # Draw the pause button
            screen.blit(paused_image, paused_rect)
            # Display chest reminder
            chest_text = score_font.render("Press F to open.", True, BLACK)
            if chest_touched:
                screen.blit(chest_text, (bg_width-200, bg_height-50))
            
        # Display money
        money_text = score_font.render("$ {}".format(money), True, BLACK)
        screen.blit(money_text, (20, bg_size[1]-50))
        # Display level
        level_color = BLACK
        if (level >= 3) and (level < 5):
            level_color = GREEN
        elif level >= 5:
            level_color = RED
        level_text = score_font.render("Lv {}".format(level), True, level_color)        
        screen.blit(level_text, (bg_width-110, 6))
        lv_up_text = promt_font.render("Lv {}!".format(level), True, level_color)
        if lv_up:
            screen.blit(lv_up_text, (bg_width//2, bg_height//2))
        boss_coming_text = promt_font.render("BOSS is coming!", True, RED)
        if boss_coming:
            screen.blit(boss_coming_text, (bg_width//2, bg_height//2))
        
        # Switch images of the small enemy
        if delay % 60 == 0:
            switch_image = not switch_image
        if delay % 20 == 0:
            switch_shield = not switch_shield
            switch_super_speed = not switch_super_speed
        
        delay -= 1
        if delay == 0:
            delay = 200
        pygame.display.flip()
        clock.tick(60)  # Frams per sec: 60
    
    pygame.quit()


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
