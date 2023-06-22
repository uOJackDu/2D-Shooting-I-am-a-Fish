#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 24 17:19:46 2021

@author: jackdu
"""
import pygame


class Bullet1(pygame.sprite.Sprite):
    def __init__(self, bg_size, position):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("images/bullet1.png").convert_alpha()
        
        self.bg_width, self.bg_height = bg_size[0], bg_size[1]
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
        self.speed = 8
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)
        self.facing = 1
    
    def moveUp(self):
        self.rect.top -= self.speed
        
        if self.rect.bottom < 0:
            self.active = False
    
    def moveDown(self):
        self.rect.top += self.speed
        
        if self.rect.top > self.bg_height:
            self.active = False
    
    def moveLeft(self):
        self.rect.left -= self.speed
        
        if self.rect.right < 0:
            self.active = False
    
    def moveRight(self):
        self.rect.left += self.speed
        
        if self.rect.left > self.bg_width:
            self.active = False
    
    def reset(self, position):
        self.active = True
        self.rect.left, self.rect.top = position


class Bullet2(pygame.sprite.Sprite):
    def __init__(self, bg_size, position):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("images/bullet2.png").convert_alpha()
        
        self.bg_width, self.bg_height = bg_size[0], bg_size[1]
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
        self.speed = 4
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)
        self.facing = 4
    
    def moveDown(self):
        self.rect.top += self.speed
        
        if self.rect.top > self.bg_height:
            self.active = False
    
    def reset(self, position):
        self.active = True
        self.rect.left, self.rect.top = position
