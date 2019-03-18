from chatbot.asr import GoogleASR
from chatbot.player import SimplePlayer, PlayerAutostop
from chatbot.recorder import FromFileRecorder, SimpleRecorder
from chatbot.tts import GoogleTTS


class SimpleBot:
    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        return self.process(*args, **kwargs)

    def process(self, *args, **kwargs):
        audio_file = kwargs.get('path', '/tmp/84-121123-0001-1.wav')

        recorder = SimpleRecorder()
        # recorder = FromFileRecorder(file_path='/home/hung/tmp/2/84-121123-0001-1.wav')
        asr = GoogleASR()
        tts = GoogleTTS(voice_gender=1)
        player = SimplePlayer()
        # player = PlayerAutostop()

        audio_file = recorder(audio_output_filename=audio_file, record_seconds=10)
        outputs = asr(audio_file_path=audio_file)
        print(outputs)

        for i, one in enumerate(outputs):
            voice = tts(text=one)
            player(file_path=tts.outfile)
            break  # currently play the best one
