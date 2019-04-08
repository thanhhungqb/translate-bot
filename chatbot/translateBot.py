from chatbot.bots import TranslateBot


def main():
    bot = TranslateBot()
    bot(path='x_translate.wav')


if __name__ == '__main__':
    main()
