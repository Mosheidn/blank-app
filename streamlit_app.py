# Rayon MVP App – Version without images, with emoji icons and improved search

import streamlit as st
import pandas as pd
import time
import random
from difflib import get_close_matches

# Set page config
st.set_page_config(page_title="Rayon – Ideas in Motion", layout="wide")

# ---------- Initialization ----------

@st.cache_data
def generate_ideas(num=1000):
    now = time.time()
    authors = ["Idan", "Alex", "Lina", "Jordan", "Sam", "Taylor", "Riley", "Morgan", "Dana", "Casey"]
    base_titles = [
        "AI Coach for ", "Marketplace for ", "Decentralized ", "Emotional ", "Micro-Volunteering ",
        "Interactive Tool for ", "Collaborative Space for ", "Crowdsourced Map of ", "Gamified App for ", "Open Source Project on "
    ]
    base_topics = [
        "Habits", "Projects", "Learning", "Task Management", "Civic Actions",
        "Productivity", "Ideas", "Urban Data", "Self-Growth", "Climate Tech"
    ]
    emoji_map = {
        "Habits": "🧘",
        "Projects": "🛠️",
        "Learning": "📚",
        "Task Management": "✅",
        "Civic Actions": "🌍",
        "Productivity": "🚀",
        "Ideas": "💡",
        "Urban Data": "🏙️",
        "Self-Growth": "🌱",
        "Climate Tech": "♻️"
    }
    titles, descriptions, tags, authors_list, icons = [], [], [], [], []
    for i in range(num):
        prefix = random.choice(base_titles)
        topic = random.choice(base_topics)
        full_title = prefix + topic + f" #{i}"
        titles.append(full_title)
        descriptions.append(f"A platform to explore: {prefix.lower()}{topic.lower()}.")
        tags.append(topic)
        authors_list.append(random.choice(authors))
        icons.append(emoji_map[topic])

    return pd.DataFrame({
        "id": range(num),
        "author": authors_list,
        "title": titles,
        "description": descriptions,
        "tags": tags,
        "icon": icons,
        "support": [random.uniform(20, 100) for _ in range(num)],
        "velocity": [random.uniform(0.1, 0.4) for _ in range(num)],
        "acceleration": [random.uniform(0.01, 0.04) for _ in range(num)],
        "last_updated": [now]*num
    })

if "ideas" not in st.session_state:
    st.session_state.ideas = generate_ideas(1000)

if "supported_ideas" not in st.session_state:
    st.session_state.supported_ideas = set()

if "search_query" not in st.session_state:
    st.session_state.search_query = ""

if "page" not in st.session_state:
    st.session_state.page = 0

# ---------- UI Header ----------
st.markdown("""
<style>
.rayon-title {
    font-size: 6vw;
    font-weight: 700;
    color: #2C3E50;
    text-align: center;
    margin-bottom: 10px;
}
.rayon-subtext {
    font-size: 4vw;
    text-align: center;
    color: #7F8C8D;
    margin-bottom: 30px;
    padding: 0 10px;
}
.author-tag {
    font-size: 3.2vw;
    color: #555;
}
@media (min-width: 768px) {
  .rayon-title { font-size: 36px; }
  .rayon-subtext { font-size: 18px; }
  .author-tag { font-size: 14px; }
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="rayon-title">Rayon – Ideas in Motion</div>', unsafe_allow_html=True)
st.markdown('<div class="rayon-subtext">Support ideas that matter. Watch them grow with momentum over time.</div>', unsafe_allow_html=True)

# ---------- Search and Filter ----------
st.session_state.search_query = st.text_input("🔎 Search ideas by keyword or tag")

# ---------- Filter Ideas ----------
def filter_ideas():
    df = st.session_state.ideas
    q = st.session_state.search_query.lower().strip()
    if q:
        mask = df.apply(lambda row: q in row['title'].lower() or q in row['description'].lower() or q in row['tags'].lower(), axis=1)
        df = df[mask]
    return df.sort_values(by="support", ascending=False)

# ---------- Pagination ----------
IDEAS_PER_PAGE = 10
all_ideas = filter_ideas()
total_pages = (len(all_ideas) - 1) // IDEAS_PER_PAGE + 1

start_idx = st.session_state.page * IDEAS_PER_PAGE
end_idx = start_idx + IDEAS_PER_PAGE
paged_ideas = all_ideas.iloc[start_idx:end_idx]

# ---------- Display Paged Ideas ----------
for _, row in paged_ideas.iterrows():
    with st.container():
        st.markdown(f"### {row['icon']} {row['title']}")
        st.write(row['description'])
        st.write(f"Tags: #{row['tags']}")
        st.markdown(f"<span class='author-tag'>Shared by {row['author']}</span>", unsafe_allow_html=True)
        st.caption(f"Support: {row['support']:.1f} | Velocity: {row['velocity']:.2f} | Acceleration: {row['acceleration']:.2f}")
        if st.button("Support this idea", key=f"support_{row['id']}"):
            if row['id'] not in st.session_state.supported_ideas:
                st.session_state.ideas.at[row.name, "acceleration"] += 0.05
                st.session_state.supported_ideas.add(row['id'])
            else:
                st.warning("You already supported this idea.")

# ---------- Page Navigation (Bottom) ----------
st.write(f"Page {st.session_state.page + 1} of {total_pages}")
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("⬅️ Previous", key="prev_bottom") and st.session_state.page > 0:
        st.session_state.page -= 1
with col3:
    if st.button("Next ➡️", key="next_bottom") and st.session_state.page < total_pages - 1:
        st.session_state.page += 1
