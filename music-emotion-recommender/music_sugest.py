import streamlit as st
import pandas as pd
import random

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("Clustered_df.csv")
    return df

df = load_data()

# Emotion mapping with colors & emojis
emotion_map = {
    "Happy 😀": {"valence": (0.6, 1.0), "energy": (0.6, 1.0), "color": "#FFD93D", "emoji": "✨"},
    "Sad 😔": {"valence": (0.0, 0.4), "energy": (0.0, 0.4), "color": "#4D96FF", "emoji": "💧"},
    "Angry 😡": {"valence": (0.0, 0.4), "energy": (0.6, 1.0), "color": "#FF4C29", "emoji": "🔥"},
    "Relaxed 😌": {"valence": (0.6, 1.0), "energy": (0.0, 0.4), "color": "#6BCB77", "emoji": "🍃"},
    "Neutral 🙂": {"valence": (0.4, 0.6), "energy": (0.4, 0.6), "color": "#B0BEC5", "emoji": "⚪"},
}

# Simple text-based emotion detection
def detect_emotion(user_input):
    text = user_input.lower()
    if any(word in text for word in ["happy", "joy", "excited", "fun"]):
        return "Happy 😀"
    elif any(word in text for word in ["sad", "down", "lonely", "depressed"]):
        return "Sad 😔"
    elif any(word in text for word in ["angry", "mad", "furious", "rage"]):
        return "Angry 😡"
    elif any(word in text for word in ["relax", "calm", "peace", "chill"]):
        return "Relaxed 😌"
    else:
        return "Neutral 🙂"

# Streamlit UI setup
st.set_page_config(page_title="Emotion Music Recommender", layout="centered")

st.title("🎵 Emotion-Based Music Recommendation System")
st.write("Type your feelings or select an emotion to get personalized song suggestions!")

# User input
user_text = st.text_input("📝 How are you feeling right now?")
detected_emotion = detect_emotion(user_text) if user_text else None

# Manual selection fallback
manual_emotion = st.selectbox("Or select from here:", list(emotion_map.keys()))

# Final emotion choice
emotion = detected_emotion if detected_emotion else manual_emotion
color = emotion_map[emotion]["color"]
emoji = emotion_map[emotion]["emoji"]

# Dynamic background
page_bg = f"""
<style>
.stApp {{
    background-color: {color};
    color: black;
}}

.emoji-float {{
  position: fixed;
  top: -50px;
  font-size: 40px;
  animation: fall 6s infinite;
}}

@keyframes fall {{
  0% {{ top: -50px; opacity: 1; }}
  100% {{ top: 100vh; opacity: 0; }}
}}
</style>
"""

st.markdown(page_bg, unsafe_allow_html=True)

# Floating emoji animation
for i in range(10):  # number of floating emojis
    st.markdown(
        f"<div class='emoji-float' style='left:{random.randint(5,90)}%; animation-delay:{random.uniform(0,3)}s;'>{emoji}</div>",
        unsafe_allow_html=True,
    )

if st.button("Get Recommendations 🎶"):
    v_range = emotion_map[emotion]["valence"]
    e_range = emotion_map[emotion]["energy"]

    # Filter songs
    filtered = df[
        (df["valence"] >= v_range[0]) & (df["valence"] <= v_range[1]) &
        (df["energy"] >= e_range[0]) & (df["energy"] <= e_range[1])
    ]

    if filtered.empty:
        st.warning("😕 No songs found for this mood. Try another one!")
    else:
        recommendations = filtered.sample(min(8, len(filtered)))

        st.subheader(f"🎶 Songs Recommended for {emotion}")
        for idx, row in recommendations.iterrows():
            st.markdown(f"""
            <div style="padding:10px; margin:10px; border-radius:15px; background:#ffffffaa;">
                <h4>🎵 {row['name']}</h4>
                <p>👨‍🎤 Artist: {row['artists']}<br>
                🔀 Cluster: {row['Cluster']}<br>
                📊 Popularity: {row['popularity']}</p>
            </div>
            """, unsafe_allow_html=True)