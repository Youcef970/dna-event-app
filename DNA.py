import streamlit as st
import random
import pandas as pd
from urllib.parse import quote

# ------------------ DNA Utility Functions ------------------ #
def random_dna(length=10):
    return ''.join(random.choice('ATCG') for _ in range(length))

def compare_dna(seq1, seq2):
    alignment = ""
    matches = 0
    mismatches = 0
    for a, b in zip(seq1, seq2):
        if a == b:
            alignment += f"🟩{a}"
            matches += 1
        else:
            alignment += f"🟥{a}"
            mismatches += 1
    similarity = (matches / len(seq1)) * 100
    return alignment, similarity, matches, mismatches


# ------------------ Page Setup ------------------ #
st.set_page_config(page_title="DNA Event Demo", layout="centered")
st.title("🧬 DNA Comparison Interactive Exhibit")

st.image("https://media.giphy.com/media/3o6Zt481isNVuQI1l6/giphy.gif", width=200)


# ------------------ Session State Init ------------------ #
if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = []

if "seq2" not in st.session_state:
    st.session_state.seq2 = random_dna(10)


# ------------------ Input Section ------------------ #
st.subheader("Step 1: Enter your DNA sequence")

name = st.text_input("Your name (for leaderboard):")
seq1 = st.text_input("DNA (use letters A, T, C, G only):", "ATCGATCGAT").upper()

species_choices = {
    "Random Sequence": random_dna(len(seq1)),
    "Cat": "ATCGTACGTA",
    "Dog": "ATGGTACCTA",
    "Superhero": "TACCGGATAC",
    "Alien Creature": "CGTACGATCG"
}

option = st.selectbox("Step 2: Compare with:", list(species_choices.keys()))
seq2 = species_choices[option]

# Make seq2 same length
if len(seq2) != len(seq1):
    seq2 = random_dna(len(seq1))


# ------------------ Compare Button ------------------ #
if st.button("🔍 Compare Now"):
    if not name:
        st.error("Please enter your name before comparing!")
    elif any(base not in "ATCG" for base in seq1):
        st.error("DNA must contain only A, T, C, G letters!")
    else:
        alignment, sim, match, mismatch = compare_dna(seq1, seq2)
        st.success("Comparison Complete!")

        st.write(f"📌 Comparing with **{option}**")
        st.markdown(f"**Sequence 2:** {seq2}")
        st.markdown(f"🧬 **Alignment:** {alignment}")
        st.write(f"🎯 Similarity: **{sim:.2f}%**")

        # Bar Chart
        chart = pd.DataFrame({"Count": [match, mismatch]}, index=["Matches", "Mismatches"])
        st.bar_chart(chart)

        # Update Leaderboard instantly
        st.session_state.leaderboard.append((name, sim))
        st.session_state.leaderboard = sorted(st.session_state.leaderboard, key=lambda x: x[1], reverse=True)


# ------------------ Leaderboard (Always Visible) ------------------ #
if st.session_state.leaderboard:
    st.subheader("🏆 Live Leaderboard")
    for i, (n, s) in enumerate(st.session_state.leaderboard, 1):
        st.write(f"{i}. {n}: {s:.2f}%")


# ------------------ QR Code Section ------------------ #
st.markdown("---")
st.subheader("📱 Play with this online!")

app_url = "https://youcef970-dna-event-app-dna-keckja.streamlit.app/"
encoded_url = quote(app_url)

st.write(f"🔗 [Click here to open the app]({app_url})")
st.image(f"https://api.qrserver.com/v1/create-qr-code/?size=180x180&data={encoded_url}")
