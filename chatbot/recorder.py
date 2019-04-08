"""PyAudio example: Record a few seconds of audio and save to a WAVE file."""
import time
import wave

import pyaudio
import speech_recognition as sr


class SimpleRecorder:
    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        return self.audio_record(*args, **kwargs)

    def audio_record(self, audio_output_filename='output.wav', chunk=1024,
                     f_format=pyaudio.paInt16, channels=1, rate=44100,
                     record_seconds=5):
        p = pyaudio.PyAudio()

        for i in range(3, 0, -1):
            print('recording starting on {}s'.format(i))
            time.sleep(1)

        print("* recording")

        frames = []

        stream = p.open(format=f_format,
                        channels=channels,
                        rate=rate,
                        input=True,
                        frames_per_buffer=chunk)
        for i in range(0, int(rate / chunk * record_seconds)):
            data = stream.read(chunk)
            frames.append(data)

        print("* done recording")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(audio_output_filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(f_format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
        wf.close()
        return audio_output_filename


class FromFileRecorder:
    def __init__(self, file_path):
        self.file_path = file_path

    def __call__(self, *args, **kwargs):
        return self.file_path


class XRecorder:
    """
    Credit: https://github.com/Uberi/speech_recognition/blob/master/examples/microphone_recognition.py
    """
    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        pass

    def recording(self):
        # NOTE: this example requires PyAudio because it uses the Microphone class

        # obtain audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)

        # recognize speech using Sphinx
        try:
            print("Sphinx thinks you said " + r.recognize_sphinx(audio))
        except sr.UnknownValueError:
            print("Sphinx could not understand audio")
        except sr.RequestError as e:
            print("Sphinx error; {0}".format(e))

        # recognize speech using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

        # recognize speech using Google Cloud Speech
        GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""INSERT THE CONTENTS OF THE GOOGLE CLOUD SPEECH JSON CREDENTIALS FILE HERE"""
        try:
            print("Google Cloud Speech thinks you said " + r.recognize_google_cloud(audio,
                                                                                    credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS))
        except sr.UnknownValueError:
            print("Google Cloud Speech could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Cloud Speech service; {0}".format(e))

        # recognize speech using Wit.ai
        WIT_AI_KEY = "INSERT WIT.AI API KEY HERE"  # Wit.ai keys are 32-character uppercase alphanumeric strings
        try:
            print("Wit.ai thinks you said " + r.recognize_wit(audio, key=WIT_AI_KEY))
        except sr.UnknownValueError:
            print("Wit.ai could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Wit.ai service; {0}".format(e))

        # recognize speech using Microsoft Bing Voice Recognition
        BING_KEY = "INSERT BING API KEY HERE"  # Microsoft Bing Voice Recognition API keys 32-character lowercase hexadecimal strings
        try:
            print("Microsoft Bing Voice Recognition thinks you said " + r.recognize_bing(audio, key=BING_KEY))
        except sr.UnknownValueError:
            print("Microsoft Bing Voice Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))

        # recognize speech using Houndify
        HOUNDIFY_CLIENT_ID = "INSERT HOUNDIFY CLIENT ID HERE"  # Houndify client IDs are Base64-encoded strings
        HOUNDIFY_CLIENT_KEY = "INSERT HOUNDIFY CLIENT KEY HERE"  # Houndify client keys are Base64-encoded strings
        try:
            print("Houndify thinks you said " + r.recognize_houndify(audio, client_id=HOUNDIFY_CLIENT_ID,
                                                                     client_key=HOUNDIFY_CLIENT_KEY))
        except sr.UnknownValueError:
            print("Houndify could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Houndify service; {0}".format(e))

        # recognize speech using IBM Speech to Text
        IBM_USERNAME = "INSERT IBM SPEECH TO TEXT USERNAME HERE"  # IBM Speech to Text usernames are strings of the form XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
        IBM_PASSWORD = "INSERT IBM SPEECH TO TEXT PASSWORD HERE"  # IBM Speech to Text passwords are mixed-case alphanumeric strings
        try:
            print("IBM Speech to Text thinks you said " + r.recognize_ibm(audio, username=IBM_USERNAME,
                                                                          password=IBM_PASSWORD))
        except sr.UnknownValueError:
            print("IBM Speech to Text could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from IBM Speech to Text service; {0}".format(e))
