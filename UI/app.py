from flask import Flask, render_template, request, jsonify
import random
import json
import pickle
import numpy as np
from tensorflow.keras.models import load_model
import nltk
from nltk.stem import WordNetLemmatizer

app = Flask(__name__)

lemmatizer = WordNetLemmatizer()

# Model ve dosyaları yükleyin
intents = json.loads(open('C:/Chatbot/AI/intents.json').read())
words = pickle.load(open('C:/Chatbot/AI/words.pkl', 'rb'))
classes = pickle.load(open('C:/Chatbot/AI/classes.pkl', 'rb'))
model = load_model('C:/Chatbot/AI/chatbot_model.keras')

# Mesajı temizleme fonksiyonu
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# Bag of words fonksiyonu
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

# Modelin sınıf tahmini fonksiyonu
def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]), verbose=0)[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

# Yanıtları alacak fonksiyon
def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['response'])  # Yanıtlar arasından rastgele birini seç
            break
    return result

# Anasayfa (HTML) endpoint'i
@app.route('/')
def home():
    return render_template('index.html')

# Chatbot API endpoint'i
@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_message = request.json['message']  # Kullanıcıdan gelen mesajı al
    ints = predict_class(user_message)  # Sınıf tahmini yap
    response = get_response(ints, intents)  # Yanıtı al
    return jsonify({'response': response})  # Yanıtı döndür

if __name__ == "__main__":
    app.run(debug=True)
