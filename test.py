import time

from utils.vlc_player_controller import PlayerController


# Initialize the player controller with the paths to your videos
video_paths = ["videos/1.mp4", "videos/2.mp4", "videos/3.mp4", "videos/4.mp4", "videos/5.mp4", "videos/6.mp4", "videos/7.mp4", "videos/8.mp4", "videos/9.mp4"]
controller = PlayerController(video_paths)

# Start the player controller thread
controller.start()

time.sleep(3)
controller.play_next()
time.sleep(3)
controller.play_previous()