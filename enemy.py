#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 24 17:08:12 2021

@author: jackdu
"""
import pygame
import random


def turn_around(facing):
    facing += 2
    if facing > 4:
        facing %= 4
    return facing


class SmallEnemy(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        
        self.image_up = pygame.image.load("images/small_enemy_up.png").convert_alpha()
        self.image_down = pygame.image.load("images/small_enemy_down.png").convert_alpha() 
        self.rect = self.image_up.get_rect()
        # Size of the window
        self.width, self.height = bg_size[0], bg_size[1]
        
        self.speed = random.randint(1, 3)
        self.active = True
        self.rect.left = random.randint(0, self.width - self.rect.width)
        self.facing = random.choice([2, 4])
        if self.facing == 2:
            self.rect.top = random.randint(2*self.height, 3*self.height)
        elif self.facing == 4:
            self.rect.bottom = random.randint(-2*self.height, -1*self.height)
        self.mask = pygame.mask.from_surface(self.image_up)
        self.entered = False
    
    def moveUp(self, freeze):
        if not freeze:
            if self.rect.top > 0:
                self.rect.top -= self.speed
            else:
                self.facing = turn_around(self.facing)
        else:
            if self.rect.bottom > 0:
                self.rect.top -= self.speed
            else:
                self.reset()
    
    def moveDown(self, freeze):
        if not freeze:
            if self.rect.bottom < self.height:
                self.rect.top += self.speed
            else:
                self.facing = turn_around(self.facing)
        else:
            if self.rect.top < self.height:
                self.rect.top += self.speed
            else:
                self.reset()
    
    def reset(self):
        self.active = True
        self.rect.left = random.randint(0, self.width - self.rect.width)
        self.facing = random.choice([2, 4])
        if self.facing == 2:
            self.rect.top = random.randint(2*self.height, 3*self.height)
        elif self.facing == 4:
            self.rect.bottom = random.randint(-2*self.height, -1*self.height)
        self.entered = False


class Dinosaur(pygame.sprite.Sprite):
    hp = 4
    
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        
        self.image_right = pygame.image.load("images/dinosaur_right.png").convert_alpha()
        self.image_left = pygame.image.load("images/dinosaur_left.png").convert_alpha()
        self.rect = self.image_right.get_rect()
        # Size of the window
        self.bg_width, self.bg_height = bg_size[0], bg_size[1]
        
        self.speed = 1
        self.active = True
        self.rect.top = random.randint(0, self.bg_height - self.rect.height)
        self.facing = random.choice([1, 3])
        if self.facing == 1:
            self.rect.right = random.randint(-1*self.bg_width, 0)
        elif self.facing == 3:
            self.rect.left = random.randint(self.bg_width, 2*self.bg_width)
        self.mask = pygame.mask.from_surface(self.image_right)
        self.hp = Dinosaur.hp
        self.hit = False
    
    def moveLeft(self):
        if self.rect.left > 0:
            self.rect.left -= self.speed
        else:
            self.facing = turn_around(self.facing)
    
    def moveRight(self):
        if self.rect.right < self.bg_width:
            self.rect.left += self.speed
        else:
            self.facing = turn_around(self.facing)
    
    def reset(self):
        self.active = True
        self.hit = False
        self.hp = Dinosaur.hp
        self.rect.top = random.randint(0, self.bg_height - self.rect.height)
        self.facing = random.choice([1, 3])
        if self.facing == 1:
            self.rect.left = random.randint(-2*self.bg_width, -1*self.bg_width)
        elif self.facing == 3:
            self.rect.left = random.randint(2*self.bg_width, 3*self.bg_width)


class Boss(pygame.sprite.Sprite):
    hp = 32
    
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("images/boss.png").convert_alpha()
        self.rect = self.image.get_rect()
        # Size of the window
        self.bg_width, self.bg_height = bg_size[0], bg_size[1]
        
        self.speed = 1
        self.active = False
        self.rect.left = random.randint(0, self.bg_width - self.rect.width)
        self.rect.top = random.randint(int(-1.5*self.bg_height), int(-0.5*self.bg_height))
        self.mask = pygame.mask.from_surface(self.image)
        self.hp = Boss.hp
    
    def move(self):
        if self.rect.top < self.bg_height:
            self.rect.top += self.speed
        else:
            self.rect.bottom = 0
    
    def shift(self, direction):
        if direction == 1:
            if self.rect.left > 0:
                self.rect.left -= 4
                self.rect.top += 1
        elif direction == 2:
            if self.rect.right < self.bg_width:
                self.rect.left += 4
                self.rect.top -= 1
    
    def reset(self):
        self.active = False
        self.hp = Boss.hp
        self.rect.left = random.randint(0, self.bg_width - self.rect.width)
        self.rect.top = random.randint(int(-1.5*self.bg_height), int(-0.5*self.bg_height))
