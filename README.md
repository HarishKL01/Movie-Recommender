Here is a fully formatted, GitHub-ready `README.md` complete with a structured layout, code blocks, API examples, and project hierarchy. You can copy this directly into your repository.

---

# 🎬 MovieLens Recommendation API

A fast, lightweight recommendation backend built with Python, FastAPI, and Pandas. This API powers movie searches, genre listings, and personalized recommendations using the classic MovieLens dataset.

## 🚀 Features

* **Content-Based Filtering:** Generates recommendations using weighted ratings for a user's favorite genre.


* **Item-Item Collaborative Filtering:** Suggests similar movies using a correlation matrix based on user rating patterns.


* **Live Search:** Features a case-insensitive search endpoint designed to power a frontend autocomplete box.


* **CORS Enabled:** Pre-configured with Cross-Origin Resource Sharing middleware to accept requests from any frontend application.



## 🛠️ Tech Stack

* **Framework:** FastAPI


* **Data Processing:** Pandas, NumPy


* **Server:** Uvicorn
* **Validation:** Pydantic



## 📂 Project Structure

```text
├── main.py                # FastAPI application and route definitions
├── recommender.py         # Recommendation logic and Pandas data processing
├── ml-latest-small/       # Data directory (must be created)
│   ├── movies.csv         # Movie metadata
│   └── ratings.csv        # User ratings
└── README.md

```

## ⚙️ Installation & Setup

**1. Clone the repository**

```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name

```

**2. Install dependencies**

```bash
pip install fastapi uvicorn pandas numpy pydantic

```

**3. Download the Dataset**

* Download the MovieLens dataset directly from [GroupLens](https://www.google.com/search?q=https://files.grouplens.org/datasets/movielens/ml-latest-small.zip).


* Extract the contents into a folder named `ml-latest-small` in your project root.


* Ensure `movies.csv` and `ratings.csv` are located directly inside this directory.



**4. Run the Server**

```bash
uvicorn main:app --reload

```

The API will be available at `[http://127.0.0.1:8000](http://127.0.0.1:8000)`. You can also view the interactive Swagger API documentation at `[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)`.

## 📡 API Reference

### 1. Get Available Genres

Returns a sorted list of every distinct genre found in the dataset[cite: 1, 2].

* **Endpoint:** `GET /genres`

* **Response:**
```json
[
  "Action",
  "Adventure",
  "Animation",
  "Comedy"
]

```



### 2. Search Movies

Returns the `id` and `title` for up to 10 movies whose titles match the query string[cite: 1, 2].

* **Endpoint:** `GET /movies/search?query={text}`

* **Response:**
```json
[
  {"id": 1, "title": "Toy Story (1995)"},
  {"id": 3114, "title": "Toy Story 2 (1999)"}
]

```



### 3. Get Recommendations

Accepts a user profile and returns a personalized list of recommendations. Provide either a `favorite_genre` or `favorite_movie` to trigger the respective recommendation engine.

* **Endpoint:** `POST /recommend`

* **Request Body:**
```json
{
  "name": "Jane Doe",
  "age": 28,
  "favorite_genre": "Sci-Fi",
  "favorite_movie": null
}

```



## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## 📝 License

This project is open source and available under the [MIT License](https://www.google.com/search?q=LICENSE).

---

Would you like me to draft a quick `requirements.txt` or `.gitignore` file to complete your repository setup?
