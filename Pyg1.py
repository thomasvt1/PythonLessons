from random import randint
import pyglet, time

window = pyglet.window.Window()

marryList = []

fps_counter = 0
last_fps = time()
fps_text = pyglet.text.Label("FPS: ", str(fps_counter), font_size=12, x=10,y=10)


label = pyglet.text.Label('Experience tranquillity',
                          font_name='Times New Roman',
                          font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')

for x in range(1, 60):
    sprite = pyglet.sprite.Sprite(pyglet.image.load('resources/mary.png'))
    sprite.x = randint(50, 600)
    sprite.y = randint(50, 500)
    sprite.rotation = randint(0, 360)
    marryList.insert(len(marryList), sprite)


def loop(value):
    #print("I'm in a loop...")
    label.draw()


    for mary in marryList:
        mary.draw()

    i = True
    for mary in marryList:
        if i:
            mary.rotation = mary.rotation + 3
        else:
            mary.rotation = mary.rotation - 3
        i = not i


@window.event
def on_draw():
    window.clear()
    loop(None)


pyglet.clock.schedule_interval(loop, 1/900)
pyglet.app.run()
