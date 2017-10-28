import pyglet

window = pyglet.window.Window()
fps_display = pyglet.clock.ClockDisplay()
# pyglet.clock.set_fps_limit(0)


class RawEventLoop(pyglet.app.EventLoop):

    def idle(self):
        pyglet.clock.tick()
        window.dispatch_event('on_draw')
        window.flip()
        window.invalid = True
        return 0


@window.event
def on_draw():
        window.clear()
        fps_display.draw()


RawEventLoop().run()