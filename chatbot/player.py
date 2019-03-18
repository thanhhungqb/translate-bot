import time

from playsound import playsound
from pygame import mixer, sndarray


class SimplePlayer:
    def __init__(self):
        mixer.init()

    def __call__(self, *args, **kwargs):
        self.play(*args, **kwargs)

    def play(self, *args, **kwargs):
        file_path = kwargs.get('file_path', '/tmp/0.mp3')
        mixer.music.load(file_path)
        mixer.music.play()
        time.sleep(5)


class PlayerAutostop:
    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        self.play(*args, **kwargs)

    def play(self, *args, **kwargs):
        file_path = kwargs.get('file_path', '/tmp/0.mp3')
        playsound(file_path)


def play_sound(x=None):
    fs = 8000  # Hz
    mixer.init()

    mixer.pre_init(fs, size=-16, channels=1)
    mixer.init()
    sound = sndarray.make_sound(x)

    sound.play()

    time.sleep(10)  # NOTE: Since sound playback is async, allow sound playback to start before Python exits


def play_sound1(x=None):
    import sounddevice
    import time

    fs = 8000
    sounddevice.play(x, fs)  # releases GIL
    time.sleep(1)  # NOTE: Since sound playback is async, allow sound playback to finish before Python exits


def play_sound2(file_path):
    mixer.init()
    s = mixer.Sound(file_path)
    s.play()
