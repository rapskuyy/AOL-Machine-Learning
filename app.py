import streamlit as st
import model

st.title("Game Recommendation System")

option = st.selectbox("Choose recommendation method", [
    "By Game Name",
    "By Tags",
    "By Genres",
    "By Description"
])

if option == "By Game Name":
    title_input = st.selectbox("Select game name", model.get_all_game_names())
    if st.button("Recommend"):
        if title_input in model.indices:
            results = model.recommend(title_input, model.cosine_sim_combined)
            st.write(results)
        else:
            st.error("Game not found. Please check the name or try selecting from the list.")

elif option == "By Tags":
    tg_input = st.multiselect("Select one or more tags", model.get_all_tags())
    if st.button("Recommend"):
        results = model.recommend_by(tg_input, model.tfid, model.matrix_tag)
        st.write(results)

elif option == "By Genres":
    genre_input = st.multiselect("Select one or more genres", model.get_all_genres())
    if st.button("Recommend"):
        results = model.recommend_by(genre_input, model.tfid2, model.matrix_genre)
        st.write(results)

elif option == "By Description":
    description_input = st.text_area("Enter description text")
    if st.button("Recommend"):
        results = model.recommend_by_description(description_input)
        st.write(results)