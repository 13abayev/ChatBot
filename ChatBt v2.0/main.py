import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import en_core_web_sm
import random
import json
import pickle
import numpy as np

nlp = en_core_web_sm.load()
from tensorflow.keras.models import load_model

file_path = 'intents.json'
with open(file_path, 'r', encoding='utf-8') as file:
    intents = json.load(file)

words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))
model = load_model('chatbot_model.h5')

def cleaning(message):
    word_list = []
    for token in nlp(message):
        if token.pos != "PUNCT":
            word_list.append(str(token.lemma_))
    return word_list

def bag_of_words(message):
    sentence_words = cleaning(message)
    bag = [0] * len(words)

    for w in sentence_words:
        for i, word in enumerate(words):
            if w == word:
                bag[i] += 1
                break
    return np.array(bag)

def predict_class (message):
    bow = bag_of_words(message)
    res = model.predict(np.array([bow]))[0]
    dismiss = 0.25
    result = [[i, r] for i, r in enumerate(res) if r > dismiss]

    result.sort(key = lambda x : x[1], reverse = True)

    return result[0]

def get_response(res):
    tag = classes[res[0]]
    lst = intents["intents"]

    for i in lst:
        if i["tag"] == tag:
            return random.choice(i['responses'])


while True:
    print("Bot : " + get_response(predict_class(input("You : "))))