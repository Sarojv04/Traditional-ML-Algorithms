import streamlit as st
import pickle
import string
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer
import os

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')

st.set_page_config(
    page_title="Spam Detector",
    page_icon="📧",
    layout="centered"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        font-size: 18px;
        border-radius: 10px;
        width: 100%;
        padding: 10px;
    }
    .result-spam {
        background-color: #ff4b4b;
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 24px;
    }
    .result-safe {
        background-color: #00c853;
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 24px;
    }
    </style>
""", unsafe_allow_html=True)

ps = PorterStemmer()

BASE_DIR = os.path.dirname(__file__)
tfid1 = pickle.load(open(os.path.join(BASE_DIR, 'vectorizer.pk1'), 'rb'))
model = pickle.load(open(os.path.join(BASE_DIR, 'model.pk1'), 'rb'))

# Header
st.markdown("# 📧 SMS/Email Spam Detector")
st.markdown("##### Detect whether a message is **Spam** or **Not Spam** instantly!")
st.divider()

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
        if i not in stopwords.words('english') and i not in string.punctuation:
            temp.append(i)
    text = temp[:]
    temp.clear()
    for i in text:
        temp.append(ps.stem(i))
    return " ".join(temp)

input_sms = st.text_area("✉️ Enter your message here:", height=150, 
                          placeholder="Type or paste your SMS/Email message...")

if st.button("🔍 Predict"):
    if input_sms.strip() == "":
        st.warning("⚠️ Please enter a message first!")
    else:
        with st.spinner("Analyzing message..."):
            transformed_sms = data_prepeocessing(input_sms)
            vector_input = tfid1.transform([transformed_sms])
            result = model.predict(vector_input)[0]

        if result == 1:
            st.markdown('<div class="result-spam">🚨 SPAM MESSAGE DETECTED!</div>', 
                       unsafe_allow_html=True)
        else:
            st.markdown('<div class="result-safe">✅ This message looks SAFE!</div>', 
                       unsafe_allow_html=True)

st.divider()
st.markdown("<center>Made with ❤️ using Streamlit & Naive Bayes</center>", 
            unsafe_allow_html=True)