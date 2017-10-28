import pyglet
from time import time


class Pyg2(pyglet.window.Window):
    def __init__(self):
        super(Pyg2, self).__init__(800, 600, fullscreen=False, vsync=False, caption='Pyg2')

        print("Started")

        self.running = True

        # FPS Init
        self.fps_counter = 0
        self.last_fps = time()
        self.fps_text = pyglet.text.Label("FPS: ", str(self.fps_counter), font_size=12, x=10, y=10)

        # pyglet.clock.schedule_interval(self.render(), 1 / 900)


    def __exit__(self):
        self.running = False

    def render(self):
        print("render")
        self.clear()

        self.fps_counter += 1
        if time() - self.last_fps > 1:
            self.fps_text.text = "FPS: " + str(self.fps_counter)
            self.fps_counter = 0
            self.last_fps = time()

        self.fps_text.draw()

    def on_draw(self):
        self.clear()
        self.render()


app = Pyg2()
pyglet.clock.schedule(app.on_draw())


