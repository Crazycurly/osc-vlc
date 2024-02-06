import os
import time
from oscpy.server import OSCThreadServer
from utils.vlc_player_controller import PlayerController

osc = OSCThreadServer()
sock = osc.listen(address='0.0.0.0', port=8000, default=True)
run = True

video_paths = ["videos/1.mp4", "videos/2.mp4", "videos/3.mp4", "videos/4.mp4", "videos/5.mp4", "videos/6.mp4", "videos/7.mp4", "videos/8.mp4", "videos/9.mp4"]
controller = PlayerController(video_paths)
controller.set_loop_mode(0)

# Start the player controller thread
controller.start()
controller.play_video()

@osc.address(b'/loop_mode')
def callback(*values):
    print(f"loop : {values}")
    controller.set_loop_mode(int(values[0]))

@osc.address(b'/play')
def callback(*values):
    print(f"play : {values}")
    if values == ():
        controller.play_video()
    else:
        controller.play_video(int(values[0])-1)

@osc.address(b'/pause')
def callback(*values):
    print(f"pause : {values}")
    controller.pause()

@osc.address(b'/resume')
def callback(*values):
    print(f"resume : {values}")
    controller.resume()

@osc.address(b'/next')
def callback(*values):
    print(f"next : {values}")
    controller.play_next()

@osc.address(b'/prev')
def callback(*values):
    print(f"previous : {values}")
    controller.play_previous()

@osc.address(b'/rate')
def callback(*values):
    print(f"rate : {values}")
    controller.set_rate(float(values[0]))

@osc.address(b'/stop')
def callback(*values):
    print(f"stop : {values}")
    controller.stop()

@osc.address(b'/state')
def callback(*values):
    print(f"state : {values}")
    print(controller.get_state())

@osc.address(b'/volume')
def callback(*values):
    print(f"volume : {values}")
    controller.set_volume(int(values[0]))

# quit
@osc.address(b'/quit')
def callback(*values):
    print(f"quit : {values}")
    os._exit(0)

try:
    while run:
        time.sleep(0.01)
except KeyboardInterrupt:
    print("Closing OSC server")
osc.stop()