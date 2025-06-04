# Game Recommendation System



**Business Understanding**

In today’s digital entertainment landscape, gamers often struggle to discover new titles that match their interests. With a massive influx of games released on platforms like Steam, personalized recommendations are crucial to improving user experience and increasing engagement.

A Game Recommendation System helps users find games similar to their preferences based on existing information such as genres, tags, or even game descriptions. This project demonstrates how content-based filtering using Natural Language Processing (NLP) techniques can be applied in this context.

**Business Problem**

With the growing number of games released annually on platforms like Steam, users often struggle to find titles that align with their interests. Without an effective recommendation system, users may feel overwhelmed and dissatisfied, potentially reducing engagement and retention. This creates a need for a personalized game recommendation system to help users navigate the vast game library.

Key Business Questions:

How can we help users discover games that match their preferences among thousands of available titles?

How can a recommendation system enhance user satisfaction and retention?

**Project Scope**

1. Primary Objective
To build a content-based game recommendation system that can:

* Recommend similar games based on a selected title.
* Recommend games using specific tags or genres.
* Recommend games using a description provided by the user.

The system should run as an interactive **Streamlit web application** and deliver relevant recommendations using **TF-IDF vectorization** and **cosine similarity**.

2. Technical Scope

Utilize a Steam games dataset (from Kaggle).

Perform text preprocessing on description, tags, and genre columns.

Apply TF-IDF vectorization to extract relevant features.

Use cosine similarity to measure game similarity.

Return a ranked list of recommended games based on a selected input game.

3. Project Limitations

Does not include behavior-based or clickstream user data.

No user interface (UI/UX) or production deployment included.

Focuses solely on Content-Based Filtering (not full Collaborative Filtering).

4. Expected Outputs

A recommendation model that suggests similar games based on a single input game.

Subjective evaluation of recommendation quality based on relevance.


**About Dataset**

The dataset (`games.csv`) consists of metadata about 20,000 games and includes the following features:

* `AppID`
* `Name`
* `Release date`
* `Tags`
* `Genres`
* `Supported languages` (used as description)

Modifications:

* The column `Supported languages` was renamed to `Description`.
* Only the top 20,000 records were used.
* Missing values were filled with empty strings.

------------------------------------------------------

**Data Preparation**

1. Column Selection and Renaming

![image](https://github.com/user-attachments/assets/079908d3-84ae-406d-bb11-1f8a499eb230)


2. Cleaning and Formatting

* All NaNs in `Tags`, `Genres`, and `Description` were filled with empty strings.
* The text in these fields was cleaned and formatted by wrapping terms in quotes and sorting alphabetically for consistent vectorization.

3. TF-IDF Vectorization


Separate `TfidfVectorizer()` instances were applied to:

* `Tags`
* `Genres`

* `Description`

These were then used to create sparse matrices for similarity computation.

![image](https://github.com/user-attachments/assets/4b2fcf82-8e3a-4695-bbda-05375f48b8cf)



**Modeling**

Recommendation Techniques:

1. By Game Name

* Input: selected game title.
* Method: calculate cosine similarity between the selected game’s combined `Tags + Genres` vector and all others.
* Output: top 20 similar games.

 2. By Genres or Tags

* Input: one or more tags/genres.
* Method: transform the input into TF-IDF, calculate cosine similarity with the dataset.
* Output: top 20 games with matching characteristics.

3. By Description

* Input: free-text game description.
* Method: transform user description into TF-IDF, compute cosine similarity with game descriptions.
* Output: top 20 most relevant games.

Each method uses the following function structure:

![image](https://github.com/user-attachments/assets/f703c49f-1887-4501-9f96-c3dc6a82caa6)



Evaluation

The system displays recommendations in a tabular format on a **Streamlit app**. Each result includes:

* Game name
* Tags
* Genres
* Description
* Similarity score (as a percentage)

Example:

| Name   | Tags          | Genres     | Score (%) |
| ------ | ------------- | ---------- | --------- |
| Game A | Action, Indie | Casual     | 98.5      |
| Game B | Adventure     | Simulation | 97.2      |
| ...    | ...           | ...        | ...       |

While formal accuracy metrics aren't applicable to unsupervised recommendation systems, the quality of results is measured by:

* Relevance of top results.
* Consistency across input types.
* Diversity in recommendations.


Conclusion

The **Game Recommendation System** demonstrates that **content-based filtering** using **TF-IDF** and **cosine similarity** is a viable approach for recommending games based on textual features.

With support for multiple input methods (title, genre, and description), it provides flexible discovery paths and is accessible through a simple **Streamlit web UI**.


