from random import randint
from pyglet.window import key
from time import sleep
import pyglet

# Show FPS
fps = pyglet.clock.ClockDisplay()


class Lives:
    def __init__(self, height, width):
        self.lives = 3

        self.image = pyglet.image.load('resources/heart.jpg')
        self.sprites = []

        for i in range(0, 3):
            sprite = pyglet.sprite.Sprite(self.image)
            sprite.scale = .05
            sprite.y = height - sprite.height - 5
            sprite.x = (width - sprite.width - 5) - i * (sprite.width + 3)
            self.sprites.insert(i, sprite)

    def draw(self):
        for i in range(0, self.lives):
            self.sprites[i].draw()

    def remove_live(self):
        self.lives -= 1

    def get_lives(self):
        return self.lives

    def is_dead(self):
        return self.lives < 1


class Spawner:
    def __init__(self, zombies, height, width):
        self.zombies = zombies
        self.height = height
        self.width = width
        self.spawned = 0
        self.spawntime = 0
        self.lastspawn = 0
        self.next_giant = False
        self.speed = 20
        self.health = 100
        self.reset()

    def reset(self):
        self.spawntime = 5
        self.lastspawn = 0

    def insanity_mode(self):
        self.spawntime = .1
        self.speed = 40

    def killed(self, kills):
        if not kills % 10:
            self.next_giant = True
            print("Next is a giant!")

    def update(self, dt):
        self.lastspawn += dt

        if self.lastspawn > self.spawntime:
            print("Spawned! @", self.spawntime)

            speed = self.speed
            health = self.health

            if self.next_giant:
                speed /= 2
                health *= 4

            zombie = Zombie(speed, health, self.next_giant, self.width, 0)
            zombie.getsprite().y = randint(0, self.height - zombie.getsprite().height)

            if self.next_giant:
                self.next_giant = False

            self.zombies.insert(len(self.zombies), zombie)
            if self.spawntime > 1:
                self.spawntime -= .2
            self.lastspawn = 0


class Collider:
    @staticmethod
    def is_bullet_colliding(prj, target):
        tx1 = target.x
        tx2 = target.x + target.width
        ty1 = target.y
        ty2 = target.y + target.height

        return tx1 < prj.x < tx2 and ty1 < prj.y < ty2


def is_obj_colliding(spr1, spr2):
    # Thank you stackoverflow for this magic function!
    return (spr1.x - spr2.x) ** 2 + (spr1.y - spr2.y) ** 2 < (spr1.width / 2 + spr2.width / 2) ** 2


class Bullet:
    def __init__(self, x, y):
        self.sprite = pyglet.sprite.Sprite(pyglet.image.load('resources/carrot.png'))
        self.sprite.x = x
        self.sprite.y = y
        self.sprite.scale = .1

    def draw(self):
        self.sprite.draw()

    def getsprite(self):
        return self.sprite

    def getx(self) -> pyglet.sprite.Sprite:
        return self.sprite.x

    def update(self, dt):
        self.sprite.x += 300 * dt


class Background:
    def __init__(self):
        self.background = pyglet.resource.image('resources/darkgrass.png')

    def draw(self):
        self.background.blit(0, 0)


class Zombie:
    def __init__(self, speed, lives, giant, x, y):
        if giant:
            src = 'resources/policeman.gif'
        else:
            src = 'resources/zombie1.gif'
        animation = pyglet.resource.animation(src)
        self.sprite = pyglet.sprite.Sprite(animation)
        self.sprite.scale = .4

        self.sprite.x = x
        self.sprite.y = y

        self.speed = speed
        self.lives = lives

    def draw(self):
        self.sprite.draw()

    def update(self, dt):
        self.sprite.x -= self.speed * dt

    def getsprite(self):
        return self.sprite

    def shot(self):
        self.lives -= randint(40, 70)
        if self.lives < 0:
            return True
        return False


class Mary:
    def __init__(self, height):
        self.sprite = pyglet.sprite.Sprite(pyglet.image.load('resources/mary.png'))
        self.sprite.x = 150
        self.sprite.y = randint(0, height)

    def draw(self):
        self.sprite.draw()

    def getsprite(self):
        return self.sprite


# The game window
class Window(pyglet.window.Window):
    def __init__(self):
        super(Window, self).__init__(vsync=False)
        self.maxfps = 60
        pyglet.clock.schedule(self.update)
        pyglet.clock.set_fps_limit(self.maxfps)

        self.set_caption("Zombie Mania")  # Insert pretty cool name here!

        # This block is for predefined labels like score and pause message.
        self.score_label = pyglet.text.Label(text="Kills: 0", x=10, y=self.height - 20)
        self.paused_text = pyglet.text.Label(bold=True, font_size=20, text="PAUSED", y=self.height / 2)
        self.paused_text.x = self.width / 2 - self.paused_text.content_width / 2

        self.kills = 0  # People like scores
        self.lastshot = 0  # Make sure the gun isn't some sort of insane weapon

        # A whole bunch of array's for storing multiple sprites.
        self.pressed_keys = []
        self.bullets = []
        self.zombies = []

        # A game without mary and no background isn't a real game.
        self.mymary = Mary(self.height)
        self.background = Background()
        self.paused = False

        # Live(s) manager
        self.lives = Lives(self.height, self.width)

        # This block is for messages like: 'The boss is incoming', 'Good work' etc..
        self.message_timeout = 0
        self.message_text = pyglet.text.Label(bold=True, font_size=20, text="INSERT TEXT", y=self.height / 2)

        # Spawner is the sprite generator
        self.spawner = Spawner(self.zombies, self.height, self.width)

    # You need the dt argument there to prevent errors,
    # it does nothing as far as I know. Just a bit of counting up!
    def update(self, dt):
        if self.paused:
            sleep(.1)  # Why waste CPU time on a game that is paused?
            return  # Make sure the rest of the update doesn't get run

        self.lastshot += dt  # Only allow shooting every .x seconds
        marry = self.mymary.getsprite()  # A bit easier than calling self.mymarry.getsprite the whole time.

        self.move_marry(marry, dt)  # A bit of marry moving
        self.keep_marry_in_screen(marry)  # Make sure marry doesn't go missing.

        self.spawner.update(dt)  # Let's tick the spawner

        self.message_timeout -= dt

        # WIP - Mary & Zombie colliding test
        for z in self.zombies:
            if is_obj_colliding(z.getsprite(), self.mymary.getsprite()):
                self.reset()

        if key.SPACE in self.pressed_keys:  # It looks like the player would like to shoot
            if self.lastshot > .3:  # The gun ain't some kind of laser
                self.bullets.insert(len(self.bullets), Bullet(marry.x + 40, marry.y + 30))  # Let's actually shoot!
                self.lastshot = 0  # Reset the shot timer.

        for z in self.zombies:  # Loop trough all zombies
            z.update(dt)  # Make sure all zombies also move. Would be a bit boring otherwise?

        for b in list(self.bullets):  # Loop trough all bullets
            if b.getx() > self.width:  # If the bullet is no longer inside the screen
                self.bullets.remove(b)  # Remove bullets that are no longer visible
            b.update(dt)  # Move the bullets passing the dt

            for z in list(self.zombies):  # Loop trough the zombies
                if Collider().is_bullet_colliding(b.getsprite(), z.getsprite()):
                    if z.shot():  # Returns true if the zombie has been killed
                        self.zombies.remove(z)  # Zombie has been killed let's remote it.
                        self.kills += 1  # Let's give the player a point!
                        self.spawner.killed(self.kills)  # Let the spawner know a zombie has been killed :)
                    if b in self.bullets:  # Sometimes the bullet already has been removed so just a quick check
                        self.bullets.remove(b)  # Remove the bullet if it's still in the game.
        pass

    def show_message(self, text, time):
        self.message_timeout = time
        self.message_text.text = text
        self.message_text.x = self.width / 2 - self.paused_text.content_width / 2

    def draw_message(self):
        if self.message_timeout < 0:
            return

    def reset(self):
        self.zombies = []
        self.bullets = []
        self.lives.remove_live()

        self.spawner = Spawner(self.zombies, self.height, self.width)

        self.spawner.reset()

    def move_marry(self, marry, dt):
        # Make sure that walking with an angle is the same speed. We're a retro game duhh
        steps = 150
        if self.pressedmovekeys() > 1:
            steps = steps / 1.5
        steps *= dt

        if key.LEFT in self.pressed_keys:
            marry.x -= steps
        if key.RIGHT in self.pressed_keys:
            marry.x += steps
        if key.DOWN in self.pressed_keys:
            marry.y -= steps
        if key.UP in self.pressed_keys:
            marry.y += steps

    def keep_marry_in_screen(self, marry):
        if marry.y < 0:
            marry.y = 0
        if marry.x < 0:
            marry.x = 0

        if marry.y + marry.height > self.height:
            marry.y = self.height - marry.height
        if marry.x + marry.width > self.width:
            marry.x = self.width - marry.width

    # Return the amount of move keys pressed
    def pressedmovekeys(self):
        keys = 0
        if key.LEFT in self.pressed_keys:
            keys += 1
        if key.RIGHT in self.pressed_keys:
            keys += 1
        if key.DOWN in self.pressed_keys:
            keys += 1
        if key.UP in self.pressed_keys:
            keys += 1
        return keys

    def on_draw(self):
        pyglet.clock.tick()  # Make sure you tick o'l the clock!
        self.clear()
        self.background.draw()
        self.mymary.draw()
        self.mymary.getsprite()

        self.score_label.text = "Kills: %s" % self.kills
        self.score_label.draw()

        if self.paused:
            self.paused_text.draw()

        if self.lives.is_dead():
            dead = pyglet.text.Label(bold=True, font_size=20, text="YOU HAVE DIED", y=self.height / 2)
            dead.x = (self.width / 2) - (dead.content_width / 2)
            dead.draw()

        for b in self.bullets:
            b.draw()
        for z in self.zombies:
            z.draw()

        self.lives.draw()
        fps.draw()

    def draw_border(self, spr1):
        melon = pyglet.image.load('resources/melon.png')
        ld = pyglet.sprite.Sprite(melon)
        ld.scale = .05
        ld.x = spr1.x
        ld.y = spr1.y
        ld.draw()

        rd = pyglet.sprite.Sprite(melon)
        rd.scale = .05
        rd.x = spr1.x + spr1.width
        rd.y = spr1.y
        rd.draw()

        lu = pyglet.sprite.Sprite(melon)
        lu.scale = .05
        lu.x = spr1.x
        lu.y = spr1.y + spr1.height
        lu.draw()

        ru = pyglet.sprite.Sprite(melon)
        ru.scale = .05
        ru.x = spr1.x + spr1.width
        ru.y = spr1.y + spr1.height
        ru.draw()

        ce = pyglet.sprite.Sprite(melon)
        ce.scale = .05
        ce.x = spr1.x + (spr1.width / 2)
        ce.y = spr1.y + (spr1.height / 2)
        ce.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol in self.pressed_keys:
            return

        if symbol is key.H:
            self.lives.remove_live()

        if symbol is key.P:
            self.paused = not self.paused
            if self.paused:
                pyglet.clock.set_fps_limit(20)
            else:
                pyglet.clock.set_fps_limit(self.maxfps)

        if key.J in self.pressed_keys:
            if key.I is symbol:
                self.spawner.insanity_mode()

        self.pressed_keys.append(symbol)

    def on_key_release(self, symbol, modifiers):
        if symbol in self.pressed_keys:
            self.pressed_keys.remove(symbol)


# Create a window and run
win = Window()
pyglet.app.run()
