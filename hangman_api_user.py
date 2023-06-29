import json
import requests
import random
import string
import secrets
import time
import re
import collections

try:
    from urllib.parse import parse_qs, urlencode, urlparse
except ImportError:
    from urlparse import parse_qs, urlparse
    from urllib import urlencode

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from copy import deepcopy
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM, Embedding, Bidirectional
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split


class HangmanAPI(object):
    def __init__(self, access_token=None, session=None, timeout=None,batch_size=1000,epochs=5,test_size=0.33):
        self.hangman_url = self.determine_hangman_url()
        self.access_token = access_token
        self.session = session or requests.Session()
        self.timeout = timeout
        self.guessed_letters = []

        full_dictionary_location = "words_250000_train.txt"
        self.full_dictionary = self.build_dictionary(full_dictionary_location)
        self.full_dictionary_common_letter_sorted = collections.Counter("".join(self.full_dictionary)).most_common()

        self.current_dictionary = []

        self.max_length = 15
        self.test_size = test_size
        self.batch_size = batch_size
        self.epochs = epochs
        self.train_model()

    @staticmethod
    def determine_hangman_url():
        links = ['https://trexsim.com', 'https://sg.trexsim.com']

        data = {link: 0 for link in links}

        for link in links:

            requests.get(link)

            for i in range(10):
                s = time.time()
                requests.get(link)
                data[link] = time.time() - s

        link = sorted(data.items(), key=lambda x: x[1])[0][0]
        link += '/trexsim/hangman'
        return link

    def guess(self, word):

        word=word[::2]

        encoded_word=self.encode_word(word)

        max_len_word=pad_sequences([encoded_word], maxlen=self.max_length, padding='post')

        pred=self.model.predict(max_len_word)

        pred = self.get_order(pred[0])

        for letter in pred:
            if letter not in self.guessed_letters:
                guess_letter = letter
                break
        return guess_letter

    def encode_word(self, word):
        encoded_word = []
        for cha in word:
            if ord(cha) == ord("_"):
                encoded_word.append(27)
            else:
                encoded_word.append(ord(cha)- ord("a")+1)
        return encoded_word

    def get_xy(self):
        encoded_dictionary = []
        for i in self.full_dictionary:
            encoded_dictionary.append(self.encode_word(i))
        X = []
        y = []
        for encoded_word in encoded_dictionary:
            dic = {cha:[] for cha in list(set(encoded_word))}
            for i in range(len(encoded_word)):
                dic[encoded_word[i]].append(i)
            cha_lis = list(dic.keys())
            for cha,lis in dic.items():
                masked_word = deepcopy(encoded_word)

                for pos in lis:
                    masked_word[pos] = 27

                target = cha -1

                X.append(masked_word)
                y.append(target)

                times = 0
                seen = [cha]
                new_masked_word = deepcopy(masked_word)

                while times < len(cha_lis):
                    j = random.randint(0,len(cha_lis)-1)
                    times+=1
                    if cha_lis[j] in seen:
                        continue
                    seen.append(cha_lis[j])
                    for pos in dic[cha_lis[j]]:
                        new_masked_word[pos] = 27

                    X.append(new_masked_word)

                    y.append(target)


        X = pad_sequences(X, maxlen=self.max_length, padding='post')
        y = to_categorical(y, num_classes=26)
        train_x, test_x, train_y, test_y = train_test_split(X, y, test_size=self.test_size, random_state=42)
        return (train_x, test_x, train_y, test_y)



    def train_model(self): # five-layer bidirectional LSTM
        (train_x, test_x, train_y, test_y) = self.get_xy()

        # define the model
        self.model = Sequential()
        self.model.add(Embedding(28, 128, input_length=self.max_length))
        self.model.add(Bidirectional(LSTM(64, return_sequences=True)))
        self.model.add(Bidirectional(LSTM(64, return_sequences=True)))
        self.model.add(Bidirectional(LSTM(64, return_sequences=True)))
        self.model.add(Bidirectional(LSTM(64, return_sequences=True)))
        self.model.add(Bidirectional(LSTM(64)))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(26, activation='softmax'))

        # compile the model
        self.model.compile(optimizer="adam",loss = "categorical_crossentropy", metrics=['accuracy', 'top_k_categorical_accuracy'])

        # summarize the model
        print(self.model.summary())

        # fit and evaluate the model
        self.model.fit(train_x, train_y,
                batch_size=self.batch_size,
                epochs=self.epochs,
                validation_data=[test_x, test_y])

        return

    def get_order(self, prediction):
        dic = {i:prediction[i] for i in range(len(prediction))}
        sorted_cha_list = [chr(index + ord("a")) for index, value in sorted(dic.items(), key=lambda x:x[1],reverse = True)]
        return sorted_cha_list


    def train_model(self): # five-layer bidirectional LSTM
        (train_x, test_x, train_y, test_y) = self.get_xy()

        # define the model
        self.model = Sequential()
        self.model.add(Embedding(28, 128, input_length=self.max_length))
        self.model.add(Bidirectional(LSTM(64, return_sequences=True)))
        self.model.add(Bidirectional(LSTM(64, return_sequences=True)))
        self.model.add(Bidirectional(LSTM(64, return_sequences=True)))
        self.model.add(Bidirectional(LSTM(64, return_sequences=True)))
        self.model.add(Bidirectional(LSTM(64)))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(26, activation='softmax'))

        # compile the model
        self.model.compile(optimizer="adam",loss = "categorical_crossentropy", metrics=['accuracy', 'top_k_categorical_accuracy'])

        # summarize the model
        print(self.model.summary())

        # fit and evaluate the model
        self.model.fit(train_x, train_y,
                batch_size=self.batch_size,
                epochs=self.epochs,
                validation_data=[test_x, test_y])

        return

    def get_order(self, prediction):
        dic = {i:prediction[i] for i in range(len(prediction))}
        sorted_cha_list = [chr(index + ord("a")) for index, value in sorted(dic.items(), key=lambda x:x[1],reverse = True)]
        return sorted_cha_list
