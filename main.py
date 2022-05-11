import math
import os
from flask import  Flask, render_template,request, url_for
from keras.models import load_model
import numpy as np
import os
import random
import librosa
import json


app = Flask(__name__)


model = load_model("model/femaleModel.h5")

with open("json/fvoice-comp.json", "r") as fp:
    data = json.load(fp)
    z = np.array(data['mapping'])


@app.route('/')
def loginlanding():
    return render_template('vregi-website/login-landing-page.html')

@app.route('/pred')
def pred():
    return render_template('vregi-website/prediction2.html')

@app.route('/predict',methods=['POST'])
def predict():
    # get audio file
    audio_file = request.files["UploadedAudio"]
    print (audio_file)
    #my_clip = mp.VideoFileClip(r"audio_file")

    with open('static/audio.wav', 'wb') as audio:
        audio_file.save(audio)
    print('file uploaded successfully')
    filename = "static/audio.wav"
    print(filename)

    # make prediction

    SAMPLE_RATE = 44100
    TRACK_DURATION = 3  # measured in seconds
    SAMPLES_PER_TRACK = SAMPLE_RATE * TRACK_DURATION
    num_mfcc = 40
    n_fft = 4096
    hop_length = 512
    num_segments = 6

    samples_per_segment = int(SAMPLES_PER_TRACK / num_segments)
    num_mfcc_vectors_per_segment = math.ceil(samples_per_segment / hop_length)
    signal, sample_rate = librosa.load(filename, sr=SAMPLE_RATE, res_type='kaiser_fast')

    for d in range(num_segments):
        start = samples_per_segment * d
        finish = start + samples_per_segment

    mfccs = librosa.feature.mfcc(signal[start:finish], sample_rate, n_mfcc=num_mfcc, n_fft=n_fft, hop_length=hop_length)
    mfccs = mfccs.T

    mfccs.shape
    mfccs = mfccs[..., np.newaxis]
    print(mfccs.shape)
    mfccs = mfccs[np.newaxis, ...]
    print(mfccs.shape)
    prediction = model.predict(mfccs)
    predicted_index = np.argmax(prediction, axis=1)
    predicted = z[predicted_index]
    predicted_percent = prediction[0, predicted_index]
    predicted = ''.join([str(elem) for elem in predicted])
    predicted_percent = ''.join([str(elem) for elem in predicted_percent])
    output = predicted, ":", predicted_percent
    print("Prediction Summary")
    print(output)
    # 2nd
    prediction1 = prediction
    predicted_index1 = np.argmax(prediction1, axis=1)
    prediction1[0, predicted_index1] = 0
    predicted_index2 = np.argmax(prediction1, axis=1)
    predicted1 = z[predicted_index2]
    predicted_percent1 = prediction1[0, predicted_index2]
    predicted1 = ''.join([str(elem) for elem in predicted1])
    predicted_percent1 = ''.join([str(elem) for elem in predicted_percent1])
    output1 = predicted1, ":", predicted_percent1
    print(predicted1)
    #3rd
    prediction2 = prediction1
    predicted_index2 = np.argmax(prediction2, axis=1)
    prediction2[0, predicted_index2] = 0
    predicted_index3 = np.argmax(prediction2, axis=1)
    predicted2 = z[predicted_index3], ":", prediction1[0, predicted_index3]
    print(predicted2)


    print_message = ' '.join([str(elem) for elem in output])
    print_message2 = ' '.join([str(elem) for elem in output1])



    result = print_message

    # message to be displayed on the html webpage
    prediction_message = predicted
    print(prediction_message)

    # save audio file for html
    #file_name1 = "1"
    #audio_file.save(file_name1 + ".wav")

    return render_template("vregi-website/prediction2-predicted.html", prediction_text=print_message,prediction_text2=print_message2, audiofile="static/audio.wav")
   # return render_template("prediction.html")
if __name__ == '__main__':
    app.run(debug=True)
