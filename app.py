import streamlit as st
import random
import re
from collections import Counter

st.set_page_config(
    page_title="Emoji Story Challenge",
    page_icon="📖",
    layout="centered"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>

.stApp{
    background:#0d1117;
    color:white;
}

.block-container{
    padding-top:2rem;
}

h1,h2,h3,h4,p,label{
    color:white;
}

.bigemoji{
    font-size:60px;
    text-align:center;
    margin-top:20px;
    margin-bottom:20px;
}

.scorecard{
    background:#161b22;
    padding:20px;
    border-radius:15px;
    border:1px solid #30363d;
}

.feedback{
    background:#161b22;
    padding:18px;
    border-radius:15px;
    border-left:6px solid #58a6ff;
}

.history{
    background:#161b22;
    padding:15px;
    border-radius:15px;
    margin-bottom:10px;
}

textarea{
    border-radius:15px !important;
}

div.stButton>button{
    width:100%;
    border-radius:12px;
    height:3em;
    background:#238636;
    color:white;
    font-weight:bold;
    border:none;
    font-size:17px;
}

div.stButton>button:hover{
    background:#2ea043;
    color:white;
}

.badge{
    font-size:28px;
    font-weight:bold;
    text-align:center;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Title
# -----------------------------
st.markdown(
    "<h1 style='text-align:center;'>🎭 Emoji Story Challenge</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center;color:lightgray;'>Write a creative story using all the emojis!</p>",
    unsafe_allow_html=True
)

# -----------------------------
# Emoji Categories
# -----------------------------
emoji_pool = [

# Faces
"😀","😎","🥳","😂","😍","🤯","😱","🤩","😴","🤖",

# Animals
"🐶","🐱","🦁","🐼","🐸","🐵","🦊","🐧","🦄","🐢",

# Nature
"🌳","🌲","🌴","🌸","🌻","🌈","🌊","🔥","❄️","🌙",

# Food
"🍕","🍔","🍩","🍎","🍓","🍉","🍦","🍰","☕","🍿",

# Travel
"🚗","🚕","🚀","✈️","🚂","🚢","🏖️","🏝️","🗻","🏰",

# Objects
"📚","🎁","🎈","🕰️","💎","🧸","🧩","🎨","🎵","💡",

# Fantasy
"🧙","🧚","🐉","👑","⚔️","🪄","🦅","🏹","🛡️","🧝",

# Sports
"⚽","🏀","🏆","🎾","🏸","🏏","🥊","🏊","🚴","🎯",

# Weather
"☀️","🌧️","⛈️","🌪️","🌨️","💨","🌤️","🌥️","🌦️","🌫️",

# Misc
"❤️","⭐","🎉","🎃","🎄","📷","🎬","📱","⌛","🔑"

]

# -----------------------------
# Session State
# -----------------------------
if "challenge" not in st.session_state:
    st.session_state.challenge = random.sample(emoji_pool,4)

if "history" not in st.session_state:
    st.session_state.history = []

if "score" not in st.session_state:
    st.session_state.score = None

if "feedback" not in st.session_state:
    st.session_state.feedback = ""

if "badge" not in st.session_state:
    st.session_state.badge = ""

if "creativity" not in st.session_state:
    st.session_state.creativity = 0

if "length_score" not in st.session_state:
    st.session_state.length_score = 0

if "emoji_score" not in st.session_state:
    st.session_state.emoji_score = 0

# -----------------------------
# New Challenge Button
# -----------------------------
if st.button("🎲 New Emoji Challenge"):
    st.session_state.challenge = random.sample(emoji_pool,4)
    st.session_state.score = None
    st.session_state.feedback = ""
    st.session_state.badge = ""
    st.rerun()

# -----------------------------
# Display Emojis
# -----------------------------
st.markdown(
    f"<div class='bigemoji'>{' '.join(st.session_state.challenge)}</div>",
    unsafe_allow_html=True
)

st.divider()

# -----------------------------
# Story Input
# -----------------------------
story = st.text_area(
    "✍️ Write your story",
    height=260,
    placeholder="Example: Once upon a time..."
)

st.write("")

score_btn = st.button("✨ Score My Story")

# -----------------------------
# Story Scoring Functions
# -----------------------------

def creativity_score(text):
    words = re.findall(r"\b\w+\b", text.lower())

    if not words:
        return 0

    unique_words = len(set(words))
    total_words = len(words)

    diversity = unique_words / total_words

    sentences = len(
        [s for s in re.split(r"[.!?]+", text) if s.strip()]
    )

    score = 0

    # Vocabulary Diversity (20)
    if diversity >= 0.80:
        score += 20
    elif diversity >= 0.70:
        score += 18
    elif diversity >= 0.60:
        score += 15
    elif diversity >= 0.50:
        score += 10
    else:
        score += 5

    # Unique Words (10)
    if unique_words >= 80:
        score += 10
    elif unique_words >= 60:
        score += 8
    elif unique_words >= 40:
        score += 6
    elif unique_words >= 20:
        score += 4
    else:
        score += 2

    # Sentence Variety (10)
    if sentences >= 8:
        score += 10
    elif sentences >= 6:
        score += 8
    elif sentences >= 4:
        score += 6
    elif sentences >= 2:
        score += 4
    else:
        score += 2

    return min(score, 40)


# -----------------------------
# Length Score
# -----------------------------

def length_score(text):

    words = len(text.split())

    if words >= 120:
        return 30

    elif words >= 80:
        return 25

    elif words >= 50:
        return 18

    elif words >= 25:
        return 10

    else:
        return 5


# -----------------------------
# Emoji Usage Score
# -----------------------------

def emoji_usage_score(text, emojis):

    used = 0

    for emoji in emojis:
        if emoji in text:
            used += 1

    if used == 4:
        score = 30
    elif used == 3:
        score = 24
    elif used == 2:
        score = 18
    elif used == 1:
        score = 10
    else:
        score = 0

    return score, used


# -----------------------------
# Bonus Points
# -----------------------------

def bonus_points(text):

    bonus = 0

    lower = text.lower().strip()

    if lower.startswith("once upon a time"):
        bonus += 3

    if '"' in text or "'" in text:
        bonus += 2

    if text.strip().endswith("!"):
        bonus += 2

    return bonus


# -----------------------------
# Badge
# -----------------------------

def get_badge(score):

    if score >= 95:
        return "🌟 Master Storyteller"

    elif score >= 80:
        return "🥇 Excellent"

    elif score >= 60:
        return "🥈 Good"

    elif score >= 40:
        return "🥉 Beginner"

    else:
        return "🙂 Keep Practicing"


# -----------------------------
# Feedback Generator
# -----------------------------

def generate_feedback(total, creativity, length, emoji_score, used):

    feedback = []

    if creativity >= 35:
        feedback.append("🌟 Your imagination is fantastic!")

    elif creativity >= 25:
        feedback.append("✨ Nice creativity. Try adding more descriptive details.")

    else:
        feedback.append("💡 Add richer descriptions and unique ideas.")

    if length >= 25:
        feedback.append("📚 Great story length.")

    elif length >= 18:
        feedback.append("📝 Good length. A few more sentences could improve it.")

    else:
        feedback.append("✍️ Try writing a longer story.")

    if emoji_score == 30:
        feedback.append("😀 You naturally used all the emojis!")

    elif emoji_score >= 18:
        feedback.append(f"😊 You used {used} emojis. Try using all four.")

    else:
        feedback.append("🎭 Include the emojis inside your story.")

    if total >= 90:
        feedback.append("🏆 Outstanding work!")

    elif total >= 75:
        feedback.append("🎉 Great job!")

    elif total >= 50:
        feedback.append("👍 Nice effort. Keep practicing!")

    else:
        feedback.append("🚀 Every story makes you better. Try again!")

    return feedback


# -----------------------------
# Calculate Scores
# -----------------------------

if score_btn:

    if story.strip() == "":

        st.warning("Please write a story first.")

    else:

        creativity = creativity_score(story)

        length = length_score(story)

        emoji_score, used = emoji_usage_score(
            story,
            st.session_state.challenge
        )

        bonus = bonus_points(story)

        total = creativity + length + emoji_score + bonus

        if total > 100:
            total = 100

        st.session_state.creativity = creativity
        st.session_state.length_score = length
        st.session_state.emoji_score = emoji_score
        st.session_state.score = total
        st.session_state.badge = get_badge(total)

        st.session_state.feedback = generate_feedback(
            total,
            creativity,
            length,
            emoji_score,
            used
        )

        st.session_state.history.insert(
            0,
            {
                "emoji": " ".join(st.session_state.challenge),
                "score": total,
                "story": story[:120]
            }
        )

        if len(st.session_state.history) > 10:
            st.session_state.history.pop()

        if total >= 90:
            st.balloons()

# -----------------------------
# Results Section
# -----------------------------

if st.session_state.score is not None:

    st.divider()

    st.subheader("📊 Story Evaluation")

    st.markdown("### 🎨 Creativity")
    st.progress(st.session_state.creativity / 40)
    st.write(f"**{st.session_state.creativity}/40**")

    st.markdown("### 📏 Length")
    st.progress(st.session_state.length_score / 30)
    st.write(f"**{st.session_state.length_score}/30**")

    st.markdown("### 😀 Emoji Usage")
    st.progress(st.session_state.emoji_score / 30)
    st.write(f"**{st.session_state.emoji_score}/30**")

    st.divider()

    st.markdown(
        f"""
<div class="scorecard">
<h2 style="text-align:center;">🏆 Final Score</h2>

<h1 style="text-align:center;color:#58a6ff;">
{st.session_state.score}/100
</h1>

<p class="badge">
{st.session_state.badge}
</p>

</div>
""",
        unsafe_allow_html=True,
    )

    st.write("")

    st.subheader("💬 Feedback")

    for item in st.session_state.feedback:
        st.success(item)

    st.divider()

    st.subheader("📚 Previous Stories")

    for i, record in enumerate(st.session_state.history, start=1):

        with st.container(border=True):

            st.markdown(f"### Story {i}")

            st.markdown(
                f"<div style='font-size:35px'>{record['emoji']}</div>",
                unsafe_allow_html=True,
            )

            st.write(f"**Score:** {record['score']}/100")

            st.caption(record["story"] + "...")

# -----------------------------
# Footer
# -----------------------------

st.divider()

st.markdown(
    """
    <center>

    ⭐ Every challenge uses a different set of emojis.

    Keep playing to improve your creativity!

    </center>
    """,
    unsafe_allow_html=True
)