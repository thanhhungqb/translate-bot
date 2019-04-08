from google.cloud import translate


class SimpleTranslation:
    def __init__(self, source_language='en', target_language='ko'):
        """ language: en, ko, vi"""
        self.source_language = source_language
        self.target_language = target_language

    def __call__(self, sentence, *args, **kwargs):
        return self.process_translate(text=sentence, *args, **kwargs)

    def process_translate(self, text, *args, **kwargs):
        # from: https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/translate/cloud-client

        # Instantiates a client
        translate_client = translate.Client()
        source_lang = kwargs.get('source_language', self.source_language)
        target_lang = kwargs.get('target_language', self.target_language)

        # The text to translate
        # text = u'Hello, world!'
        # text = u'Sentiment Analysis using out of core learning!'

        # Translates some text into Russian
        translation = translate_client.translate(
            text,
            source_language=source_lang,
            target_language=target_lang)

        print(u'Text: {}'.format(text))
        print(u'Translation: {}'.format(translation['translatedText']))

        return translation['translatedText']
