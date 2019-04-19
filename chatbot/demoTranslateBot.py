import json

from chatbot.bots import TranslateBot, TranslateBotStreaming


def demo_streaming():
    pair = 'en-ko'
    with open('config/{}.json'.format(pair)) as f:
        config = json.load(f)

    bot = TranslateBotStreaming(**config)
    bot(path='x_{}.wav'.format(pair))


def main():
    pair = 'vi-ko'
    with open('config/{}.json'.format(pair)) as f:
        config = json.load(f)

    bot = TranslateBot(**config)
    bot(path='x_{}.wav'.format(pair), asr_from_file=False)


if __name__ == '__main__':
    demo_streaming()
