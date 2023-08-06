import speech_recognition as sr
import argparse


def audioToText(n):
    filename = n
    # initialize the recognizer
    r = sr.Recognizer()
    # open the file
    with sr.AudioFile(filename) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data)
        print(text)


# =================================================================
# Arg parsing
def main():
    parser = argparse.ArgumentParser(prog='gfg',
                                     description='This a voice modem testing script.')

    parser.add_argument('-file', default=False, help="Provide audio file name to convert to text", required=True)

    args = parser.parse_args()
    n = args.file

    if args.file:
        audioToText(n)


if __name__ == "__main__":
    main()
