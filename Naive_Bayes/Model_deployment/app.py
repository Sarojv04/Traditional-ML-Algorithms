import streamlit as st 
import pickle
import string
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()


tfid1 = pickle.load(open('vectorizer.pk1','rb'))
model = pickle.load(open('model.pk1','rb'))

st.title("SMS/Email detection Application")


def data_prepeocessing(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    temp = []

    for i in text:
        if i.isalnum():
            temp.append(i)
    
    text = temp[:]
    temp.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation :
            temp.append(i)
    
    text = temp[:]
    temp.clear()

    for i in text:
        temp.append(ps.stem(i))
        

    return " ".join(temp)

input_sms = st.text_area("Enter the message")

if st.button("Predict"):

    transformed_sms = data_prepeocessing(input_sms)
    vector_input = tfid1.transform([transformed_sms])
    result = model.predict(vector_input)[0]

    if result == 1:
        st.header("Spam")
    else:
        st.header("Not Spam")
