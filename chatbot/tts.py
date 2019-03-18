import tempfile

from google.cloud import texttospeech


class GoogleTTS:
    def __init__(self, **kwargs):
        self.ssml_gender = kwargs.get('voice_gender', texttospeech.enums.SsmlVoiceGender.MALE)
        self.audio_encoding = kwargs.get('audio_encoding', texttospeech.enums.AudioEncoding.MP3)
        self.outfile = None

    def __call__(self, text="this is test", outfile=None, *args, **kwargs):
        return self.process(text=text, outfile=outfile, *args, **kwargs)

    def process(self, text="this is test", outfile=None, *args, **kwargs):
        """Synthesizes speech from the input string of text or ssml.
        credit: https://cloud.google.com/text-to-speech/docs/quickstart-client-libraries#client-libraries-install-python
        Note: ssml must be well-formed according to:
            https://www.w3.org/TR/speech-synthesis/
        """

        # Instantiates a client
        client = texttospeech.TextToSpeechClient()

        # Set the text input to be synthesized
        synthesis_input = texttospeech.types.SynthesisInput(text=text)

        # Build the voice request, select the language code ("en-US")
        voice = texttospeech.types.VoiceSelectionParams(language_code='en-US', ssml_gender=self.ssml_gender)

        # Select the type of audio file you want returned
        audio_config = texttospeech.types.AudioConfig(audio_encoding=self.audio_encoding)

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = client.synthesize_speech(synthesis_input, voice, audio_config)

        # The response's audio_content is binary.
        if outfile is None:
            """create on /tmp and play directly"""
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as out:
                out.write(response.audio_content)
                self.outfile = out.name
        else:
            with open(outfile, 'wb') as out:
                out.write(response.audio_content)
                print('Audio content written to file {}'.format(outfile))
            self.outfile = outfile

        return response.audio_content
