# This file was created by Farid Rohana
# content from kids can code: http://kidscancode.org/blog/
# Took cloud image from https://www.pinterest.com/dannyfoo/fluffy-cloud/
# Took bomb image from https://www.istockphoto.com/vector/cartoon-bomb-illustration-gm842671590-137549743
# Code from Chris Bradfield
# Help for coin code from Cary Yao
# Goals:
'''
- make coins that increase score by 1 everytime they are collected
- make enemies that can kill the player with collide function
- make more types of platforms 
'''


# import libraries and modules
import pygame as pg
from pygame.sprite import Sprite
import random
from random import randint
import os
from settings import *
from sprites import *

vec = pg.math.Vector2

# setup asset folders here - images sounds etc.
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
snd_folder = os.path.join(game_folder, 'sounds')



class Game:
    def __init__(self):
        # init pygame and create a window
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("My Game...")
        self.clock = pg.time.Clock()
        self.running = True
    
    def new(self):
        # create a group for all sprites
        self.score = 0
        self.hitpoints = 10
        self.all_sprites = pg.sprite.Group()
        self.all_platforms = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.all_coins = pg.sprite.Group()
        # instantiate classes
        self.player = Player(self)
        # add instances to groups
        self.all_sprites.add(self.player)

        for p in PLATFORM_LIST:
            # instantiation of the Platform class
            plat = Platform(*p)
            self.all_sprites.add(plat)
            self.all_platforms.add(plat)

        # Spawns mobs randomly 
        # Range is the amount of mobs that will spawn
        for m in range(0,15):
            # randomly adds bomb enemies in a chunk of space
            m = Mob(randint(0, WIDTH), randint(0, HEIGHT), 20, 20, "normal")
            self.all_sprites.add(m)
            self.all_mobs.add(m)

        # Spawns coins in randomly 
        # Range is the amount of coins that can spawn
        for c in range(0,15):
            # Randomly adds coins in a chunk of space
            c = Coin(randint(0, WIDTH), randint(0, HEIGHT), 20, 20, "normal")
            self.all_sprites.add(c)
            self.all_coins.add(c)

        self.run()
    
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.all_sprites.update()

        # this is what prevents the player from falling through the platform when falling down...
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.all_platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
                self.player.vel.x = hits[0].speed*1.5

                    
         # this prevents the player from jumping up through a platform
        if self.player.vel.y < 0:
            hits = pg.sprite.spritecollide(self.player, self.all_platforms, False)
            if hits:
                print("ouch")
                if self.player.rect.bottom >= hits[0].rect.top - 1:
                    self.player.rect.top = hits[0].rect.bottom
                    self.player.acc.y = 5
                    self.player.vel.y = 0
        
        # Coin collection code
        # When a player collides with a coin, their "score" goes up by 1 point
        if pg.sprite.spritecollide(self.player, self.all_coins, True):
            self.player.score += 1
        
        # When a player collides with a bomb their health/hitpoints go down by 1 point
        if pg.sprite.spritecollide(self.player, self.all_mobs, True):
            self.player.hitpoints -= 1

    def events(self):
        for event in pg.event.get():
        # check for closed window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
                
    def draw(self):
        ############ Draw ################
        # draw the background screen
        self.screen.fill(LIGHTBLUE)
        # draw all sprites
        self.all_sprites.draw(self.screen)
        # This draws the score text which goes up by 1 point every time a coin is collected
        self.draw_text("Score: " + str(self.player.score), 22, RED, 50, HEIGHT/10)
        # Draws the "hitpoints" text which indicates the player's health
        self.draw_text("Hitpoints: " + str(self.player.hitpoints), 22, RED, 63, 80)
        # This draws a "You Win" text in the middle of the screem when you collect all 10 coins
        if self.player.score == 10:
            self.draw_text("You Win!!!", 50, RED, 230, 210)
        # When you lose at least 10 hitpoints, the "you lose" screen pops up
        if self.player.hitpoints <= 0:
            # fills the entire screen black
            self.screen.fill(BLACK)
            # draws "You lose" text approximately in the middle of the black screen
            self.draw_text("You Lose!!!", 50, RED, 230, 210)


        # buffer - after drawing everything, flip display
        pg.display.flip()
    
    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)
    

    def show_start_screen(self):
        pass
    def show_go_screen(self):
        pass

g = Game()
while g.running:
    g.new()



pg.quit()
