import streamlit as st
from PIL import Image
import numpy as np
import pickle
import requests

# Load API key from secrets file (hidden from users)
DEEPSEEK_API_KEY = st.secrets["DEEPSEEK_API_KEY"]

# Load the saved KMeans model
with open("model.pkl", "rb") as f:
    kmeans = pickle.load(f)

st.title("Interior Design Color Suggester")
st.write("Upload a room image and get decoration suggestions!")

uploaded_file = st.file_uploader("Upload a room image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", width=400)

    # Fit model on new image pixels
    img_array = np.array(image).reshape(-1, 3)
    kmeans.fit(img_array)
    colors = kmeans.cluster_centers_.astype(int)

    # Show dominant colors
    st.subheader("Dominant Colors Found")
    hex_colors = []
    cols = st.columns(len(colors))
    for i, color in enumerate(colors):
        hex_code = "#{:02X}{:02X}{:02X}".format(*color)
        hex_colors.append(hex_code)
        cols[i].markdown(
            f'<div style="background:{hex_code}; height:60px; border-radius:8px;"></div><center>{hex_code}</center>',
            unsafe_allow_html=True
        )

    # Automatically get suggestions when image is uploaded
    st.subheader("Decoration Suggestions")
    with st.spinner("Getting suggestions..."):
        prompt = f"My room has these dominant colors: {', '.join(hex_colors)}. Suggest decoration ideas, furniture style, and wall paint color."

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"},
            json={"model": "llama-3.1-8b-instant", "messages": [{"role": "user", "content": prompt}]}
        )

        response_data = response.json()

        # This will show us what DeepSeek actually returned
        #st.write(response_data)
        result = response.json()["choices"][0]["message"]["content"]
        st.write(result)
        