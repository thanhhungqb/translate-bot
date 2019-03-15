import io

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types


def asr_google_api(audio_file_path):
    """

    :param audio_file_path: must be mono channel
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
        language_code='en-US')

    # Detects speech in the audio file
    response = client.recognize(config, audio)

    outputs = []
    for result in response.results:
        print('Transcript: {}'.format(result.alternatives[0].transcript))
        outputs.append(result.alternatives[0].transcript)

    return outputs


if __name__ == '__main__':
    asr_google_api('/home/hung/tmp/2/84-121123-0001-1.wav')
