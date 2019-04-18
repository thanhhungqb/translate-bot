import io

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

from chatbot.recorder import StreamingRecorder


class GoogleASR:
    def __init__(self, language_code='en-US', **kwargs):
        self.language_code = language_code

    def __call__(self, *args, **kwargs):
        return self.process(*args, **kwargs)

    def process(self, audio_file_path=None, *args, **kwargs):
        """
        process single-channel voice signal and return text
        :param args:
        :param kwargs:
        :return:
        """
        # Instantiates a client
        client = speech.SpeechClient()

        # Loads the audio into memory
        with io.open(audio_file_path, 'rb') as audio_file:
            content = audio_file.read()
            audio = types.RecognitionAudio(content=content)

        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            # sample_rate_hertz=44100,
            language_code=self.language_code)

        # Detects speech in the audio file
        response = client.recognize(config, audio)

        outputs = []
        for result in response.results:
            print('Transcript: {}'.format(result.alternatives[0].transcript))
            outputs.append(result.alternatives[0].transcript)

        return outputs


class GoogleStreamASR:
    """
    Credit: Google example
    """

    def __init__(self, language_code='en-US', max_length_sec=60,
                 rate=44100, **kwargs):
        self.language_code = language_code
        self.max_length_sec = max_length_sec
        self.rate = rate
        self.recorder = StreamingRecorder(self.max_length_sec, rate=self.rate)

    def __call__(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return: iterator of data text
        """
        client = speech.SpeechClient()

        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=self.rate,
            language_code=self.language_code)
        streaming_config = types.StreamingRecognitionConfig(config=config)

        requests = (types.StreamingRecognizeRequest(audio_content=chunk) for chunk in self.recorder())
        responses = client.streaming_recognize(streaming_config, requests)

        for response in responses:
            if self.recorder.is_stopped:
                raise StopIteration

            yield response.results

        raise StopIteration

    def destroy(self):
        self.recorder.stop()
