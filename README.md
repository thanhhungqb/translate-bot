# Information

This is a simple chatbot

This tool use flowing services from Google:

- Google Speech to Text
- Google Translate Api
- Google Text to Speech

You have to register and enable Google Api and get a credentials file to used.

run command:

    python -m chatbot.demoTranslateBot
    
# environment
Tested under Ubuntu 18.04


    export GOOGLE_APPLICATION_CREDENTIALS=...json

# commands
    add-apt-repository ppa:ubuntuhandbook1/audacity
    
    apt-get install portaudio19-dev python-pyaudio python3-pyaudio python3-gi
    
    install [SWIG](https://launchpad.net/ubuntu/bionic/amd64/swig/3.0.10-1.2)
    
    apt install mpg321

# Tools
audacity

# note

http://people.csail.mit.edu/hubert/pyaudio/


# language codes Google API

ASR: English (en-US), Korean (ko-KR?), Vietnamese (vi-VN) 
[ref](https://cloud.google.com/speech-to-text/docs/languages)

Translate: English (en), Korean (ko), Vietnamese (vi)
[ref](https://cloud.google.com/translate/docs/languages)

TTS: English (en-US), Korean (ko-KR)
[ref](https://cloud.google.com/text-to-speech/docs/voices)
