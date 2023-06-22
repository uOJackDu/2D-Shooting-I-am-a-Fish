#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 24 17:07:03 2021

@author: jackdu
"""
import pygame


class Player(pygame.sprite.Sprite):
    hp = 64
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        
        self.image_right = pygame.image.load("images/me_right.png").convert_alpha()
        self.image_up = pygame.image.load("images/me_up.png").convert_alpha()
        self.image_left = pygame.image.load("images/me_left.png").convert_alpha()
        self.image_down = pygame.image.load("images/me_down.png").convert_alpha()
        self.shield1 = pygame.image.load("images/shield1.png").convert_alpha()
        self.shield2 = pygame.image.load("images/shield2.png").convert_alpha()
        self.super_speed1 = pygame.image.load("images/super_speed1.png").convert_alpha()
        self.super_speed2 = pygame.image.load("images/super_speed2.png").convert_alpha()
        
        # Size of the window        
        self.width, self.height = bg_size[0], bg_size[1]
        # Size of the payer
        self.rect = self.image_left.get_rect()
        self.rect.left = self.width - self.rect.width - 10
        self.rect.top = (self.height-self.rect.height) // 2
        
        self.facing = 3
        self.speed = 4
        self.active = True
        self.mask = pygame.mask.from_surface(self.image_right)
        self.invincible = False
        self.life = 3
        self.hp = Player.hp
    
    def moveUp(self):
        if self.rect.bottom > 0:
            self.rect.top -= self.speed+1
    
    def moveDown(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed+1
    
    def moveLeft(self):
        if self.rect.right > 0:
            self.rect.left -= self.speed        
    
    def moveRight(self):
        if self.rect.left < self.width:
            self.rect.left += self.speed
    
    def reset(self):
        self.rect.left = self.width - self.rect.width - 10
        self.rect.top = (self.height-self.rect.height) // 2
        self.hp = Player.hp
        self.facing = 3


class Background(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        
        self.image_day = pygame.image.load("images/background_day.png").convert_alpha()
        self.image_night = pygame.image.load("images/background_night.png").convert_alpha()
        
        self.rect = self.image_day.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
