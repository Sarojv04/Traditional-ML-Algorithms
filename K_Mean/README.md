# Interior Design Color Suggester

🔗 **Try it here:** [Live App](https://traditional-ml-algorithms-boah7yuqsn4v6ycxzb5rua.streamlit.app/)

---

I built this project while learning K-Means Clustering. The idea came to me when I thought — what if we could look at a room photo and figure out what colors are in it, then use that to suggest how to decorate it?

So that's exactly what this does. You upload a photo of your room, the model picks out the most dominant colors, and then AI tells you what furniture, paint, and decoration would look good based on those colors.

---

## How to use it

Just go to the link above, upload any room image, and wait a few seconds. That's it. No sign up, no API key needed from your side.

---

## What's happening behind the scenes

When you upload an image, every pixel in that image has 3 color values (Red, Green, Blue). K-Means groups all those pixels into clusters and finds the center of each cluster — those centers are your dominant colors.

Once we have those colors, we send them to an AI model which looks at them and suggests decoration ideas that would match or complement those colors.

---

## Tech used

- Python
- Scikit-learn for K-Means
- Pillow for reading the image
- Streamlit for the web app
- Groq API for the AI suggestions

---

## Run it locally

```bash
git clone https://github.com/Sarojv04/Traditional-ML-Algorithms.git
cd Traditional-ML-Algorithms/K_Mean
pip install -r requirements.txt
streamlit run app.py
```

You will need a free Groq API key from [console.groq.com](https://console.groq.com). Create a file `.streamlit/secrets.toml` and add:

```toml
DEEPSEEK_API_KEY = "your-groq-api-key"
```

---

Feel free to try it and let me know what you think!