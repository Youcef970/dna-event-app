import streamlit as st
import random

# -----------------------------
# Helper Functions
# -----------------------------
def random_dna(length=10):
    """Generate a random DNA sequence"""
    return ''.join(random.choice('ATCG') for _ in range(length))

def compare_dna(seq1, seq2):
    """Compare two DNA sequences and return alignment and similarity"""
    alignment = ""
    matches = 0
    for a, b in zip(seq1, seq2):
        if a == b:
            alignment += f"🟩{a}"  # Green for match
            matches += 1
        else:
            alignment += f"🟥{a}"  # Red for mismatch
    similarity = matches / len(seq1) * 100
    return alignment, similarity

# -----------------------------
# App Layout
# -----------------------------
st.set_page_config(page_title="DNA Comparison Demo", layout="wide")
st.title("🧬 Interactive DNA Comparison")
st.markdown("Compare DNA sequences, see the similarity, and have fun with species DNA!")

# Display GIF (local or hosted)
st.image("https://media.giphy.com/media/3o6Zt481isNVuQI1l6/giphy.gif", width=200)

# -----------------------------
# Species DNA examples
# -----------------------------
species_dna = {
    "Cat": "ATCGTACGTA",
    "Dog": "ATGGTACCTA",
    "Superhero": "TACCGGATAC",
    "Fictional Creature": "CGTACGATCG"
}

# -----------------------------
# User Inputs
# -----------------------------
seq1 = st.text_input("Enter your DNA sequence (A,T,C,G):", random_dna(10))

option = st.selectbox("Compare with:", ["Random Sequence"] + list(species_dna.keys()))

if option == "Random Sequence":
    seq2 = random_dna(len(seq1))
else:
    seq2 = species_dna[option]

# -----------------------------
# Compare DNA
# -----------------------------
if st.button("Compare"):
    if len(seq1) != len(seq2):
        st.error("Sequences must be the same length!")
    else:
        alignment, similarity = compare_dna(seq1.upper(), seq2.upper())
        st.markdown(f"**Sequence to compare:** {seq2}")
        st.markdown(f"**Alignment:** {alignment}")
        st.markdown(f"**Similarity:** {similarity:.2f}%")

        # -----------------------------
        # Visitor Leaderboard
        # -----------------------------
        if 'leaderboard' not in st.session_state:
            st.session_state.leaderboard = []

        name = st.text_input("Enter your name for the leaderboard:")
        if st.button("Submit for Leaderboard"):
            if name:
                st.session_state.leaderboard.append((name, similarity))
                st.session_state.leaderboard.sort(key=lambda x: x[1], reverse=True)

        if st.session_state.leaderboard:
            st.subheader("🏆 Leaderboard")
            for i, (n, s) in enumerate(st.session_state.leaderboard, 1):
                st.write(f"{i}. {n}: {s:.2f}%")

# -----------------------------
# QR Code
# -----------------------------
st.markdown("---")
st.subheader("📱 Take this demo with you!")
app_url = "https://share.streamlit.io/your-username/your-repo/main/dna_demo.py"  # Replace with your deployed URL
st.markdown("Scan this QR code to access the interactive demo online:")
st.image(f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={app_url}")
