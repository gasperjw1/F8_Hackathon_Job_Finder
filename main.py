from flask import Flask, request, abort
from flask_ngrok import run_with_ngrok
from pydub import AudioSegment
import speech_recognition as sr
import os

app = Flask(__name__)


def messengerClipToWavMac(audioFileName):
    file = AudioSegment.from_file('/'+audioFileName, format="mp4")
    output = file.export("/output.wav", format="wav")


def messengerClipToWav(audioFileName):
    file = AudioSegment.from_file('./'+audioFileName, format="mp4")
    output = file.export("./output.wav", format="wav")

def wav2txt(audioFileName):
    reco = sr.Recognizer()
    reco.energy_threshold = 300

    givenAudioFile = sr.AudioFile(audioFileName)

    with givenAudioFile as srcFile:
        givenAudioFile = reco.record(srcFile)

    print(reco.recognize_wit(givenAudioFile, "O7NTCSR3OEK6VZOGW4I65N6P5OTKSI3C"))

    txtFile = open("audioAsText.txt", "w+")
    txtFile.write(reco.recognize_wit(givenAudioFile, "O7NTCSR3OEK6VZOGW4I65N6P5OTKSI3C"))
    txtFile.close()


@app.route('/test')
def webhook():
    VERIFY_TOKEN = "test"
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if mode and token:
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            print("Worked")
            return challenge

    return 'success', 200


@app.route('/test', methods=['POST'])
def handleMessage():
    if request.method == 'POST':
        print(request.json)
        return 'success', 200
    else:
        abort(400)


if __name__ == "__main__":
    app.run()