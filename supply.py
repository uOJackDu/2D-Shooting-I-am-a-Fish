#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 24 17:08:24 2021

@author: jackdu
"""
import pygame
import random


class Apple(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("images/apple.png").convert_alpha()
        
        self.rect = self.image.get_rect()
        self.bg_width, self.bg_height = bg_size[0], bg_size[1]
        self.rect.left = random.randint(0, self.bg_width - self.rect.width)
        self.facing = random.choice([2, 4])
        if self.facing == 2:
            self.rect.top = self.bg_height + 10
        elif self.facing == 4:
            self.rect.bottom = -10
        self.speed = 3
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)
        self.shift_right = random.choice([True, False])
    
    def moveUp(self):
        if self.rect.bottom > 0:
            self.rect.top -= self.speed
        else:
            self.active = False
    
    def moveDown(self):
        if self.rect.top < self.bg_height:
            self.rect.top += self.speed
        else:
            self.active = False
    
    def shift(self):
        if self.shift_right:
            self.rect.left += 1
        else:
            self.rect.left -= 1
    
    def reset(self):
        self.active = True
        self.shift_right = random.choice([True, False])
        self.rect.left = random.randint(0, self.bg_width - self.rect.width)
        self.facing = random.choice([2, 4])
        if self.facing == 2:
            self.rect.top = self.bg_height + 10
        elif self.facing == 4:
            self.rect.bottom = -10


class Pizza(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("images/pizza.png").convert_alpha()
        
        self.rect = self.image.get_rect()
        self.bg_width, self.bg_height = bg_size[0], bg_size[1]
        self.rect.left = random.randint(0, self.bg_width - self.rect.width)
        self.facing = random.choice([2, 4])
        if self.facing == 2:
            self.rect.top = self.bg_height + 10
        elif self.facing == 4:
            self.rect.bottom = -10
        self.speed = 3
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)
        self.shift_right = random.choice([True, False])
        
    def moveUp(self):
        if self.rect.bottom > 0:
            self.rect.top -= self.speed
        else:
            self.active = False
    
    def moveDown(self):
        if self.rect.top < self.bg_height:
            self.rect.top += self.speed
        else:
            self.active = False
    
    def shift(self):
        if self.shift_right:
            self.rect.left += 2
        else:
            self.rect.left -= 2
    
    def reset(self):
        self.active = True
        self.shift_right = random.choice([True, False])
        self.rect.left = random.randint(0, self.bg_width - self.rect.width)
        self.facing = random.choice([2, 4])
        if self.facing == 2:
            self.rect.top = self.bg_height + 10
        elif self.facing == 4:
            self.rect.bottom = -10


class Chest(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("images/chest.png").convert_alpha()
        
        self.rect = self.image.get_rect()
        self.bg_width, self.bg_height = bg_size[0], bg_size[1]
        self.rect.top = random.randint(0, self.bg_height - self.rect.height)
        self.rect.right = -10
        self.destinationx = random.randint(0, self.bg_width - self.rect.width)
        self.speed = 3
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)
    
    def move(self):
        if self.rect.left < self.destinationx:
            self.rect.left += self.speed
    
    def reset(self):
        self.active = True
        self.rect.top = random.randint(0, self.bg_height - self.rect.height)
        self.rect.right = -10
        self.destinationx = random.randint(0, self.bg_width - self.rect.width)
