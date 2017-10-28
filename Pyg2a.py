import pyglet
import time


def start():

    print("Started")

    self.running = True

    # FPS Init
    self.fps_counter = 0
    self.last_fps = time.time()
    self.fps_text = pyglet.text.Label("FPS: ", str(self.fps_counter), font_size=12, x=10, y=10)

    pyglet.clock.schedule_interval(self.render(), 1 / 900)

def run(self):
    print("Run method")
    while self.running is True:
        self.render()


def __exit__(self):
    self.running = False


def render(self):
    self.clear()

    self.fps_counter += 1
    if time.time() - self.last_fps > 1:
        self.fps_text.text = "FPS: " + str(self.fps_counter)
        self.fps_counter = 0
        self.last_fps = time.time()

    self.fps_text.draw()


