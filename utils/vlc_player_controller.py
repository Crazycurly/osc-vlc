import time
import threading
import vlc

class PlayerController(threading.Thread):
    def __init__(self, video_paths, *args):
        # Initialize the thread
        super().__init__()
        self.video_paths = video_paths  # List of video file paths

        # Initialize VLC instance with additional arguments if provided
        if args:
            self.instance = vlc.Instance(*args)
        else:
            self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()  # Create a new VLC media player

        self.player_state = "exited"  # Initial state of the player
        self.stop_event = threading.Event()  # Event to signal thread to stop
        self.current_video_index = 0  # Index to keep track of the current video

    def run(self):
        # Attach event listener for MediaPlayerEndReached event to handle video completion
        self.player.event_manager().event_attach(
            vlc.EventType.MediaPlayerEndReached, self.on_player_exit)
        # Thread's main loop to keep playing videos until stop_event is set
        while not self.stop_event.is_set():
            if self.player_state == "exited":
                self.play_video()
            time.sleep(0.01)  # Sleep to prevent high CPU usage

    def set_uri(self, uri):
        # Set the media resource locator for the player
        self.uri = uri
        self.player.set_mrl(self.uri)

    def play(self, path=None):
        # Play the media. If a path is provided, set it as the current media
        if path:
            self.set_uri(path)
        return self.player.play()

    def pause(self):
        # Pause the media playback
        self.player.pause()

    def resume(self):
        # Resume the media playback
        self.player.set_pause(0)

    def is_playing(self):
        # Check if the media is currently playing
        return self.player.is_playing()

    def get_time(self):
        # Get the current playback time in milliseconds
        return self.player.get_time()

    def set_time(self, ms):
        # Incorrectly returns the current time instead of setting it. This should set the playback time.
        return self.player.get_time()

    def get_length(self):
        # Get the length of the media in milliseconds
        return self.player.get_length()

    def get_volume(self):
        # Get the current volume （0~100）
        return self.player.audio_get_volume()

    def set_volume(self, volume):
        # Set the playback volume （0~100）
        return self.player.audio_set_volume(volume)

    def get_state(self):
        # Return the current state of the player as a string
        state = self.player.get_state()
        if state == vlc.State.Playing:
            return "Playing"
        elif state == vlc.State.Paused:
            return "Paused"
        elif state == vlc.State.Stopped:
            return "Stopped"
        else:
            return -1  # Indicates an unknown state

    def get_position(self):
        # Get the current playback position as a float ratio (0=start, 1=end) 0.0~1.0
        return self.player.get_position()

    def set_position(self, float_val):
        # Set the playback position as a float ratio (0=start, 1=end) 0.0~1.0
        return self.player.set_position(float_val)

    def get_rate(self):
        # Get the current playback rate
        return self.player.get_rate()

    def set_rate(self, rate):
        # Set the playback rate (speed)
        return self.player.set_rate(rate)

    def set_ratio(self, ratio):
        # Set the video aspect ratio （ex:"16:9","4:3"）
        self.player.video_set_scale(0)  # Disable default scaling, otherwise the aspect ratio won't change
        self.player.video_set_aspect_ratio(ratio)  # Set aspect ratio

    def on_player_exit(self, event):
        # Callback for when the video ends
        print("Player exited")
        self.player_state = "exited"
        # Automatically move to the next video
        self.current_video_index = (self.current_video_index + 1) % len(self.video_paths)

    def play_video(self):
        # Play the current video
        print("Playing video...")
        self.player_state = "playing"
        self.play(self.video_paths[self.current_video_index])

    def play_next(self):
        # Play the next video in the list
        self.current_video_index = (self.current_video_index + 1) % len(self.video_paths)
        self.play_video()

    def play_previous(self):
        # Play the previous video in the list
        self.current_video_index = (self.current_video_index - 1) % len(self.video_paths)
        self.play_video()

    def change_video(self, path):
        # Change the current video path list (this should likely replace the list or modify it, not just assign a single path)
        self.video_paths = path