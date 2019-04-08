from google.cloud.texttospeech_v1.gapic.enums import SsmlVoiceGender

from chatbot.asr import GoogleASR
from chatbot.player import SimplePlayer, PlayerAutostop
from chatbot.recorder import FromFileRecorder, SimpleRecorder
from chatbot.translation import SimpleTranslation
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
        tts = GoogleTTS(voice_gender=SsmlVoiceGender.FEMALE)
        player = SimplePlayer()
        # player = PlayerAutostop()

        audio_file = recorder(audio_output_filename=audio_file, record_seconds=10)
        outputs = asr(audio_file_path=audio_file)
        print(outputs)

        for i, one in enumerate(outputs):
            voice = tts(text=one)
            player(file_path=tts.outfile)
            break  # currently play the best one


class TranslateBot:
    """
    Bot with received input, translate to new language, and TTS
    Use asr, tts, translate google api
    """

    def __init__(self, **kwargs):
        self.config = {
            'asr_lang': kwargs.get('asr_lang', 'en'),
            'tran_source_lang': kwargs.get('asr_lang', 'en'),
            'tran_target_lang': kwargs.get('tran_target_lang', 'ko'),
            'tts_lang': kwargs.get('tts_lang', 'ko-KR'),  # en-US ko-KR
            'tts_gender': kwargs.get('tts_gender', SsmlVoiceGender.FEMALE)
        }

    def __call__(self, *args, **kwargs):
        return self.process(*args, **kwargs)

    def process(self, *args, **kwargs):
        audio_file = kwargs.get('path', '/tmp/84-121123-0001-1.wav')

        recorder = SimpleRecorder()
        # recorder = FromFileRecorder(file_path='/home/hung/tmp/2/84-121123-0001-1.wav')
        asr = GoogleASR()
        tts = GoogleTTS(voice_gender=SsmlVoiceGender.FEMALE)
        player = SimplePlayer()
        # player = PlayerAutostop()

        audio_file = recorder(audio_output_filename=audio_file, record_seconds=10)
        outputs = asr(audio_file_path=audio_file)
        print(outputs)

        translator = SimpleTranslation(source_language=self.config['tran_source_lang'],
                                       target_language=self.config['tran_target_lang'])

        for i, one in enumerate(outputs):
            text = translator(one)
            voice = tts(text=text)
            player(file_path=tts.outfile)
            break  # currently play the best one
