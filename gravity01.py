#!/usr/bin/env python

import numpy as np
import random
import math
import pygame as pg

# constants
WINSIZE = [640, 480]
WINCENTER = [320, 240]
NUMSTARS = 100

grav_const = 6.67430e-11 # m^3 kg^-1 s^-2

class SpaceObject:
    def __init__(self, n, m, x, y, z, r):
        self.name = n
        self.mass = m
        self.position = np.float32([x, y, z])
        self.radius = r

def distance(so1, so2):
    d = so1.position - so2.position
    return (np.inner(d, d))

def grav_force(so1, so2):
    fg = grav_const * so1.mass * so2.mass / distance(so1, so2) # N
    return fg

""" pg.examples.stars

    We are all in the gutter,
    but some of us are looking at the stars.
                                            -- Oscar Wilde

A simple starfield example. Note you can move the 'center' of
the starfield by leftclicking in the window. This example show
the basics of creating a window, simple pixel plotting, and input
event management.
"""


def init_star():
    "creates new star values"
    dir = random.randrange(100000)
    velmult = random.random() * 0.6 + 0.4
    vel = [math.sin(dir) * velmult, math.cos(dir) * velmult]
    return vel, WINCENTER[:]


def initialize_stars():
    "creates a new starfield"
    stars = []
    for x in range(NUMSTARS):
        star = init_star()
        vel, pos = star
        steps = random.randint(0, WINCENTER[0])
        pos[0] = pos[0] + (vel[0] * steps)
        pos[1] = pos[1] + (vel[1] * steps)
        vel[0] = vel[0] * (steps * 0.09)
        vel[1] = vel[1] * (steps * 0.09)
        stars.append(star)
    move_stars(stars)
    return stars


def draw_stars(surface, stars, color):
    "used to draw (and clear) the stars"
    for vel, pos in stars:
        pos = (int(pos[0]), int(pos[1]))
        surface.set_at(pos, color)


def move_stars(stars):
    "animate the star values"
    for vel, pos in stars:
        pos[0] = pos[0] + vel[0]
        pos[1] = pos[1] + vel[1]
        if not 0 <= pos[0] <= WINSIZE[0] or not 0 <= pos[1] <= WINSIZE[1]:
            vel[:], pos[:] = init_star()
        else:
            vel[0] = vel[0] * 1.05
            vel[1] = vel[1] * 1.05


def main():
    ## random testing of my class
    m_starship = 1e6 ## kg, 1000 tons
    m_sun = 1.9884e30 ## kg
    dist = 149.6e9 ## m, 149.6 Mio km = 1AU = 1 Astronomical Unit
    
    spaceship = SpaceObject('Enterprise', 1e6, 149.6e9, 0, 0, 5)
    print(spaceship.name)
    sun = SpaceObject('Sun', 1.9884e30, 0, 0, 0, 10)

    distance(spaceship, sun)
    print(grav_force(spaceship, sun))
          
   
    "This is the starfield code"
    # create our starfield
    random.seed()
    stars = initialize_stars()
    clock = pg.time.Clock()
    # initialize and prepare screen
    pg.init()
    screen = pg.display.set_mode(WINSIZE)
    pg.display.set_caption("pygame Stars Example")
    white = 255, 240, 200
    black = 20, 20, 40
    screen.fill(black)

    # main game loop
    done = 0
    while not done:
        draw_stars(screen, stars, black)
        move_stars(stars)
        draw_stars(screen, stars, white)
        pg.display.update()
        for e in pg.event.get():
            if e.type == pg.QUIT or (e.type == pg.KEYUP and e.key == pg.K_ESCAPE):
                done = 1
                break
            elif e.type == pg.MOUSEBUTTONDOWN and e.button == 1:
                WINCENTER[:] = list(e.pos)
        clock.tick(50)


# if python says run, then we should run
if __name__ == "__main__":
    main()

    # I prefer the time of insects to the time of stars.
    #
    #                              -- Wisława Szymborska

