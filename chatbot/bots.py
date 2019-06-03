from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from google.cloud.texttospeech_v1.gapic.enums import SsmlVoiceGender

from chatbot.asr import GoogleASR, GoogleStreamASR
from chatbot.player import SimplePlayer
from chatbot.recorder import FromFileRecorder, SimpleRecorder, StreamingRecorder
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
            'tran_source_lang': kwargs.get('tran_source_lang', 'en'),
            'tran_target_lang': kwargs.get('tran_target_lang', 'ko'),
            'tts_lang': kwargs.get('tts_lang', 'ko-KR'),  # en-US ko-KR
            'tts_gender': kwargs.get('tts_gender', SsmlVoiceGender.FEMALE)
        }

    def __call__(self, *args, **kwargs):
        return self.process(*args, **kwargs)

    def process(self, *args, **kwargs):
        audio_file = kwargs.get('path', '/tmp/84-121123-0001-1.wav')

        recorder = SimpleRecorder()
        if kwargs.get('asr_from_file', False):
            # for testing only with voice from file
            recorder = FromFileRecorder(file_path=audio_file)

        asr = GoogleASR(language_code=self.config['asr_lang'])
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


class TranslateBotStreaming:
    """
    Bot with received input, translate to new language, and TTS
    Use asr, tts, translate google api
    """

    def __init__(self, **kwargs):
        self.config = {
            'asr_lang': kwargs.get('asr_lang', 'en'),
            'tran_source_lang': kwargs.get('tran_source_lang', 'en'),
            'tran_target_lang': kwargs.get('tran_target_lang', 'ko'),
            'tts_lang': kwargs.get('tts_lang', 'ko-KR'),  # en-US ko-KR
            'tts_gender': kwargs.get('tts_gender', SsmlVoiceGender.FEMALE)
        }

    def __call__(self, *args, **kwargs):
        return self.process(*args, **kwargs)

    def process(self, *args, **kwargs):

        tts = GoogleTTS(voice_gender=self.config['tts_gender'])
        player = SimplePlayer()

        translator = SimpleTranslation(source_language=self.config['tran_source_lang'],
                                       target_language=self.config['tran_target_lang'])

        while True:
            gsasr = GoogleStreamASR(language_code=self.config['asr_lang'])
            for results in gsasr():
                print(results)
                for result in results:
                    print('Finished: {}'.format(result.is_final))
                    print('Stability: {}'.format(result.stability))
                    alternatives = result.alternatives
                    # The alternatives are ordered from most likely to least.
                    for alternative in alternatives:
                        print('Confidence: {}'.format(alternative.confidence))
                        print(u'Transcript: {}'.format(alternative.transcript))
                        transcript = alternative.transcript

                        if transcript.upper().strip() == 'STOP':
                            return None

                        text = translator(transcript)
                        tts(text=text)
                        player(file_path=tts.outfile)
                        # TODO stop gsasr and continue while
                        # gsasr.destroy()
                        break
