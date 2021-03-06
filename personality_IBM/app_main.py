from flask  import Flask,request,jsonify
from model import Model
import tensorflow as tf
import keras
from gensim.corpora import Dictionary
#import tensorflow_core.keras
from prediction_class import models
from prediction import Predictor_cat5,mbti_models
app=Flask(__name__)
Predictor_cat5_obj,mbti_models_obj=Predictor_cat5(),mbti_models()
model=Model()
models =models()
import pickle
import re
import pandas as pd
model=pickle.load(open('glove_model.pickle','rb'))
df=pd.read_csv('Emotion_Lexicon.csv')
word_list=df.Words.values


@app.route('/',methods=['POST'])
def test():
    probablity={}
    if request.method=='POST':
        json_data=request.json
        text=json_data['text']
        text1=re.sub('[\W\d]',' ',text).strip().split()
        res = len(text1)
        print(res)
        if res > 50:
            global models
            prediction1,probablity1,prediction_text=models.predict([text])
            cat5_probablity=Predictor_cat5_obj.predict([text])
            mbti_probablity=mbti_models_obj.predict([text])
            probablity.update(cat5_probablity)
            probablity.update(mbti_probablity)
            main_json = {'probablities':str(probablity),'prediction1':prediction1}
            return jsonify(main_json)
        else:
            return str("Please provide more data")
                

@app.route('/word',methods=['POST'])
def count_word():
    if request.method=='POST':
        print("@@@@@@@@")
        json_data=request.json
        text=json_data['text']
        global word_list
        words,emotion_lexicon=set(),set()
        text=re.sub('[\W\d]',' ',text).strip().split()
        res = len(text) 
        for word in text:
            try:
                if len(model.get_vector(word)) >0:
                    words.add(word)
                if word in word_list:
                    emotion_lexicon.add(word)
            except KeyError:
                return('Not found word : ' ,word)
            words =dict.fromkeys(words, 0)
            emotion_lexicon = dict.fromkeys(emotion_lexicon, 0) 
            try:
                if res > 1000:
                    main_json_1 = {'word_lenght': res,'emotion_lexicon':emotion_lexicon}
                return jsonify(main_json_1)
            except KeyError:
                return "Please provide more data"
                
if __name__=='__main__':
    app.run(debug=True,port=5001)