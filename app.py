import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Book Recommendation System",
    layout="wide"
)

# ---------------- UI STYLE ----------------
st.markdown("""
<style>
.stApp { background-color: #eaf4ff; }
.book-card img {
    width: 150px;
    height: 220px;
    border-radius: 12px;
}
.book-title {
    font-weight: 600;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("books.csv")
    df = df.fillna("")
    df = df.drop_duplicates("Book-Title")

    df["combined"] = df["Book-Title"] + " " + df["Book-Author"]

    tfidf = TfidfVectorizer(stop_words="english", max_features=4000)
    vectors = tfidf.fit_transform(df["combined"])
    similarity = cosine_similarity(vectors)

    return df.reset_index(drop=True), similarity


books, similarity = load_data()

# ---------------- SIDEBAR ----------------
feature = st.sidebar.radio(
    "Select Feature",
    ["Popular Books", "Recommend Books"]
)

# ---------------- POPULAR BOOKS ----------------
if feature == "Popular Books":

    st.header("Popular Books")

    for _, row in books.head(10).iterrows():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.image(row["Image-URL-M"])
        with col2:
            st.subheader(row["Book-Title"])
            st.write(f"Author: {row['Book-Author']}")
        st.write("")

# ---------------- RECOMMEND BOOKS ----------------
else:

    st.header("Book Recommendation System")

    selected_book = st.selectbox(
        "Select a Book",
        books["Book-Title"].tolist()
    )

    if st.button("Recommend"):

        idx = books[books["Book-Title"] == selected_book].index[0]
        scores = list(enumerate(similarity[idx]))
        scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:6]

        st.subheader(f"Books similar to {selected_book}")

        cols = st.columns(5)
        for i, (book_idx, _) in enumerate(scores):
            with cols[i]:
                st.image(books.iloc[book_idx]["Image-URL-M"])
                st.markdown(
                    f"<div class='book-title'>{books.iloc[book_idx]['Book-Title']}</div>",
                    unsafe_allow_html=True
                )
                st.caption(books.iloc[book_idx]["Book-Author"])
