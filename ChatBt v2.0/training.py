import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import en_core_web_sm
import json
import random
import pickle
import numpy as np
import devFunc as df

nlp = en_core_web_sm.load()

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD

file_path = 'intents.json'
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

words = []
classes = []
documents = []

for intent in data['intents']:
    for pattern in intent["patterns"]:
        word_list = []
        doc = nlp(pattern)
        for token in doc:
            if token.pos_ != "PUNCT":
                word_list.append(str(token.lemma_))
        words.extend(word_list)
        documents.append((word_list, intent['tag']))
        classes.append(intent['tag'])

words = sorted(set(words))
classes = sorted(set(classes))

pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

training = []
output_empty = [0] * len(classes)

for document in documents:
    bag = []
    word_patterns = document[0]
    for word in words:
        bag.append(word_patterns.count(word))
    df.yukle(bag,document[1])
    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])

random.shuffle(training)
training = np.array(training)

train_x = np.array([item[0] for item in training])
train_y = np.array([item[1] for item in training])

model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(classes), activation='softmax'))


model.compile(
    loss='categorical_crossentropy',
    optimizer=SGD(learning_rate=0.01, decay= 1e-6, momentum=0.9, nesterov=True),
    metrics=['accuracy'],
)

model.fit(
    train_x, train_y,
    epochs=200, batch_size=5, verbose=2
)

model.save("chatbot_model.h5")

print("Done")