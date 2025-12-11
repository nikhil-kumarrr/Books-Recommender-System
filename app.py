import streamlit as st
import pandas as pd

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(page_title="Book Recommender", layout="wide")

# ---------------------------------------------------------
# DARK MODE / LIGHT MODE TOGGLE
# ---------------------------------------------------------
mode = st.sidebar.radio("🌗 Choose Theme", ["Light Mode", "Dark Mode"])

if mode == "Light Mode":
    background = "linear-gradient(135deg, #d8e9ff, #f5faff)"
    card_bg = "rgba(255, 255, 255, 0.72)"
    card_border = "rgba(255,255,255,0.35)"
    title_color = "#002b5c"
    author_color = "#444"
else:
    background = "linear-gradient(135deg, #1f1f1f, #121212)"
    card_bg = "rgba(30, 30, 30, 0.85)"
    card_border = "rgba(255,255,255,0.15)"
    title_color = "#e6e6e6"
    author_color = "#bbbbbb"

# ---------------------------------------------------------
# ULTRA MODERN UI (Glassmorphism + Hover Animation)
# ---------------------------------------------------------
st.markdown(f"""
<style>
body, .stApp {{
    background: {background};
    transition: all 0.3s ease-in-out;
}}

/* Page Title */
h1, h2, h3, h4 {{
    font-family: 'Segoe UI', sans-serif;
    font-weight: 700 !important;
    color: {title_color} !important;
}}

/* Book Card */
.card {{
    background: {card_bg};
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    padding: 22px;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0px 4px 18px rgba(0,0,0,0.15);
    transition: 0.25s ease-in-out;
    border: 1px solid {card_border};
}}

.card:hover {{
    transform: translateY(-6px) scale(1.03);
    box-shadow: 0px 6px 22px rgba(0,0,0,0.35);
}}

/* Book Title */
.book-title {{
    font-size: 20px;
    font-weight: 700;
    margin-top: 12px;
    margin-bottom: 6px;
    color: {title_color};
}}

/* Book Author */
.book-author {{
    font-size: 16px;
    color: {author_color};
    margin-bottom: 4px;
}}

/* Sidebar glass look */
.css-1d391kg, .css-1lcbmhc {{
    background: rgba(255, 255, 255, 0.70) !important;
    backdrop-filter: blur(12px) !important;
    border-right: 1px solid rgba(255,255,255,0.35);
}}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# DATA (Embedded)
# ---------------------------------------------------------
books_data = {
    "Book-Title": [
        "The Alchemist", "Harry Potter", "The Power of Habit",
        "Atomic Habits", "Rich Dad Poor Dad", "The Hobbit"
    ],
    "Book-Author": [
        "Paulo Coelho", "J.K. Rowling", "Charles Duhigg",
        "James Clear", "Robert Kiyosaki", "J.R.R. Tolkien"
    ],
    "Image-URL": [
        "https://m.media-amazon.com/images/I/71aFt4+OTOL.jpg",
        "https://m.media-amazon.com/images/I/81YOuOGFCJL.jpg",
        "https://m.media-amazon.com/images/I/91bYsX41DVL.jpg",
        "https://m.media-amazon.com/images/I/81wgcld4wxL.jpg",
        "https://m.media-amazon.com/images/I/81bsw6fnUiL.jpg",
        "https://m.media-amazon.com/images/I/91b0C2YNSrL.jpg",
    ]
}

df = pd.DataFrame(books_data)

similar_books = {
    "The Alchemist": ["The Hobbit", "Atomic Habits", "Rich Dad Poor Dad"],
    "Harry Potter": ["The Hobbit", "The Alchemist", "Atomic Habits"],
    "The Power of Habit": ["Atomic Habits", "Rich Dad Poor Dad", "The Alchemist"],
    "Atomic Habits": ["The Power of Habit", "Rich Dad Poor Dad", "The Alchemist"],
    "Rich Dad Poor Dad": ["The Power of Habit", "Atomic Habits", "The Alchemist"],
    "The Hobbit": ["Harry Potter", "The Alchemist", "Atomic Habits"]
}

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
menu = st.sidebar.radio(
    "📘 Menu",
    ["Popular Books", "Recommend Books"]
)

# ---------------------------------------------------------
# POPULAR BOOKS PAGE
# ---------------------------------------------------------
if menu == "Popular Books":
    st.title("🔥 Trending & Popular Books")
    cols = st.columns(3)
    index = 0

    for i, row in df.iterrows():
        with cols[index]:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.image(row["Image-URL"], use_column_width=True)
            st.markdown(f"<div class='book-title'>{row['Book-Title']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='book-author'>{row['Book-Author']}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        index = (index + 1) % 3

# ---------------------------------------------------------
# RECOMMENDATION PAGE
# ---------------------------------------------------------
if menu == "Recommend Books":
    st.title("🎯 Smart Book Recommendation System")

    selected_book = st.selectbox("Choose a Book", df["Book-Title"])

    if st.button("🔍 Recommend"):
        st.subheader(f"✨ Books similar to **{selected_book}**")

        recs = similar_books[selected_book]
        result_df = df[df["Book-Title"].isin(recs)]

        cols = st.columns(3)
        index = 0

        for i, row in result_df.iterrows():
            with cols[index]:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.image(row["Image-URL"], use_column_width=True)
                st.markdown(f"<div class='book-title'>{row['Book-Title']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='book-author'>{row['Book-Author']}</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            index = (index + 1) % 3
