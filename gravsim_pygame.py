#!/usr/bin/env python
""" pygame.examples.aliens

Shows a mini game where you have to defend against aliens.

What does it show you about pygame?

* pg.sprite, the difference between Sprite and Group.
* dirty rectangle optimization for processing for speed.
* music with pg.mixer.music, including fadeout
* sound effects with pg.Sound
* event processing, keyboard handling, QUIT handling.
* a main loop frame limited with a game clock from pg.time.Clock
* fullscreen switching.


Controls
--------

* Left and right arrows to move.
* Space bar to shoot
* f key to toggle between fullscreen.

"""

import random
import os
import numpy as np

# import basic pygame modules
import pygame as pg

# see if we can load more than standard BMP
# if not pg.image.get_extended():
#     raise SystemExit("Sorry, extended image module required")

# game constants
WIDTH = 640
HEIGHT = 480
SCREENRECT = pg.Rect(0, 0, WIDTH, HEIGHT)
# SCORE = 0
GRAV_CONST = 1e-23

MASS_SUN = 1.981e30     # kg
MASS_EARTH = 5.972e24   # kg

main_dir = os.path.split(os.path.abspath(__file__))[0]

# Each type of game object gets an init and an update function.
# The update function is called once per frame, and it is when each object should
# change it's current position and state.
#
# The Player object actually gets a "move" function instead of update,
# since it is passed extra information about the keyboard.


class SpaceObject:
    """ Contains the properties of a space object, like mass, position, velocity, and radius
    """

    def __init__(self, obj_name, obj_mass):
        self.name = obj_name
        self.mass = obj_mass             # kg
        self.position = np.array([0.0, 0.0, 0.0])  # m
        self.velocity = np.array([0.0, 0.0, 0.0])  # m/s
        self.radius = 10                 # m
        # TODO: this should not be here
        self.color = pg.Color(200, 200, 200, 255)


class GravitationalField:
    """ This should calculated the gravitational field generated by all registered objects,
        and the resulting forces as well.
    """
    delta_t = 0.1          # s
    space_objects = []
    epsilon = 1e-5

    def __init__(self):
        pass

    def distance(self, a: SpaceObject, b: SpaceObject):
        d = np.subtract(b.position, a.position)
        # d = np.inner(d, d)
        # return np.sqrt(d)
        return np.linalg.norm(d)

    def direction(self, a: SpaceObject, b: SpaceObject):
        v = np.subtract(b.position, a.position)
        # TODO: add some epsilon here.
        return v / np.linalg.norm(v)

    def grav_force(self, a: SpaceObject, b: SpaceObject):
        d = np.subtract(b.position, a.position)
        d = np.inner(d, d)
        return GRAV_CONST * a.mass * b.mass / d # in N, or kg m / s^2

    def add(self, new_object: SpaceObject):
        self.space_objects.append(new_object)

    def calculate(self):
        # TODO: everything, really...
        pass

    def accel(self):
        acc = []
        # TODO: this is now completely inefficient...
        for so1 in self.space_objects:
            acc.append(np.array([0, 0, 0]))
            for so2 in self.space_objects:
                if self.distance(so1, so2) > self.epsilon:
                    i = self.space_objects.index(so1)
                    acc[i] = np.add(acc[i], self.direction(so1, so2) * self.grav_force(so1, so2) / so1.mass)
            # pos.append(np.array([random.random() - 0.5, random.random() - 0.5, random.random() - 0.5]))
        return acc


class SpaceSprite(pg.sprite.Sprite):
    def __init__(self, space_obj: SpaceObject, container):
        self.space_object = space_obj
        pg.sprite.Sprite.__init__(self, container)
        r = space_obj.radius
        self.image = pg.Surface([2 * r, 2 * r], pg.SRCALPHA, 32)
        self.image.fill((0, 0, 0, 0))
        pg.draw.circle(self.image, space_obj.color, (round(r), round(r)), round(r))
        pg.draw.circle(self.image, space_obj.color.correct_gamma(3.0), (round(r * 0.7), round(r * 0.7)), round(r / 2))

        # TODO: this directly uses the coordinates of the passed SpaceObject. use scaling and zooming and stuff, later.
        self.rect = self.image.get_rect(center=(space_obj.position[0] + WIDTH / 2, space_obj.position[1] + HEIGHT / 2))

    def update(self):
        """ called every time around the game loop.

        """
        # self.rect.move_ip(self.space_object.velocity[0], self.space_object.velocity[1])
        self.rect.left = round(self.space_object.position[0] + WIDTH / 2)
        self.rect.top = round(self.space_object.position[1] + HEIGHT / 2)
        # if self.rect.top <= 0:
        #    self.kill()


class SpaceObjectRenderer:
    """ This contains the methods to render SpaceObject objects, using pygame
    """

    space_objects = []
    all_sprites = pg.sprite.RenderUpdates()
    grav_field = GravitationalField()

    def __init__(self):
        pass

    def print(self):
        for o in self.space_objects:
            s = '{:>10}: Mass: {:6.3e} kg'.format(o.name, o.mass)
            print(s)

    def add(self, new_object: SpaceObject):
        self.space_objects.append(new_object)
        self.grav_field.add(new_object)
        SpaceSprite(new_object, self.all_sprites)

    def update(self):
        a = self.grav_field.accel()
        for so in self.space_objects:
            i = self.space_objects.index(so)
            so.velocity = np.add(so.velocity, np.multiply(a[i], self.grav_field.delta_t))
            so.position = np.add(so.position, np.multiply(so.velocity, self.grav_field.delta_t))
        pass

def main(winstyle=0):
    # Initialize pygame
    # if pg.get_sdl_version()[0] == 2:
    #     pg.mixer.pre_init(44100, 32, 2, 1024)
    pg.init()
    # if pg.mixer and not pg.mixer.get_init():
    #    print("Warning, no sound")
    #    pg.mixer = None

    fullscreen = False
    # Set the display mode
    winstyle = 0  # |FULLSCREEN
    bestdepth = pg.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pg.display.set_mode(SCREENRECT.size, winstyle, bestdepth)

    # decorate the game window
    # icon = pg.transform.scale(Alien.images[0], (32, 32))
    # pg.display.set_icon(icon)
    pg.display.set_caption("Pygame GravSim 1.0.0.0")
    pg.mouse.set_visible(0)

    # create the background, tile the bgd image
    # bgdtile = load_image("background.gif")
    background = pg.Surface(SCREENRECT.size)
    # for x in range(0, SCREENRECT.width, bgdtile.get_width()):
    #    background.blit(bgdtile, (x, 0))
    screen.blit(background, (0, 0))
    pg.display.flip()

    sun = SpaceObject('Sun', 1.234e20)
    sun.position = np.array([0.0, 0.0, 0.0])
    sun.velocity = np.array([-0.4, 0.0, 0.0])
    sun.radius = 30
    sun.mass = MASS_SUN / 1e5              # kg
    sun.color = pg.Color(220, 200, 0)

    earth = SpaceObject('Earth', 5.20e8)
    earth.position = np.array([0.0, 100.0, 0.0])
    earth.velocity = np.array([1.5, 0.0, 0.0])
    earth.color = pg.Color(100, 100, 255)
    earth.mass = MASS_EARTH                   #kg

    moon = SpaceObject('Moon', 5.20e8)
    moon.radius = 5
    moon.position = np.array([0.0, 120.0, 0.0])
    moon.velocity = np.array([2, 0.0, 0.0])
    moon.color = pg.Color(100, 100, 100)
    moon.mass = 1e5                   #kg

    renderer = SpaceObjectRenderer()
    renderer.add(sun)
    renderer.add(earth)
    renderer.add(moon)

    # Create Some Starting Values
    clock = pg.time.Clock()

    # Run our main loop.
    while True:

        # get input
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                return
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_f:
                    if not fullscreen:
                        print("Changing to FULLSCREEN")
                        screen_backup = screen.copy()
                        screen = pg.display.set_mode(
                            SCREENRECT.size, winstyle | pg.FULLSCREEN, bestdepth
                        )
                        screen.blit(screen_backup, (0, 0))
                    else:
                        print("Changing to windowed mode")
                        screen_backup = screen.copy()
                        screen = pg.display.set_mode(
                            SCREENRECT.size, winstyle, bestdepth
                        )
                        screen.blit(screen_backup, (0, 0))
                    pg.display.flip()
                    fullscreen = not fullscreen

        keystate = pg.key.get_pressed()

        # clear/erase the last drawn sprites
        renderer.all_sprites.clear(screen, background)

        # update all the sprites
        renderer.update()
        renderer.all_sprites.update()

        # handle player input
        # direction = keystate[pg.K_RIGHT] - keystate[pg.K_LEFT]
        # player.move(direction)
        # firing = keystate[pg.K_SPACE]
        # if not player.reloading and firing and len(shots) < MAX_SHOTS:
        #    Shot(player.gunpos())
        #    if pg.mixer:
        #        shoot_sound.play()
        # player.reloading = firing

        # Detect collisions between aliens and players.
        # for alien in pg.sprite.spritecollide(player, aliens, 1):

        # See if alien boms hit the player.
        # for bomb in pg.sprite.spritecollide(player, bombs, 1):
        #     if pg.mixer:
        #         boom_sound.play()
        #     Explosion(player)
        #     Explosion(bomb)
        #     player.kill()

        # draw the scene
        dirty = renderer.all_sprites.draw(screen)
        pg.display.update(dirty)

        # cap the framerate at 40fps. Also called 40HZ or 40 times per second.
        clock.tick(40)

    # if pg.mixer:
    #     pg.mixer.music.fadeout(1000)
    pg.time.wait(1000)
    pg.quit()


def main_test():
    sun = SpaceObject('Sun', 1.234e20)
    sun.position = (30.0, 0.0, 0.0)
    earth = SpaceObject('Earth', 5.20e8)
    earth.position = (0.0, 40.0, 0.0)
    renderer = SpaceObjectRenderer()
    renderer.add(sun)
    renderer.add(earth)
    renderer.print()
    # print(distance(sun, earth))


# call the "main" function if running this script
if __name__ == "__main__":
    main()
    # main_test()
