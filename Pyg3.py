from random import randint
from pyglet.window import key
#from pyglet import clock
import pyglet

# Show FPS
fps = pyglet.clock.ClockDisplay()

class Spawner:
    def __init__(self, zombies):
        self.zombies = zombies

class Collider:
    def is_colliding(self, prj, target):
        tx1 = target.x
        tx2 = target.x + target.width
        ty1 = target.y
        ty2 = target.y + target.height

        return tx1 < prj.x < tx2 and ty1 < prj.y < ty2


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

    def update(self):
        self.sprite.x += 2

    def spawn(self):
        print("TODO: Spawn")


class Background:
    def __init__(self):
        self.background = pyglet.resource.image('resources/grass.jpg')

    def draw(self):
        self.background.blit(0, 0)


class Zombie:
    def __init__(self, random):
        animation = pyglet.resource.animation('resources/zombie1.gif')
        self.sprite = pyglet.sprite.Sprite(animation)
        self.sprite.scale = .3

        if random is True:
            self.sprite.x = randint(200, 500)
            self.sprite.y = randint(50, 300)
        # marryList.insert(len(marryList), sprite)

    def draw(self):
        self.sprite.draw()

    def getsprite(self):
        return self.sprite


class Mary:
    def __init__(self, random):
        self.sprite = pyglet.sprite.Sprite(pyglet.image.load('resources/mary.png'))
        if random is True:
            self.sprite.x = randint(50, 600)
            self.sprite.y = randint(50, 500)
        # marryList.insert(len(marryList), sprite)

    def draw(self):
        self.sprite.draw()

    def getsprite(self):
        return self.sprite


# The game window
class Window(pyglet.window.Window):
    def __init__(self):
        super(Window, self).__init__(vsync=False)
        pyglet.clock.schedule(self.update)
        pyglet.clock.set_fps_limit(60)

        self.lastshot = 0
        self.pressed_keys = []
        self.bullets = []
        self.zombies = []
        self.mymary = Mary(True)
        self.zombie = Zombie(True)
        self.background = Background()

    # You need the dt argument there to prevent errors,
    # it does nothing as far as I know. Just a bit of counting up!
    def update(self, dt):
        self.lastshot += dt  # Only allow shooting every .x seconds
        marry = self.mymary.getsprite()

        self.move_marry(marry, dt)
        self.keep_marry_in_screen(marry)

        if key.SPACE in self.pressed_keys:
            if self.lastshot > .5:
                self.bullets.insert(len(self.bullets), Bullet(marry.x + 40, marry.y + 30))
                self.lastshot = 0

        for b in list(self.bullets):
            if b.getx() > self.width:
                self.bullets.remove(b)
            b.update()

            if Collider.is_colliding(self, b.getsprite(), self.zombie.getsprite()):
                print("Collide!")
                self.bullets.remove(b)
        pass

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
        fps.draw()
        self.mymary.draw()
        self.mymary.getsprite()
        self.zombie.draw()

        #self.drawborder(self.zombie.getsprite())

        for b in self.bullets:
            b.draw()
        for z in self.zombies:
            z.draw()

    def drawborder(self, spr1):
        melon = pyglet.image.load('resources/melon.png')
        ld = pyglet.sprite.Sprite(melon)
        ld.scale = .05
        ld.x = self.zombie.getsprite().x
        ld.y = self.zombie.getsprite().y
        ld.draw()

        rd = pyglet.sprite.Sprite(melon)
        rd.scale = .05
        rd.x = self.zombie.getsprite().x + spr1.width
        rd.y = self.zombie.getsprite().y
        rd.draw()

        lu = pyglet.sprite.Sprite(melon)
        lu.scale = .05
        lu.x = self.zombie.getsprite().x
        lu.y = self.zombie.getsprite().y + spr1.height
        lu.draw()

        ru = pyglet.sprite.Sprite(melon)
        ru.scale = .05
        ru.x = self.zombie.getsprite().x + spr1.width
        ru.y = self.zombie.getsprite().y + spr1.height
        ru.draw()

        ce = pyglet.sprite.Sprite(melon)
        ce.scale = .05
        ce.x = self.zombie.getsprite().x + (spr1.width / 2)
        ce.y = self.zombie.getsprite().y + (spr1.height / 2)
        ce.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol in self.pressed_keys:
            return
        self.pressed_keys.append(symbol)

    def on_key_release(self, symbol, modifiers):
        if symbol in self.pressed_keys:
            self.pressed_keys.remove(symbol)


# Create a window and run
win = Window()
pyglet.app.run()
