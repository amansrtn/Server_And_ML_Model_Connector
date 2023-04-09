import json
import numpy as np
from flask import Flask, request
import requests
import pickle
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))
output = "Done sucessfully"


@app.route('/', methods=['GET', 'POST'])
def predict():
    if(request.method == 'POST'):

        global output
        request_data = request.data
        request_data = json.loads(request_data.decode('Utf-8'))
        input_list = request_data['Message']

        MAX_VOCAB_SIZE = 20000
        tokenizer = Tokenizer(num_words=MAX_VOCAB_SIZE)
        tokenizer.fit_on_texts(input_list)
        sequences_test = tokenizer.texts_to_sequences(input_list)
        data_test = pad_sequences(sequences_test, maxlen=24)
        predicted_value = model.predict(data_test)
        output = predicted_value[0]
        if(output > 0.185):
            output = 1
        else:
            output = 0
        return str(output)
    else:
        return str(output)


if __name__ == "__main__":
    app.run()
